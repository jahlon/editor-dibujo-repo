import abc
import pickle

from PyQt5.QtCore import QPoint, Qt, QLine, QRect
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush


class IFigura(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def pintar(self, qp: QPainter, seleccionada: bool):
        raise NotImplementedError

    @abc.abstractmethod
    def esta_dentro(self, x: int, y: int) -> bool:
        raise NotImplementedError


class Figura(IFigura, abc.ABC):
    def __init__(self, p1: QPoint, p2: QPoint, color_linea: QColor, tipo_linea: Qt.PenStyle, ancho_linea: int):
        self.punto_1 = p1
        self.punto_2 = p2
        self.color_linea = color_linea
        self.tipo_linea = tipo_linea
        self.ancho_linea = ancho_linea


class Linea(Figura):

    def __init__(self, p1: QPoint, p2: QPoint, color_linea: QColor, tipo_linea: Qt.PenStyle, ancho_linea: int):
        super().__init__(p1, p2, color_linea, tipo_linea, ancho_linea)
        self.linea = QLine(p1, p2)

    def pintar(self, qp: QPainter, seleccionada: bool):
        pen = QPen()
        pen.setStyle(self.tipo_linea)
        pen.setWidth(self.ancho_linea)
        pen.setColor(self.color_linea)
        qp.setPen(pen)
        qp.drawLine(self.linea)

        if seleccionada:
            brush = QBrush()
            brush.setColor(Qt.green)
            brush.setStyle(Qt.SolidPattern)
            pen = QPen()
            pen.setWidth(1)
            qp.setPen(pen)
            qp.setBrush(brush)
            qp.drawEllipse(self.punto_1.x() - 3, self.punto_1.y() - 3, 7, 7)
            qp.drawEllipse(self.punto_2.x() - 3, self.punto_2.y() - 3, 7, 7)

    def esta_dentro(self, x: int, y: int) -> bool:
        m = (self.punto_2.y() - self.punto_1.y()) / (self.punto_2.x() - self.punto_1.x())
        min_x = min(self.punto_1.x(), self.punto_2.x())
        max_x = max(self.punto_1.x(), self.punto_2.x())
        termino_y = m * (x - self.punto_1.x()) + self.punto_1.y()
        return (min_x <= x <= max_x) and (termino_y-5 <= y <= termino_y+5)


class FiguraRectangularConFondo(Figura, abc.ABC):
    def __init__(self, p1: QPoint, p2: QPoint, color_linea: QColor, tipo_linea: Qt.PenStyle, ancho_linea: int,
                 color_fondo: QColor):
        super().__init__(p1, p2, color_linea, tipo_linea, ancho_linea)
        self.color_fondo = color_fondo
        self.rect = QRect(p1, p2)

    def pintar(self, qp: QPainter, seleccionada: bool):
        pen = QPen()
        pen.setStyle(self.tipo_linea)
        pen.setWidth(self.ancho_linea)
        pen.setColor(self.color_linea)

        brush = QBrush()
        brush.setColor(self.color_fondo)
        brush.setStyle(Qt.SolidPattern)

        qp.setPen(pen)
        qp.setBrush(brush)
        self._pintar(qp)

        if seleccionada:
            brush = QBrush()
            brush.setColor(Qt.green)
            brush.setStyle(Qt.SolidPattern)
            qp.setBrush(brush)
            pen = QPen()
            pen.setWidth(1)
            qp.setPen(pen)
            qp.drawEllipse(self.punto_1.x() - 3, self.punto_1.y() - 3, 7, 7)
            qp.drawEllipse(self.punto_1.x() - 3, self.punto_2.y() - 3, 7, 7)
            qp.drawEllipse(self.punto_2.x() - 3, self.punto_2.y() - 3, 7, 7)
            qp.drawEllipse(self.punto_2.x() - 3, self.punto_1.y() - 3, 7, 7)

    def esta_dentro(self, x: int, y: int) -> bool:
        return self.rect.contains(x, y)

    @abc.abstractmethod
    def _pintar(self, qp: QPainter):
        raise NotImplementedError


class Rectangulo(FiguraRectangularConFondo):

    def __init__(self, p1: QPoint, p2: QPoint, color_linea: QColor, tipo_linea: Qt.PenStyle, ancho_linea: int,
                 color_fondo: QColor):
        super().__init__(p1, p2, color_linea, tipo_linea, ancho_linea, color_fondo)

    def _pintar(self, qp: QPainter):
        qp.drawRect(self.rect)


class Ovalo(FiguraRectangularConFondo):
    def __init__(self, p1: QPoint, p2: QPoint, color_linea: QColor, tipo_linea: Qt.PenStyle, ancho_linea: int,
                 color_fondo: QColor):
        super().__init__(p1, p2, color_linea, tipo_linea, ancho_linea, color_fondo)

    def _pintar(self, qp: QPainter):
        qp.drawEllipse(self.rect)


class Dibujo:
    def __init__(self):
        self.figuras = []
        self.seleccionada = None
        self.archivo = None
        self.modificado = False

    def esta_guardado(self):
        return self.archivo is not None

    def guardar(self, archivo=None):
        if archivo is not None:
            self.archivo = archivo

        with open(self.archivo, "wb") as f:
            pickle.dump(self, f)

        self.modificado = False

    def cargar(self, archivo):
        self.archivo = archivo

        with open(self.archivo, "rb") as f:
            d = pickle.load(f)
            self.figuras = d.figuras
            self.seleccionada = d.seleccionada
            self.archivo = d.archivo
            self.modificado = False

    def agregar_figura(self, figura: IFigura):
        self.figuras.append(figura)
        self.modificado = True

    def intentar_seleccionar(self, x, y):
        self.seleccionada = None
        for f in self.figuras:
            if f.esta_dentro(x, y):
                self.seleccionada = f
                self.modificado = True
                break

    def borrar_figura_seleccionada(self):
        if self.seleccionada is not None:
            self.figuras.remove(self.seleccionada)
            self.seleccionada = None
            self.modificado = True

    def dibujar(self, qp: QPainter):
        for f in self.figuras:
            f.pintar(qp, f == self.seleccionada)
