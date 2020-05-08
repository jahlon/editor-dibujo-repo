import sys

from PyQt5.QtWidgets import QApplication

from editordibujo.ui.vista import MainWindowEditorDibujo

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindowEditorDibujo()
    win.show()
    sys.exit(app.exec_())
