from PyQt5 import QtWidgets
import sys
import os
import tkinter.filedialog
import design

class NodoArbolBinario:
    def __init__(self, nombre):
        self.nombre = nombre
        self.izquierda = None
        self.derecha = None

def insertar_nodo(raiz, nuevo_nodo):
    if raiz is None:
        return nuevo_nodo

    if nuevo_nodo.nombre < raiz.nombre:
        raiz.izquierda = insertar_nodo(raiz.izquierda, nuevo_nodo)
    elif nuevo_nodo.nombre > raiz.nombre:
        raiz.derecha = insertar_nodo(raiz.derecha, nuevo_nodo)

    return raiz

def inorden_traversal(raiz, nivel=0, lado=None, print_function=print):
    if raiz:
        inorden_traversal(raiz.izquierda, nivel + 1, "izquierda", print_function)
        if lado:
            print_function("  " * (nivel - 1) + f"|— {raiz.nombre} ({lado})")
        else:
            print_function("  " * nivel + f"{raiz.nombre}")
        inorden_traversal(raiz.derecha, nivel + 1, "derecha", print_function)

def construir_arbol_directorio(ruta, raiz_arbol=None):
    if raiz_arbol is None:
        raiz_arbol = NodoArbolBinario(os.path.basename(ruta))

    try:
        elementos = sorted(os.listdir(ruta))
        for elemento in elementos:
            elemento_ruta = os.path.join(ruta, elemento)
            if os.path.isdir(elemento_ruta):
                nuevo_nodo = NodoArbolBinario(elemento)
                raiz_arbol = insertar_nodo(raiz_arbol, nuevo_nodo)
                construir_arbol_directorio(elemento_ruta, nuevo_nodo)
    except PermissionError as e:
        print(f"No se puede acceder a {ruta}: {e}")

    return raiz_arbol

class ui2py(QtWidgets.QMainWindow, design.Ui_ui2py):
    savedir = os.getcwd()

    def __init__(self, parent=None):
        super(ui2py, self).__init__(parent)
        self.setupUi(self)
        self.OpenButton.clicked.connect(self.OpenUI)
        self.ClearButton.clicked.connect(self.Clear)
        self.ExitButton.clicked.connect(self.close)

        bar = self.menuBar()
        help_menu = bar.addMenu("Help")
        help_menu.addAction("Usage")
        help_menu.triggered[QtWidgets.QAction].connect(self.MenuHandler)

        about_menu = bar.addMenu("About")
        about_menu.addAction("Info")
        about_menu.triggered[QtWidgets.QAction].connect(self.MenuHandler)

    def OpenUI(self):
        root = tkinter.Tk()
        root.withdraw()

        folder_path = tkinter.filedialog.askdirectory(initialdir=self.savedir, title="Select Folder")

        if folder_path:
            self.savedir = folder_path
            raiz_arbol_directorio = construir_arbol_directorio(folder_path)
            self.show_tree_structure(raiz_arbol_directorio)
            self.PathLabel.setText(folder_path)
        else:
            self.show_tree_structure(None)

    def show_tree_structure(self, raiz):
        output = []

        def print_to_output(text):
            output.append(text)

        if raiz:
            print_to_output("Estructura del árbol:")
            inorden_traversal(raiz, print_function=print_to_output)
        else:
            output = ["No files selected"]

        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setText("\n".join(output))
        msg_box.setWindowTitle("Árbol de Directorios")
        msg_box.exec_()

    def Clear(self):
        self.SelectedFilesLabel.setText("")
        self.PathLabel.setText("")

    def MenuHandler(self, action):
        mode = 0
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

        if mode == 0:
            msg.setText("Usage:")
            msg.setInformativeText("WIP.")
            msg.setWindowTitle("Help")
        else:
            msg.setText("ui2py")
            msg.setInformativeText("Created by Grupo 2 - MateDiscreta")
            msg.setWindowTitle("About")

        msg.exec_()

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = ui2py()
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
