#!/usr/bin/env python3
"""
Smooth parallax wallpaper for Hyprland.

Renders the wallpaper into a gtk4-layer-shell surface on the `bottom` layer
(above whatever awww/swww has on `background`, below every real window) and
slides it horizontally when the active workspace changes. The image is a
single GPU texture that gets re-blitted at a new offset each frame, driven by
a critically-damped spring, so the motion is continuous at the monitor's
refresh rate rather than a series of discrete crops.

  daemon:        wallpaper-parallax.py
  change image:  wallpaper-parallax.py --set /path/to/image.jpg
  nudge/retune:  wallpaper-parallax.py --reload

Tunables live in CONFIG below. Each also reads an env var, which is read once
at startup -- so to try a setting, restart the daemon with it set:

  wallpaper-parallax.py --quit
  PARALLAX_PAN_PER_WS=300 wallpaper-parallax.py &

Edit CONFIG to make a value stick, since autostart launches it with no env.
"""

import ctypes

# gtk4-layer-shell must be loaded before GTK initialises the Wayland display,
# otherwise its protocol hook never gets installed.
ctypes.CDLL("libgtk4-layer-shell.so.0")

import atexit
import glob
import json
import math
import os
import signal
import socket
import sys

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gsk", "4.0")
gi.require_version("Graphene", "1.0")
gi.require_version("Gtk4LayerShell", "1.0")
gi.require_version("GdkPixbuf", "2.0")

from gi.repository import (  # noqa: E402
    Gdk,
    GdkPixbuf,
    Gio,
    GLib,
    Graphene,
    Gsk,
    Gtk,
)
from gi.repository import Gtk4LayerShell as LayerShell  # noqa: E402

try:  # GLib.unix_signal_add moved namespaces in newer pygobject
    gi.require_version("GLibUnix", "2.0")
    from gi.repository import GLibUnix  # noqa: E402

    unix_signal_add = GLibUnix.signal_add
except (ValueError, ImportError):
    unix_signal_add = GLib.unix_signal_add


# ---------------------------------------------------------------- config ----

def _env(name, default, cast=float):
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    try:
        return cast(raw)
    except ValueError:
        return default


CONFIG = {
    # Horizontal travel per workspace step, in logical pixels. The whole point
    # of the effect -- bigger is more dramatic. The image is scaled up if it
    # isn't wide enough to cover the full travel.
    "pan_per_ws": _env("PARALLAX_PAN_PER_WS", 180.0),

    # Highest workspace that still moves the wallpaper. Workspace N sits at the
    # far end of the pan; anything above it is clamped there.
    "workspaces": int(_env("PARALLAX_WORKSPACES", 10, int)),

    # Spring constants for the pan. `stiffness` sets how fast it travels,
    # `damping_ratio` how it arrives: 1.0 glides to a stop with no overshoot,
    # ~0.75 adds a little bounce. Raise stiffness for a snappier feel.
    "stiffness": _env("PARALLAX_STIFFNESS", 180.0),
    "damping_ratio": _env("PARALLAX_DAMPING", 1.0),

    # Seconds for the wipe when the wallpaper image itself changes. The new
    # image is revealed by a hard edge sweeping left to right.
    "wipe_duration": _env("PARALLAX_WIPE", 0.45),

    # Zoom past cover-fit. 1.0 means the image is never scaled up beyond what
    # it takes to fill the screen, so nothing is cropped to make room for the
    # pan -- instead the pan shrinks to whatever width the image actually has
    # spare. Raise it only if you want more motion out of a 16:9 image and
    # don't mind losing some top and bottom.
    "max_zoom": _env("PARALLAX_MAX_ZOOM", 1.0),
}

STATE_DIR = os.path.join(
    GLib.get_user_state_dir(), "hypr-wallpaper-parallax"
)
STATE_FILE = os.path.join(STATE_DIR, "wallpaper")

FALLBACK_WALLPAPERS = [
    os.path.expanduser("~/Pictures/system/ultra-wide-wallpapers/earth-from-space.jpg"),
    os.path.expanduser("~/.cache/wal/current_wallpaper"),
    os.path.expanduser("~/Pictures/wallpaper3.jpg"),
]


def control_socket_path():
    runtime = GLib.get_user_runtime_dir()
    return os.path.join(runtime, "hypr-wallpaper-parallax.sock")


def smoothstep(t):
    """Ease the wipe edge in and out so it starts and stops without a jolt."""
    t = min(1.0, max(0.0, t))
    return t * t * (3.0 - 2.0 * t)


def log(*a):
    print("[parallax]", *a, file=sys.stderr, flush=True)


DEBUG = bool(os.environ.get("PARALLAX_DEBUG"))


def dlog(*a):
    if DEBUG:
        print("[parallax:dbg]", *a, file=sys.stderr, flush=True)


# ------------------------------------------------------------ hyprland ipc ---

def hypr_socket_dir():
    runtime = GLib.get_user_runtime_dir()
    sig = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE")
    if sig:
        path = os.path.join(runtime, "hypr", sig)
        if os.path.isdir(path):
            return path
    # Launched without the env var (manual start, systemd unit): pick the
    # most recently created instance directory.
    candidates = [p for p in glob.glob(os.path.join(runtime, "hypr", "*")) if os.path.isdir(p)]
    if not candidates:
        return None
    return max(candidates, key=os.path.getmtime)


def hypr_query(command):
    """Send a request over Hyprland's .socket.sock and return the reply."""
    sock_dir = hypr_socket_dir()
    if not sock_dir:
        return None
    path = os.path.join(sock_dir, ".socket.sock")
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)
            s.connect(path)
            s.sendall(command.encode())
            chunks = []
            while True:
                data = s.recv(65536)
                if not data:
                    break
                chunks.append(data)
        return b"".join(chunks).decode(errors="replace")
    except OSError as exc:
        log("hyprctl query failed:", exc)
        return None


def active_workspace_per_monitor():
    """{connector_name: workspace_id} for every monitor Hyprland knows about."""
    raw = hypr_query("j/monitors")
    if not raw:
        return {}
    try:
        monitors = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    out = {}
    for mon in monitors:
        ws = mon.get("activeWorkspace") or {}
        wid = ws.get("id")
        if isinstance(wid, int):
            out[mon.get("name")] = wid
    return out


# -------------------------------------------------------------- the widget ---

class ParallaxSurface(Gtk.Widget):
    """Draws a panorama texture at an animated horizontal offset."""

    __gtype_name__ = "ParallaxSurface"

    def __init__(self, loader):
        super().__init__()
        self._loader = loader

        self._texture = None
        self._prev_texture = None
        self._wipe = 1.0          # 0 = old image fully covering, 1 = wipe done

        self._path = None         # wallpaper we want to be showing
        self._applied_path = None # wallpaper the current texture came from
        self._wipe_next = False   # wipe the next image swap?

        self._position = 0.0      # workspace position, 0 .. 1
        self._pan = 0.0           # current offset, logical px
        self._pan_target = 0.0
        self._velocity = 0.0

        self._tick_id = None
        self._last_frame_us = None
        self._snapshotted = False
        self._dbg_samples = []

    # -- geometry ----------------------------------------------------------

    @property
    def wanted_travel(self):
        steps = max(CONFIG["workspaces"] - 1, 1)
        return CONFIG["pan_per_ws"] * steps

    def _cover(self, texture, width, height):
        """Pure cover fit: the smallest scale that fills the screen.

        No extra zoom is applied, so nothing is cropped beyond what covering a
        1.6:1 screen with this image inevitably costs.
        """
        tw, th = texture.get_width(), texture.get_height()
        if tw <= 0 or th <= 0 or width <= 0 or height <= 0:
            return None
        scale = max(width / tw, height / th) * CONFIG["max_zoom"]
        return scale, tw * scale, th * scale

    def travel_for(self, texture, width, height):
        """How far we can actually pan without zooming in past cover fit.

        A 21:9 panorama has thousands of spare pixels; a 16:9 image has only a
        few hundred. We use whatever is there rather than zooming to invent
        more, so the image is never cropped harder than cover fit requires.
        """
        if texture is None:
            return 0.0
        fit = self._cover(texture, width, height)
        if fit is None:
            return 0.0
        _, dw, _ = fit
        return min(self.wanted_travel, max(dw - width, 0.0))

    def _draw_rect(self, texture, width, height):
        """Where to blit `texture` so it covers the widget at the current pan."""
        fit = self._cover(texture, width, height)
        if fit is None:
            return None
        _, dw, dh = fit

        slack = max(dw - width, 0.0)
        # pan runs -travel/2 .. +travel/2; 0 is the centre of the image.
        x = -slack / 2.0 - self._pan
        x = min(0.0, max(width - dw, x))
        y = -(dh - height) / 2.0
        return Graphene.Rect.alloc().init(x, y, dw, dh)

    def do_snapshot(self, snapshot):
        width, height = self.get_width(), self.get_height()
        if not self._snapshotted:
            self._snapshotted = True
            dlog("first snapshot", width, height, "texture:", self._texture)
        if width <= 0 or height <= 0:
            return

        bounds = Graphene.Rect.alloc().init(0, 0, width, height)
        snapshot.push_clip(bounds)

        wiping = self._prev_texture is not None and self._wipe < 1.0

        # The outgoing image stays put; the new one is revealed over it by a
        # hard edge travelling left to right. No dissolve, no fade.
        if wiping:
            rect = self._draw_rect(self._prev_texture, width, height)
            if rect is not None:
                snapshot.append_scaled_texture(
                    self._prev_texture, Gsk.ScalingFilter.TRILINEAR, rect
                )

        if self._texture is not None:
            rect = self._draw_rect(self._texture, width, height)
            if rect is not None:
                if wiping:
                    edge = width * smoothstep(self._wipe)
                    snapshot.push_clip(
                        Graphene.Rect.alloc().init(0, 0, edge, height)
                    )
                snapshot.append_scaled_texture(
                    self._texture, Gsk.ScalingFilter.TRILINEAR, rect
                )
                if wiping:
                    snapshot.pop()

        snapshot.pop()

    # -- state changes -----------------------------------------------------

    def set_workspace(self, workspace_id, animate=True):
        n = CONFIG["workspaces"]
        wid = workspace_id
        if wid < 1:
            wid = 1
        elif wid > n:
            wid = n
        self._position = (wid - 1) / max(n - 1, 1)        # 0 .. 1
        self._update_target(animate=animate)

    def _update_target(self, animate=True):
        """Recompute the pan target. Travel depends on the current image."""
        travel = self.travel_for(self._texture, self.get_width(), self.get_height())
        target = (self._position - 0.5) * travel
        if animate and abs(target - self._pan_target) < 0.01:
            return
        self._pan_target = target
        if animate:
            self._start_ticking()
        else:
            self._pan = target
            self._velocity = 0.0
            self.queue_draw()

    def set_image(self, path, animate=True):
        """Remember which wallpaper to show; load it as soon as we have a size."""
        self._path = os.path.realpath(os.path.expanduser(path))
        self._wipe_next = animate
        return self._ensure_texture()

    def do_size_allocate(self, width, height, baseline):
        dlog("size_allocate", width, height)
        # The texture is loaded at the size it will be drawn at, which we only
        # learn here -- so (re)load whenever the surface is sized.
        self._ensure_texture(width, height)

    def _ensure_texture(self, width=None, height=None):
        if not self._path:
            dlog("ensure_texture: no path yet")
            return False
        if width is None:
            width, height = self.get_width(), self.get_height()
        if width <= 0 or height <= 0:
            dlog("ensure_texture: not allocated", width, height)
            return False      # not allocated yet; do_size_allocate retries

        scale = self.get_scale_factor() or 1
        # Cover size is exactly what we draw, so a 7680px panorama doesn't sit
        # in VRAM at full size.
        target_w = int(width * CONFIG["max_zoom"] * scale)
        target_h = int(height * CONFIG["max_zoom"] * scale)

        texture = self._loader.load(self._path, target_w, target_h)
        if texture is None:
            return False
        if texture is self._texture:
            self._update_target(animate=False)
            return True       # same image, same size: nothing to do

        new_image = self._path != self._applied_path
        if new_image and self._wipe_next and self._texture is not None:
            self._prev_texture = self._texture
            self._wipe = 0.0
        else:
            self._prev_texture = None
            self._wipe = 1.0

        self._texture = texture
        self._applied_path = self._path
        self._wipe_next = True

        # A new image can afford a different amount of travel.
        self._update_target(animate=False)

        if self._wipe < 1.0:
            self._start_ticking()
        else:
            self.queue_draw()
        return True

    # -- animation ---------------------------------------------------------

    def _start_ticking(self):
        if self._tick_id is None:
            self._last_frame_us = None
            self._dbg_samples = []
            self._tick_id = self.add_tick_callback(self._on_tick)

    def _on_tick(self, _widget, frame_clock):
        now = frame_clock.get_frame_time()
        if self._last_frame_us is None:
            self._last_frame_us = now
            return GLib.SOURCE_CONTINUE
        dt = (now - self._last_frame_us) / 1_000_000.0
        self._last_frame_us = now
        # A stall (vt switch, suspend) shouldn't make the spring explode.
        dt = min(dt, 1.0 / 30.0)

        moving = self._step_spring(dt)
        wiping = self._step_wipe(dt)
        self.queue_draw()

        if DEBUG:
            self._dbg_samples.append((dt, self._pan))

        if moving or wiping:
            return GLib.SOURCE_CONTINUE

        if DEBUG and self._dbg_samples:
            total = sum(s[0] for s in self._dbg_samples)
            n = len(self._dbg_samples)
            track = " ".join(f"{p:.0f}" for _, p in self._dbg_samples[::4])
            dlog(
                f"animation: {n} frames in {total*1000:.0f}ms "
                f"({n/total:.0f} fps) pan track: {track}"
            )

        self._tick_id = None
        self._last_frame_us = None
        return GLib.SOURCE_REMOVE

    def _step_spring(self, dt):
        k = CONFIG["stiffness"]
        c = 2.0 * math.sqrt(k) * CONFIG["damping_ratio"]

        displacement = self._pan - self._pan_target
        # Sub-pixel residue isn't visible, so stop the frame clock rather than
        # chasing the asymptote and redrawing forever.
        if abs(displacement) < 0.5 and abs(self._velocity) < 10.0:
            self._pan = self._pan_target
            self._velocity = 0.0
            return False

        # Semi-implicit Euler, substepped so a long frame stays stable.
        substeps = max(1, int(dt / (1.0 / 240.0)))
        h = dt / substeps
        for _ in range(substeps):
            accel = -k * (self._pan - self._pan_target) - c * self._velocity
            self._velocity += accel * h
            self._pan += self._velocity * h
        return True

    def _step_wipe(self, dt):
        if self._prev_texture is None or self._wipe >= 1.0:
            return False
        duration = max(CONFIG["wipe_duration"], 0.01)
        self._wipe = min(1.0, self._wipe + dt / duration)
        if self._wipe >= 1.0:
            self._prev_texture = None
            return False
        return True


# ------------------------------------------------------------ texture cache --

class TextureLoader:
    """Loads images downscaled to roughly the size they'll be drawn at."""

    def __init__(self):
        self._cache = {}

    def load(self, path, target_w, target_h):
        path = os.path.realpath(os.path.expanduser(path))
        key = (path, target_w // 64, target_h // 64)
        if key in self._cache:
            return self._cache[key]

        try:
            fmt, src_w, src_h = GdkPixbuf.Pixbuf.get_file_info(path)[0:3]
        except Exception as exc:  # unreadable / not an image
            log("cannot inspect", path, exc)
            return None
        if not fmt or not src_w or not src_h:
            log("not a loadable image:", path)
            return None

        # Cover the requested box, but never load bigger than the source --
        # any upscaling is cheaper done by the GPU at draw time.
        scale = min(max(target_w / src_w, target_h / src_h), 1.0)
        out_w = max(1, int(round(src_w * scale)))
        out_h = max(1, int(round(src_h * scale)))
        # Stay inside the usual 8192px GL texture limit.
        if out_w > 8192 or out_h > 8192:
            shrink = min(8192 / out_w, 8192 / out_h)
            out_w = max(1, int(out_w * shrink))
            out_h = max(1, int(out_h * shrink))

        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                path, out_w, out_h, False
            )
            fmt = (
                Gdk.MemoryFormat.R8G8B8A8
                if pixbuf.get_has_alpha()
                else Gdk.MemoryFormat.R8G8B8
            )
            texture = Gdk.MemoryTexture.new(
                pixbuf.get_width(),
                pixbuf.get_height(),
                fmt,
                GLib.Bytes.new(pixbuf.get_pixels()),
                pixbuf.get_rowstride(),
            )
        except Exception as exc:
            log("cannot load", path, exc)
            return None

        # Keep a couple of entries so multi-monitor re-allocations and the
        # outgoing image of a wipe don't force a redecode.
        while len(self._cache) >= 4:
            self._cache.pop(next(iter(self._cache)))
        self._cache[key] = texture
        log(f"loaded {os.path.basename(path)} {src_w}x{src_h} -> {out_w}x{out_h}")
        return texture


# -------------------------------------------------------------------- app ----

class ParallaxApp:
    def __init__(self):
        self.app = Gtk.Application(
            application_id="dev.luminara.WallpaperParallax",
            flags=Gio.ApplicationFlags.NON_UNIQUE,
        )
        self.app.connect("activate", self.on_activate)
        self.loader = TextureLoader()
        self.windows = {}          # connector -> (window, surface)
        self.image_path = None
        self.hold = None
        self.event_stream = None
        self.control_service = None
        self.control_path = None

    # -- lifecycle ---------------------------------------------------------

    def run(self):
        return self.app.run([])

    def on_activate(self, app):
        # Claim the control socket before building anything, so a second copy
        # bows out without ever putting a surface on screen.
        if not self.start_control_socket():
            app.quit()
            return

        self.hold = app.hold()
        self.image_path = self.initial_image()

        display = Gdk.Display.get_default()
        if display is None:
            log("no wayland display")
            app.quit()
            return

        monitors = display.get_monitors()
        monitors.connect("items-changed", lambda *_: self.sync_monitors())
        self.sync_monitors()

        self.connect_events()
        self.refresh_workspaces(animate=False)

    def initial_image(self):
        try:
            with open(STATE_FILE) as fh:
                saved = fh.read().strip()
            if saved and os.path.exists(saved):
                return saved
        except OSError:
            pass
        for candidate in FALLBACK_WALLPAPERS:
            if os.path.exists(candidate):
                return os.path.realpath(candidate)
        return None

    def save_state(self):
        if not self.image_path:
            return
        try:
            os.makedirs(STATE_DIR, exist_ok=True)
            with open(STATE_FILE, "w") as fh:
                fh.write(self.image_path + "\n")
        except OSError as exc:
            log("cannot save state:", exc)

    # -- surfaces ----------------------------------------------------------

    def sync_monitors(self):
        display = Gdk.Display.get_default()
        if display is None:
            return
        live = {}
        monitors = display.get_monitors()
        for i in range(monitors.get_n_items()):
            monitor = monitors.get_item(i)
            name = monitor.get_connector() or f"monitor-{i}"
            live[name] = monitor
            if name not in self.windows:
                self.create_window(name, monitor)

        for name in list(self.windows):
            if name not in live:
                window, _ = self.windows.pop(name)
                window.destroy()

    def create_window(self, name, monitor):
        window = Gtk.Window(application=self.app)
        window.set_decorated(False)

        LayerShell.init_for_window(window)
        # `bottom` keeps us above anything swww/awww painted on `background`
        # while staying under every ordinary window.
        LayerShell.set_layer(window, LayerShell.Layer.BOTTOM)
        LayerShell.set_namespace(window, "wallpaper-parallax")
        LayerShell.set_monitor(window, monitor)
        LayerShell.set_keyboard_mode(window, LayerShell.KeyboardMode.NONE)
        for edge in (
            LayerShell.Edge.TOP,
            LayerShell.Edge.BOTTOM,
            LayerShell.Edge.LEFT,
            LayerShell.Edge.RIGHT,
        ):
            LayerShell.set_anchor(window, edge, True)
        # Don't let panels reserve space away from us, and don't reserve any.
        LayerShell.set_exclusive_zone(window, -1)

        surface = ParallaxSurface(self.loader)
        if self.image_path:
            # Records the path; the texture itself is loaded once the
            # compositor has told us how big the surface is.
            surface.set_image(self.image_path, animate=False)
        window.set_child(surface)
        window.present()

        self.windows[name] = (window, surface)
        surface.connect("map", lambda *_: self.refresh_workspaces(animate=False))
        log("surface created for", name)

    # -- hyprland events ---------------------------------------------------

    def connect_events(self):
        sock_dir = hypr_socket_dir()
        if not sock_dir:
            log("no hyprland socket directory; parallax will not react")
            return
        path = os.path.join(sock_dir, ".socket2.sock")
        try:
            client = Gio.SocketClient.new()
            conn = client.connect(Gio.UnixSocketAddress.new(path), None)
        except GLib.Error as exc:
            log("cannot connect to event socket:", exc.message)
            return
        self.event_stream = Gio.DataInputStream.new(conn.get_input_stream())
        self._read_event()
        log("listening on", path)

    def _read_event(self):
        self.event_stream.read_line_async(
            GLib.PRIORITY_DEFAULT, None, self._on_event_line
        )

    def _on_event_line(self, stream, result):
        try:
            line, _ = stream.read_line_finish_utf8(result)
        except GLib.Error as exc:
            log("event socket error:", exc.message)
            return
        if line is None:
            log("event socket closed")
            return

        name = line.split(">>", 1)[0]
        if name in (
            "workspace",
            "workspacev2",
            "focusedmon",
            "focusedmonv2",
            "moveworkspace",
            "moveworkspacev2",
            "createworkspace",
            "createworkspacev2",
            "destroyworkspace",
            "destroyworkspacev2",
            "monitoradded",
            "monitoraddedv2",
            "monitorremoved",
        ):
            self.refresh_workspaces()

        self._read_event()

    def refresh_workspaces(self, animate=True):
        mapping = active_workspace_per_monitor()
        if not mapping:
            return False
        for name, (_, surface) in self.windows.items():
            if name in mapping:
                surface.set_workspace(mapping[name], animate=animate)
            elif len(mapping) == 1:
                # Single-output setups where the connector names disagree.
                surface.set_workspace(next(iter(mapping.values())), animate=animate)
        return False

    # -- control socket ----------------------------------------------------

    def start_control_socket(self):
        """Bind the control socket. False means another daemon owns it."""
        path = control_socket_path()
        if os.path.exists(path):
            if daemon_alive():
                log("another parallax daemon is already running; exiting")
                return False
            # Socket left behind by a crashed daemon -- reclaim it.
            try:
                os.unlink(path)
            except OSError as exc:
                log("cannot remove stale socket:", exc)
                return False

        service = Gio.SocketService.new()
        try:
            service.add_address(
                Gio.UnixSocketAddress.new(path),
                Gio.SocketType.STREAM,
                Gio.SocketProtocol.DEFAULT,
                None,
            )
        except GLib.Error as exc:
            log("cannot bind control socket:", exc.message)
            return False
        service.connect("incoming", self.on_control_connection)
        service.start()
        self.control_service = service
        self.control_path = path

        atexit.register(self.release_control_socket)
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
            unix_signal_add(GLib.PRIORITY_DEFAULT, sig, self.on_signal)

        log("control socket at", path)
        return True

    def on_signal(self):
        log("shutting down")
        self.app.quit()
        return GLib.SOURCE_REMOVE

    def release_control_socket(self):
        if not self.control_path:
            return
        if self.control_service is not None:
            self.control_service.stop()
            self.control_service = None
        try:
            os.unlink(self.control_path)
        except OSError:
            pass
        self.control_path = None

    def on_control_connection(self, _service, connection, _source):
        stream = Gio.DataInputStream.new(connection.get_input_stream())

        def done(st, result):
            try:
                line, _ = st.read_line_finish_utf8(result)
            except GLib.Error:
                return
            if line:
                self.handle_command(line.strip())

        stream.read_line_async(GLib.PRIORITY_DEFAULT, None, done)
        return True

    def handle_command(self, line):
        parts = line.split(" ", 1)
        cmd = parts[0]
        arg = parts[1].strip() if len(parts) > 1 else ""

        if cmd == "img" and arg:
            path = os.path.realpath(os.path.expanduser(arg))
            if not os.path.exists(path):
                log("no such image:", path)
                return
            changed = False
            for _, surface in self.windows.values():
                if surface.set_image(path, animate=True):
                    changed = True
            if changed:
                self.image_path = path
                self.save_state()
        elif cmd == "reload":
            if self.image_path:
                for _, surface in self.windows.values():
                    surface.set_image(self.image_path, animate=False)
            self.refresh_workspaces(animate=False)
        elif cmd == "quit":
            self.app.quit()


# -------------------------------------------------------------------- cli ----

def daemon_alive():
    """True if something is actually listening on the control socket."""
    path = control_socket_path()
    if not os.path.exists(path):
        return False
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.connect(path)
        return True
    except OSError:
        return False


def send_command(command):
    path = control_socket_path()
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.settimeout(2.0)
            s.connect(path)
            s.sendall((command + "\n").encode())
        return 0
    except OSError as exc:
        print(f"parallax daemon not reachable ({exc})", file=sys.stderr)
        return 1


def main(argv):
    if len(argv) > 1:
        flag = argv[1]
        if flag == "--set":
            if len(argv) < 3:
                print("usage: wallpaper-parallax.py --set <image>", file=sys.stderr)
                return 2
            return send_command("img " + os.path.abspath(os.path.expanduser(argv[2])))
        if flag == "--reload":
            return send_command("reload")
        if flag == "--quit":
            return send_command("quit")
        if flag in ("-h", "--help"):
            print(__doc__)
            return 0
        print(f"unknown option {flag}", file=sys.stderr)
        return 2

    return ParallaxApp().run()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
