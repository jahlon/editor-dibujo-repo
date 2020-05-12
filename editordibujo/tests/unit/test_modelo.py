import unittest

from unittest.mock import Mock, patch, mock_open
from editordibujo.dibujo import modelo


class TestDibujo(unittest.TestCase):

    def setUp(self):
        self.dibujo = modelo.Dibujo()

    def test_dibujo_no_guardado_cuando_se_crea(self):
        self.assertFalse(self.dibujo.esta_guardado(), "Un dibujo nuevo  no debería estar guardado")

    def test_dibujo_modificado_al_agregar_figura(self):
        linea = Mock()
        self.dibujo.agregar_figura(linea)
        self.assertTrue(self.dibujo.modificado, "dibujo.modificado debería ser True")

    def test_cantidad_de_figuras_al_agregar_figuras(self):
        linea = Mock()
        rectangulo = Mock()
        self.dibujo.agregar_figura(linea)
        self.dibujo.agregar_figura(rectangulo)
        self.assertEqual(len(self.dibujo.figuras), 2)

    def test_cargar_dibujo_de_archivo(self):
        linea = Mock()
        rectangulo = Mock()
        dibujo_cargado = modelo.Dibujo()
        dibujo_cargado.agregar_figura(linea)
        dibujo_cargado.agregar_figura(rectangulo)
        dibujo_cargado.seleccionada = linea
        dibujo_cargado.archivo = "TestFile"
        dibujo_cargado.modificado = False

        with patch("builtins.open", mock_open(), create=True):
            with patch('editordibujo.dibujo.modelo.pickle.load') as mock_pickle:
                mock_pickle.return_value = dibujo_cargado
                self.dibujo.cargar("TestFile")

        self.assertEqual(len(dibujo_cargado.figuras), len(self.dibujo.figuras),
                         "Número de figuras en dibujo diferente de archivo")
        self.assertIs(self.dibujo.seleccionada, linea, "La imagen seleccionada no es la del archivo")
        self.assertEqual(self.dibujo.archivo, "TestFile")
        self.assertFalse(self.dibujo.modificado)


if __name__ == "__main__":
    unittest.main()
