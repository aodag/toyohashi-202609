import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Poppler", "0.18")


from gi.repository import GLib, Gtk, Poppler


import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()
filename = args.file
print(f"{filename=}")
doc = Poppler.Document.new_from_file(filename, None)
print(f"{doc.get_n_pages()=}")
pages = [doc.get_page(i) for i in range(doc.get_n_pages())]
if not pages:
    print("no pages")
    sys.exit(1)
win = Gtk.Window()
view = Gtk.DrawingArea()
view.set_draw_func(lambda drawing_area, cr, width, height: pages[1].render(cr))
win.set_child(view)
win.present()
loop = GLib.MainLoop()
win.connect("close-request", lambda *args: loop.quit())
loop.run()
