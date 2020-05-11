import editordibujo.ui.resources

from PyQt5 import uic, QtGui
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QColor, QPainter, QPaintEvent, QPalette, QBrush
from PyQt5.QtWidgets import QMainWindow, QWidget, QFrame, QColorDialog, QFileDialog, qApp

from editordibujo.dibujo.modelo import Dibujo, Rectangulo, Linea, Ovalo


class Canvas(QWidget):
    def __init__(self, main_window):
        QWidget.__init__(self)
        self.main_window = main_window
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        if e.button() == Qt.LeftButton:
            self.main_window.hacer_click(e.x(), e.y())

    def paintEvent(self, e: QPaintEvent) -> None:
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        self.main_window.dibujar(qp)

        x_sel = self.main_window.x_seleccionado
        y_sel = self.main_window.y_seleccionado
        if x_sel != -1 and y_sel != -1:
            brush = QBrush()
            brush.setColor(Qt.green)
            brush.setStyle(Qt.SolidPattern)
            qp.setBrush(brush)
            qp.drawEllipse(x_sel-2, y_sel-2, 3, 3)

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
        self.guardado = False
        self.configurar_ui()

    def configurar_ui(self):
        self.actualizar_titulo()

        self.canvas_container.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.canvas_container.layout().addWidget(self.canvas)

        pal_fondo = self.label_color_fondo.palette()
        pal_fondo.setColor(QPalette.Background, Qt.blue)
        self.label_color_fondo.setPalette(pal_fondo)
        pal_linea = self.label_color_linea.palette()
        pal_linea.setColor(QPalette.Background, Qt.black)
        self.label_color_linea.setPalette(pal_linea)
        self.label_color_fondo.mousePressEvent = self.seleccionar_color_fondo
        self.label_color_linea.mousePressEvent = self.seleccionar_color_linea

        self.pbutton_borrar.clicked.connect(self.borrar_figura)

        self.accion_guardar.triggered.connect(self.guardar_dibujo)
        self.accion_abrir.triggered.connect(self.abrir_dibujo)
        self.accion_salir.triggered.connect(qApp.quit)

    def actualizar_titulo(self):
        mod = "*" if self.dibujo.modificado else ""
        if self.dibujo.esta_guardado():
            titulo = f"Editor de dibujo - {self.dibujo.archivo} {mod}"
        else:
            titulo = f"Editor de dibujo - Sin nombre {mod}"

        self.setWindowTitle(titulo)

    def guardar_dibujo(self):
        if not self.dibujo.esta_guardado():
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, "Guardar dibujo", "", "Dibujo (*.dibujo)",
                                                       "Dibujo (*.dibujo)", options)
            if file_name:
                self.dibujo.guardar(file_name)
        else:
            self.dibujo.guardar()
        self.actualizar_titulo()

    def abrir_dibujo(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Abrir dibujo", "", "Dibujo (*.dibujo)", "Dibujo (*.dibujo)",
                                                   options)
        if file_name:
            self.dibujo.abrir(file_name)

        self.actualizar_titulo()

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
        self.canvas.repaint()

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

    def borrar_figura(self):
        self.dibujo.borrar_figura_seleccionada()
        self.canvas.repaint()
        self.actualizar_titulo()

    def seleccionar(self, x: int, y: int):
        self.dibujo.intentar_seleccionar(x, y)
        self.canvas.repaint()
        self.actualizar_titulo()

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
        p1 = QPoint(x1, y1)
        p2 = QPoint(x2, y2)
        c_linea = self.label_color_linea.palette().color(QPalette.Background)
        c_fondo = self.label_color_fondo.palette().color(QPalette.Background)
        ancho = self.spin_ancho_linea.value()
        t_linea = self.tipo_linea()
        if self.pbutton_linea.isChecked():
            figura = Linea(p1, p2, c_linea, t_linea, ancho)
        elif self.pbutton_rect.isChecked():
            figura = Rectangulo(p1, p2, c_linea, t_linea, ancho, c_fondo)
        elif self.pbutton_ovalo.isChecked():
            figura = Ovalo(p1, p2, c_linea, t_linea, ancho, c_fondo)

        self.dibujo.agregar_figura(figura)
        self.canvas.repaint()
        self.actualizar_titulo()

    def dibujar(self, qp: QPainter):
        self.dibujo.dibujar(qp)
