import os

#Define el árbol
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

def inorden_traversal(raiz, nivel=0, lado=None):
    if raiz:
        inorden_traversal(raiz.izquierda, nivel + 1, "izquierda")
        if lado:
            print("  " * (nivel - 1) + f"|— {raiz.nombre} ({lado})")
        else:
            print("  " * nivel + f"{raiz.nombre}")
        inorden_traversal(raiz.derecha, nivel + 1, "derecha")

def construir_arbol_directorio(ruta, raiz_arbol=None):
    if raiz_arbol is None:
        raiz_arbol = NodoArbolBinario(ruta)

    try:
        elementos = sorted(os.listdir(ruta))  # Ordenar alfabéticamente
        for elemento in elementos:
            elemento_ruta = os.path.join(ruta, elemento)
            if os.path.isdir(elemento_ruta):
                nuevo_nodo = NodoArbolBinario(elemento)
                raiz_arbol = insertar_nodo(raiz_arbol, nuevo_nodo)
                construir_arbol_directorio(elemento_ruta, nuevo_nodo)
            else:
                nuevo_nodo = NodoArbolBinario(elemento)
                raiz_arbol = insertar_nodo(raiz_arbol, nuevo_nodo)
    except PermissionError as e:
        print(f"No se puede acceder a {ruta}: {e}")

    return raiz_arbol

# Cambien su ruta noma
ruta_carpeta = r"D:\Backup\Escritorio\Proyecto MateDiscreta"

raiz_arbol_directorio = construir_arbol_directorio(ruta_carpeta)

# Realizar el recorrido inorden para imprimir los elementos ordenados alfabéticamente con formato de árbol
print("Estructura del árbol:")
inorden_traversal(raiz_arbol_directorio)
