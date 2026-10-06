#!/usr/bin/env python3
"""Native "Save as" dialog.

Prints the chosen path on stdout and exits 0; exits 1 if the dialog was
cancelled or failed. Used by screenshot.sh to ask where a capture should go.

Usage: save-dialog.py <initial-folder> <initial-filename> [title]
"""

import os
import sys

import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gio, GLib, Gtk  # noqa: E402

folder = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~")
name = sys.argv[2] if len(sys.argv) > 2 else "untitled"
title = sys.argv[3] if len(sys.argv) > 3 else "Save as"

chosen = {"path": None}


def on_activate(app):
    hold = app.hold()

    dialog = Gtk.FileDialog()
    dialog.set_title(title)
    dialog.set_initial_name(name)
    dialog.set_modal(True)
    if os.path.isdir(folder):
        dialog.set_initial_folder(Gio.File.new_for_path(folder))

    def done(dlg, result):
        try:
            gfile = dlg.save_finish(result)
            if gfile is not None:
                chosen["path"] = gfile.get_path()
        except GLib.Error:
            pass        # cancelled -- caller falls back to the default folder
        finally:
            del hold
            app.quit()

    dialog.save(None, None, done)


app = Gtk.Application(
    application_id="dev.luminara.SaveDialog",
    flags=Gio.ApplicationFlags.NON_UNIQUE,
)
app.connect("activate", on_activate)
app.run([])

if chosen["path"]:
    print(chosen["path"])
    sys.exit(0)
sys.exit(1)
