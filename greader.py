import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Poppler", "0.18")


from gi.repository import Gtk, Poppler


print(f"{Gtk=}, {Poppler=}")
