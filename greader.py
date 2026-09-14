import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Poppler", "0.18")


from gi.repository import Gtk, Poppler


import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()
filename = args.file
print(f"{filename=}")
doc = Poppler.Document.new_from_file(filename, None)
print(f"{doc.get_n_pages()=}")
