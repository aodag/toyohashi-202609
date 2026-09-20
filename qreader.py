import sys
from PyQt6 import QtWidgets, QtPdf, QtCore, QtGui


class QReaderView(QtWidgets.QWidget):

    _image = None
    _document = None
    _page = -1

    def __init__(self, parent=None, document=None):
        super().__init__(parent=parent)
        self.document = document
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

    def renderImage(self):
        if not self.document:
            return None
        return doc.render(self.page, self.document.pagePointSize(self.page).toSize())

    @QtCore.pyqtProperty(int)
    def page(self):
        return self._page

    @page.setter
    def page(self, p):
        if not self._document:
            return
        if p < 0:
            return
        if p > self._document.pageCount() - 1:
            return
        if self._page == p:
            return
        self._page = p
        self.image = self.renderImage()

    def setPage(self, p):
        self.page = p

    def next(self):
        self.page += 1

    def prev(self):
        self.page -= 1

    @QtCore.pyqtProperty(QtPdf.QPdfDocument)
    def document(self):
        return self._document

    @document.setter
    def document(self, d):
        self._document = d
        self.page = 0

    @QtCore.pyqtProperty(QtGui.QImage)
    def image(self):
        return self._image

    @image.setter
    def image(self, i):
        self._image = i
        self.repaint()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(QtCore.QRect(QtCore.QPoint(0, 0), self.size()), QtGui.QColorConstants.DarkGray)
        if self.image:
            im = self.image.scaled(
                self.width(), self.height(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            painter.drawImage(0, 0, im)

app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QWidget()
layout = QtWidgets.QVBoxLayout(widget)
doc = QtPdf.QPdfDocument(app)
doc.load(sys.argv[1])
view = QReaderView(widget, doc)
nextButton = QtWidgets.QPushButton("next", widget)
nextButton.clicked.connect(view.next)
prevButton = QtWidgets.QPushButton("prev", widget)
prevButton.clicked.connect(view.prev)
layout.addWidget(view)
layout.addWidget(nextButton)
layout.addWidget(prevButton)
widget.show()
app.exec()
