import editordibujo.ui.resources
import random as rnd

from PyQt5 import uic
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QColor, QPainter, QPaintEvent, QPalette
from PyQt5.QtWidgets import QMainWindow, QWidget, QFrame, QColorDialog

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

    SELECCIONAR = 1
    DIBUJAR = 2
    NINGUNA = 0

    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("../designer/MainWindowEditorDibujo.ui", self)
        self.dibujo = Dibujo()
        self.canvas = Canvas(self)
        self.x_seleccionado = -1
        self.y_seleccionado = -1
        self.configurar_ui()

    def configurar_ui(self):
        self.canvas_container.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.canvas_container.layout().addWidget(self.canvas)

        self.pbutton_linea.clicked.connect(self.agregar_linea)
        self.pbutton_rect.clicked.connect(self.agregar_rectangulo)
        self.pbutton_ovalo.clicked.connect(self.agregar_ovalo)

        pal_fondo = self.label_color_fondo.palette()
        pal_fondo.setColor(QPalette.Background, Qt.blue)
        self.label_color_fondo.setPalette(pal_fondo)
        pal_linea = self.label_color_linea.palette()
        pal_linea.setColor(QPalette.Background, Qt.black)
        self.label_color_linea.setPalette(pal_linea)
        self.label_color_fondo.mousePressEvent = self.seleccionar_color_fondo
        self.label_color_linea.mousePressEvent = self.seleccionar_color_linea

    def hacer_click(self, x: int, y: int):
        acc = self.accion()
        if acc == MainWindowEditorDibujo.SELECCIONAR:
            self.seleccionar(x, y)
        elif acc == MainWindowEditorDibujo.DIBUJAR:
            if self.x_seleccionado == -1 and self.y_seleccionado == -1:
                self.x_seleccionado = x
                self.y_seleccionado = y
            else:
                self.agregar_figura(self.x_seleccionado, self.y_seleccionado, x, y)
                self.x_seleccionado = -1
                self.y_seleccionado = -1

    def accion(self):
        if self.pbutton_seleccionar.isChecked():
            return MainWindowEditorDibujo.SELECCIONAR
        elif self.pbutton_linea.isChecked() or self.pbutton_rect.isChecked() or self.pbutton_ovalo.isChecked():
            return MainWindowEditorDibujo.DIBUJAR
        else:
            return MainWindowEditorDibujo.NINGUNA

    def tipo_linea(self):
        index = self.combo_tipo_linea.currentIndex()
        if index == 0:
            return Qt.SolidLine
        elif index == 1:
            return Qt.DashLine
        else:
            return Qt.DotLine

    def seleccionar(self, x: int, y: int):
        pass

    def seleccionar_color_fondo(self, event):
        pal = self.label_color_fondo.palette()
        color = QColorDialog.getColor(pal.color(QPalette.Background))
        pal.setColor(QPalette.Background, color)
        self.label_color_fondo.setPalette(pal)

    def seleccionar_color_linea(self, event):
        pal = self.label_color_linea.palette()
        color = QColorDialog.getColor(pal.color(QPalette.Background))
        pal.setColor(QPalette.Background, color)
        self.label_color_linea.setPalette(pal)

    def agregar_figura(self, x1: int, y1: int, x2: int, y2: int):
        pass

    def agregar_rectangulo(self):
        x1 = rnd.randint(0, self.canvas.width())
        y1 = rnd.randint(0, self.canvas.height())
        x2 = rnd.randint(0, self.canvas.width())
        y2 = rnd.randint(0, self.canvas.height())
        p1 = QPoint(x1, y1)
        p2 = QPoint(x2, y2)
        color = self.label_color_linea.palette().color(QPalette.Background)
        fondo = self.label_color_fondo.palette().color(QPalette.Background)
        linea = self.tipo_linea()
        ancho = self.spin_ancho_linea.value()
        rect = Rectangulo(p1, p2, color, linea, ancho, fondo)
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
