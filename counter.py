import sys
import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gio, GLib, GObject, Gtk


class CounterModel(GObject.Object):
    @GObject.Property(type=int, flags=GObject.ParamFlags.READABLE)
    def count(self):
        return self._count

    def do_constructed(self):
        self._count = 0

    def increment(self):
        self._count += 1
        self.notify("count")

    def decrement(self):
        self._count -= 1
        self.notify("count")


class CounterView(Gtk.Box):
    model = GObject.Property(type=CounterModel, flags=GObject.ParamFlags.CONSTRUCT_ONLY | GObject.ParamFlags.READWRITE)

    def do_constructed(self):
        super().do_constructed()

        self.count_label = Gtk.Label()
        self.increment_button = Gtk.Button(label="inc")
        self.decrement_button = Gtk.Button(label="decr")

        self.model.bind_property("count", self.count_label, "label", GObject.BindingFlags.SYNC_CREATE)
        self.increment_button.connect("clicked", lambda *args: self.model.increment())
        self.decrement_button.connect("clicked", lambda *args: self.model.decrement())

        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.append(self.count_label)
        self.buttons_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.buttons_box.append(self.increment_button)
        self.buttons_box.append(self.decrement_button)
        self.append(self.buttons_box)


class Counter(Gtk.Application):
    def do_activate(self):
        model = CounterModel()
        view = CounterView(model=model)
        win = Gtk.ApplicationWindow(application=self)
        win.set_child(view)
        win.present()


def main():
    counter = Counter()
    counter.run(sys.argv)


if __name__ == "__main__":
    main()
