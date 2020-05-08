import abc

from PyQt5.QtCore import QPoint, Qt, QLine, QRect
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush


class IFigura(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def pintar(self, qp: QPainter):
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

    def pintar(self, qp: QPainter):
        pen = QPen()
        pen.setStyle(self.tipo_linea)
        pen.setWidth(self.ancho_linea)
        pen.setColor(self.color_linea)
        qp.setPen(pen)
        qp.drawLine(self.linea)

    def esta_dentro(self, x: int, y: int) -> bool:
        # TODO: Implementar lógica para verificar que un punto pertenece a la línea
        pass


class FiguraRectangularConFondo(Figura, abc.ABC):
    def __init__(self, p1: QPoint, p2: QPoint, color_linea: QColor, tipo_linea: Qt.PenStyle, ancho_linea: int,
                 color_fondo: QColor):
        super().__init__(p1, p2, color_linea, tipo_linea, ancho_linea)
        self.color_fondo = color_fondo
        self.rect = QRect(p1, p2)

    def pintar(self, qp: QPainter):
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

    def agregar_figura(self, figura: IFigura):
        self.figuras.append(figura)

    def dibujar(self, qp: QPainter):
        for f in self.figuras:
            f.pintar(qp)
