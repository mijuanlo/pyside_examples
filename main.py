# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QDialog, QLineEdit, QVBoxLayout
from PySide2.QtCore import qDebug,Signal, Slot, QFile
from PySide2.QtUiTools import QUiLoader

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

    @Slot()
    def testslot(self):
        qDebug('test ending')
        sys.exit(1)

class Form(QDialog):
    def __init__(self,parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("My Form")

# Form implementation generated from reading ui file 'mainwindow.ui',
# licensing of 'mainwindow.ui' applies.
#
# Created: Tue Oct 15 10:11:41 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindowUI")
        MainWindow.resize(800, 600)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))


class MainWindow2(QMainWindow):
    def __init__(self):
        super(MainWindow2, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

from PySide2.QtGui import QPdfWriter,QPainter,QPagedPaintDevice,QFont
from PySide2.QtGui import QTextDocument 
from PySide2.QtPrintSupport import QPrinter
from PySide2.QtWidgets import QTextEdit
from PySide2.QtCore import QSizeF,QRectF,Qt
textMargins = 12
borderMargins = 10
doPageFooter = False
def mmToPixels(printer, mm):
    return mm * 0.039370147 * printer.resolution()

def paintPage(currentPage, totalpages, painter, doc, textrect, footerheight):
    painter.save()
    pagesize = QRectF(0,currentPage * doc.pageSize().height(),doc.pageSize().width(), doc.pageSize().height())
    painter.setClipRect(textrect)
    painter.translate(0,-pagesize.top())
    painter.translate(textrect.left(),textrect.top())
    doc.drawContents(painter)
    painter.restore()
    footerrect = QRectF(textrect)
    footerrect.setTop(textrect.bottom())
    footerrect.setHeight(footerheight)
    if doPageFooter:
        painter.drawText(footerrect,Qt.AlignVCenter|Qt.AlignRight,"Page {} of {}".format(currentPage+1,totalpages))

def customPrint(printer, doc):
    painter = QPainter(printer)
    doc.documentLayout().setPaintDevice(printer)
    doc.setPageSize(printer.pageRect().size())
    pageSize = printer.pageRect().size()
    tm = mmToPixels(printer,textMargins)
    footHeight = painter.fontMetrics().height()
    textRect = QRectF(tm,tm,pageSize.width() - 2 * tm, pageSize.height()-2*tm - footHeight)
    doc.setPageSize(textRect.size())
    pagecount=doc.pageCount()
    for index in range(pagecount):
        if index != 0:
            printer.newPage()
        paintPage(index, pagecount, painter, doc, textRect, footHeight)

if __name__ == "__main__":
    from PySide2.QtCore import Qt
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    window = MainWindow()
    window.show()

    label = QLabel("<font color=red size=40>Hello</font>")
    label.show()

    button = QPushButton("Exit button")
    button.clicked.connect(window.testslot)
    button.show()

    form = Form()
    form.show()

    editor = QLineEdit("Write something...")

    layout = QVBoxLayout()
    layout.addWidget(editor)
    form.setLayout(layout)

    window2 = MainWindow2()
    window2.show()

    ui_file= QFile("mainwindow2.ui")
    ui_file.open(QFile.ReadOnly)
    loader = QUiLoader()
    window3 = loader.load(ui_file)
    ui_file.close()
    window3.show()

    from PySide2.QtGui import QPdfWriter,QPainter,QPagedPaintDevice,QFont
    from PySide2.QtCore import QMargins, QRect, Qt

    qpdf_writer = QPdfWriter("file.pdf")
    qpdf_writer.setPageSize(QPagedPaintDevice.A4)
    qpdf_writer.setPageMargins(QMargins(20,20,20,20))

    painter = QPainter(qpdf_writer)
    painter.setPen(Qt.black)
    painter.setFont(QFont("Times",10))

    rect = painter.viewport()

    painter.drawText(rect,Qt.AlignCenter,"QTEXAMPLE")
    painter.end()

    from PySide2.QtGui import QTextDocument 
    from PySide2.QtPrintSupport import QPrinter
    from PySide2.QtWidgets import QTextEdit

    html = "<body><div align=center> Center </div>"
    html += "<div align=left> Left </div>"
    html += "<h1 align=center> Center title </h1>"
    html += "<p align=justify class=\"test1\"> {} </p>".format("Loren ipsum "*1000)
    html += "<div align=right> End document </div></body>"

    document = QTextDocument()
    with open("style.css","r") as fp:
        document.setDefaultStyleSheet(fp.read())
    document.setHtml(html)
    
    printer = QPrinter(QPrinter.PrinterResolution)
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setPaperSize(QPrinter.A4)
    printer.setOutputFileName("file2.pdf")
    printer.setPageMargins(QMargins(10,10,10,10))
    document.print_(printer)

    from PySide2.QtPrintSupport import QPrintPreviewWidget
    
    '''
    txtview = QTextEdit()
    txtview.setDocument(document)
    txtview.show()
    '''

    printer = QPrinter(QPrinter.HighResolution)
    printer.setPageSize(QPrinter.A4)
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setOutputFileName("file3.pdf")
    customPrint(printer,document)
    
    
    preview = QPrintPreviewWidget(printer)
    preview.setWindowFlags(Qt.Window)
    #preview.setViewMode(QPrintPreviewWidget.AllPagesView)
    #preview.setViewMode(QPrintPreviewWidget.FacingPagesView)
    #preview.setViewMode(QPrintPreviewWidget.SinglePageView)
    preview.setSinglePageViewMode()
    #preview.setZoomMode(QPrintPreviewWidget.FitInView)
    preview.fitInView()
    preview.paintRequested.connect(document.print_)
    preview.show()
    preview.resize(600,800)

    sys.exit(app.exec_())

