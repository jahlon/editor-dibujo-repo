import sys

from PyQt5.QtWidgets import QApplication

from editordibujo.ui.vista import MainWindowEditorDibujo


def main() :
    app = QApplication(sys.argv)
    win = MainWindowEditorDibujo()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
