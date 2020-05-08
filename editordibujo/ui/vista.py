import random as rnd

from PyQt5 import uic
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QColor, QPainter, QPaintEvent
from PyQt5.QtWidgets import QMainWindow, QWidget, QFrame

from editordibujo.dibujo.modelo import Dibujo, Rectangulo, Linea, Ovalo


class Canvas(QWidget):
    def __init__(self, main_window):
        QWidget.__init__(self)
        self.main_window = main_window
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

    def paintEvent(self, e: QPaintEvent) -> None:
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        self.main_window.dibujar(qp)
        qp.end()


class MainWindowEditorDibujo(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("../designer/MainWindowEditorDibujo.ui", self)
        self.dibujo = Dibujo()
        self.canvas = Canvas(self)
        self.canvas_container.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.canvas_container.layout().addWidget(self.canvas)
        self.pbutton_linea.clicked.connect(self.agregar_linea)
        self.pbutton_rect.clicked.connect(self.agregar_rectangulo)
        self.pbutton_ovalo.clicked.connect(self.agregar_ovalo)

    def agregar_rectangulo(self):
        x1 = rnd.randint(0, self.canvas.width())
        y1 = rnd.randint(0, self.canvas.height())
        x2 = rnd.randint(0, self.canvas.width())
        y2 = rnd.randint(0, self.canvas.height())
        p1 = QPoint(x1, y1)
        p2 = QPoint(x2, y2)
        color = QColor(rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0, 255))
        fondo = QColor(rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0, 255))
        rect = Rectangulo(p1, p2, color, Qt.SolidLine, 2, fondo)
        self.dibujo.agregar_figura(rect)
        self.canvas.repaint()

    def agregar_ovalo(self):
        x1 = rnd.randint(0, self.canvas.width())
        y1 = rnd.randint(0, self.canvas.height())
        x2 = rnd.randint(0, self.canvas.width())
        y2 = rnd.randint(0, self.canvas.height())
        p1 = QPoint(x1, y1)
        p2 = QPoint(x2, y2)
        color = QColor(rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0, 255))
        fondo = QColor(rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0, 255))
        oval = Ovalo(p1, p2, color, Qt.SolidLine, 2, fondo)
        self.dibujo.agregar_figura(oval)
        self.canvas.repaint()

    def agregar_linea(self):
        x1 = rnd.randint(0, self.canvas.width())
        y1 = rnd.randint(0, self.canvas.height())
        x2 = rnd.randint(0, self.canvas.width())
        y2 = rnd.randint(0, self.canvas.height())
        p1 = QPoint(x1, y1)
        p2 = QPoint(x2, y2)
        color = QColor(rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0, 255))
        linea = Linea(p1, p2, color, Qt.SolidLine, 2)
        self.dibujo.agregar_figura(linea)
        self.canvas.repaint()

    def dibujar(self, qp: QPainter):
        self.dibujo.dibujar(qp)
