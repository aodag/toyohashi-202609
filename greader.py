import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Poppler", "0.18")


from gi.repository import Gio, GLib, GObject, Gtk, Poppler


class GReaderModel(GObject.Object):
    current_page = GObject.Property(nick="current-page", type=Poppler.Page)

    def do_constructed(self):
        self.pages = Gio.ListStore.new(Poppler.Page)
        self.selection = Gtk.SingleSelection.new(self.pages)
        self.selection.bind_property("selected-item", self, "current-page")

    def open(self, files):
        for file in files:
            doc = Poppler.Document.new_from_gfile(file, None)
            for i in range(doc.get_n_pages()):
                page = doc.get_page(i)
                self.pages.append(page)

    def next(self):
        selected = self.selection.get_selected()
        next = min(selected + 1, self.selection.get_n_items() - 1)
        self.selection.set_selected(next)

    def prev(self):
        selected = self.selection.get_selected()
        prev = max(0, selected - 1)
        self.selection.set_selected(prev)

    def render(self, cr):
        if not self.current_page:
            return
        self.current_page.render(cr)


class GReaderView(Gtk.DrawingArea):
    model = GObject.Property(type=GReaderModel, flags=GObject.ParamFlags.CONSTRUCT | GObject.ParamFlags.READWRITE)

    def do_constructed(self):
        self.signal_group = GObject.SignalGroup.new(GReaderModel)
        self.signal_group.connect_data("notify", lambda *args: self.queue_draw(), None, GObject.ConnectFlags.DEFAULT)
        self.bind_property("model", self.signal_group, "target", flags=GObject.BindingFlags.SYNC_CREATE)
        self.set_draw_func(lambda drawing_area, cr, width, height: self.model.render(cr))


class GReader(Gtk.Application):

    def do_open(self, files, n_files, hint):
        model = GReaderModel()
        model.open(files)
        self._show(model)

    def _show(self, model):
        win = Gtk.ApplicationWindow(application=self)
        view = GReaderView(model=model)
        next_action = Gio.SimpleAction.new("next", None)
        next_action.connect("activate", lambda *args: model.next())
        prev_action = Gio.SimpleAction.new("prev", None)
        prev_action.connect("activate", lambda *args: model.prev())
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
        model = GReaderModel()
        self._show(model)


def main():
    app = GReader(application_id=None, flags=Gio.ApplicationFlags.HANDLES_OPEN)
    sys.exit(app.run(sys.argv))


if __name__ == "__main__":
    main()
