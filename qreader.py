import sys
from PyQt6 import QtWidgets, QtPdf, QtPdfWidgets, QtCore

app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QWidget()
layout = QtWidgets.QVBoxLayout(widget)
doc = QtPdf.QPdfDocument(app)
doc.load(sys.argv[1])
selector = QtPdfWidgets.QPdfPageSelector(None)
selector.setDocument(doc)
view = QtPdfWidgets.QPdfView(None)
view.setDocument(doc)
selector.currentPageChanged.connect(lambda page: view.pageNavigator().jump(page, QtCore.QPointF(0, 0)))
layout.addWidget(selector)
layout.addWidget(view)
widget.show()
app.exec()
