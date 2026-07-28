#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("GtkLayerShell", "0.1")
from gi.repository import Gtk, GtkLayerShell, GLib, GdkPixbuf
from datetime import datetime
import sys, os

win = Gtk.Window()
GtkLayerShell.init_for_window(win)
GtkLayerShell.set_layer(win, GtkLayerShell.Layer.OVERLAY)
GtkLayerShell.set_exclusive_zone(win, -1)
for edge in (GtkLayerShell.Edge.TOP, GtkLayerShell.Edge.BOTTOM,
             GtkLayerShell.Edge.LEFT, GtkLayerShell.Edge.RIGHT):
    GtkLayerShell.set_anchor(win, edge, True)
GtkLayerShell.set_keyboard_mode(win, GtkLayerShell.KeyboardMode.EXCLUSIVE)

win.set_app_paintable(True)
screen = win.get_screen()
visual = screen.get_rgba_visual()
if visual:
    win.set_visual(visual)

overlay = Gtk.Overlay()
win.add(overlay)

# --- Background: DrawingArea + cairo, always scales to real allocation ---
bg_path = os.path.expanduser("~/Pictures/hyprlock.jpg")
pixbuf = GdkPixbuf.Pixbuf.new_from_file(bg_path)

drawing_area = Gtk.DrawingArea()
drawing_area.set_hexpand(True)
drawing_area.set_vexpand(True)

def on_draw(widget, cr):
    aw = widget.get_allocated_width()
    ah = widget.get_allocated_height()
    pw, ph = pixbuf.get_width(), pixbuf.get_height()
    # cover-fit scaling (fills screen, crops overflow, no distortion)
    scale = max(aw / pw, ah / ph)
    sw, sh = pw * scale, ph * scale
    ox, oy = (aw - sw) / 2, (ah - sh) / 2
    cr.save()
    cr.translate(ox, oy)
    cr.scale(scale, scale)
    Gtk_gdk_ctx = cr
    from gi.repository import Gdk
    Gdk.cairo_set_source_pixbuf(cr, pixbuf, 0, 0)
    cr.paint()
    cr.restore()
    return False

drawing_area.connect("draw", on_draw)
overlay.add(drawing_area)

hour = Gtk.Label()
minute = Gtk.Label()
for lbl, name in ((hour, "hour"), (minute, "minute")):
    lbl.set_name(name)
    lbl.set_halign(Gtk.Align.CENTER)

box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
box.set_halign(Gtk.Align.CENTER)
box.set_valign(Gtk.Align.CENTER)
box.pack_start(hour, False, False, 0)
box.pack_start(minute, False, False, 0)
overlay.add_overlay(box)

css = Gtk.CssProvider()
css.load_from_data(b"""
#hour, #minute {
  font-family: Poppins;
  font-size: 150px;
  color: #F0CDA0;
}
#hour {
  margin-bottom: -20px;
}

#minute {
  margin-top: -20px;
}
""")
Gtk.StyleContext.add_provider_for_screen(
    screen, css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

def tick():
    now = datetime.now()
    hour.set_text(now.strftime("%I"))
    minute.set_text(now.strftime("%M"))
    return True

tick()
GLib.timeout_add(1000, tick)

def quit_on_input(*args):
    Gtk.main_quit()

win.connect("key-press-event", quit_on_input)
win.connect("button-press-event", quit_on_input)

win.show_all()
Gtk.main()
sys.exit(0)
