import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Poppler", "0.18")


from gi.repository import Gio, GLib, Gtk, Poppler


import argparse


class GReader(Gtk.Application):

    def do_open(self, files, n_files, hint):
        self._show(files)

    def _show(self, files):
        if not files:
            print("no files")
            self.quit()
            return
        pages = Gio.ListStore.new(Poppler.Page)
        for file in files:
            doc = Poppler.Document.new_from_gfile(file, None)
            for i in range(doc.get_n_pages()):
                page = doc.get_page(i)
                pages.append(page)
        if not pages:
            print("no pages")
            sys.exit(1)
        selection = Gtk.SingleSelection.new(pages)
        win = Gtk.ApplicationWindow(application=self)
        view = Gtk.DrawingArea()
        view.set_draw_func(lambda drawing_area, cr, width, height: selection.get_selected_item().render(cr))
        selection.connect("selection-changed", lambda *args: view.queue_draw())
        next_action = Gio.SimpleAction.new("next", None)
        next_action.connect("activate", lambda *args: selection.set_selected(min(selection.get_selected() + 1, selection.get_n_items() - 1)))
        prev_action = Gio.SimpleAction.new("prev", None)
        prev_action.connect("activate", lambda *args: selection.set_selected(max(0, selection.get_selected() - 1)))
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", lambda *args: self.quit())
        self.add_action(next_action)
        self.add_action(prev_action)
        self.add_action(quit_action)
        self.set_accels_for_action("app.next", ["j"])
        self.set_accels_for_action("app.prev", ["k"])
        self.set_accels_for_action("app.quit", ["q"])
        win.set_child(view)
        win.present()

    def do_activate(self):
        self._show([])


def main():
    app = GReader(application_id=None, flags=Gio.ApplicationFlags.HANDLES_OPEN)
    sys.exit(app.run(sys.argv))


if __name__ == "__main__":
    main()
