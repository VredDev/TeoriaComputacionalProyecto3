import json
import os
import re
from typing import Dict, Set, Callable, List, Tuple

class AFD:
    def __init__(
        self,
        estados: Set[str],
        estado_inicial: str,
        estados_aceptacion: Set[str],
        transiciones: Dict[str, List[Tuple[Callable[[str], bool], str]]]
    ):
        self.estados = estados
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = estados_aceptacion
        self.transiciones = transiciones

    def validar(self, cadena: str) -> bool:
        estado_actual = self.estado_inicial
        for simbolo in cadena:
            transicion_encontrada = False
            for condicion, estado_siguiente in self.transiciones.get(estado_actual, []):
                if condicion(simbolo):
                    estado_actual = estado_siguiente
                    transicion_encontrada = True
                    break
            if not transicion_encontrada:
                return False
        return estado_actual in self.estados_aceptacion


def crear_afd_matricula() -> AFD:
    """AFD para ITI-[0-9]{4}-[0-9]{4}"""
    es_digito = lambda c: c.isdigit()
    transiciones = {
        "q0":  [(lambda c: c == "I", "q1")],
        "q1":  [(lambda c: c == "T", "q2")],
        "q2":  [(lambda c: c == "I", "q3")],
        "q3":  [(lambda c: c == "-", "q4")],
        "q4":  [(es_digito, "q5")],
        "q5":  [(es_digito, "q6")],
        "q6":  [(es_digito, "q7")],
        "q7":  [(es_digito, "q8")],
        "q8":  [(lambda c: c == "-", "q9")],
        "q9":  [(es_digito, "q10")],
        "q10": [(es_digito, "q11")],
        "q11": [(es_digito, "q12")],
        "q12": [(es_digito, "q13")],
    }
    return AFD({f"q{i}" for i in range(14)}, "q0", {"q13"}, transiciones)


def crear_afd_cp() -> AFD:
    """AFD para [0-9]{5}"""
    es_digito = lambda c: c.isdigit()
    transiciones = {f"q{i}": [(es_digito, f"q{i+1}")] for i in range(5)}
    return AFD({f"q{i}" for i in range(6)}, "q0", {"q5"}, transiciones)


def crear_afd_telefono() -> AFD:
    """AFD para [0-9]{10}"""
    es_digito = lambda c: c.isdigit()
    transiciones = {f"q{i}": [(es_digito, f"q{i+1}")] for i in range(10)}
    return AFD({f"q{i}" for i in range(11)}, "q0", {"q10"}, transiciones)


def crear_afd_nombre() -> AFD:
    """AFD para nombres propios (letras y espacios simples, mínimo 2 caracteres)."""
    es_letra = lambda c: c.isalpha()
    es_espacio = lambda c: c == " "
    transiciones = {
        "q0": [(es_letra, "q1")],
        "q1": [(es_letra, "q2"), (es_espacio, "q3")],
        "q2": [(es_letra, "q2"), (es_espacio, "q3")],
        "q3": [(es_letra, "q2")],
    }
    return AFD({"q0", "q1", "q2", "q3"}, "q0", {"q2"}, transiciones)

class AutomataDePilaCorreo:
    """
    Autómata de Pila para validar: ITI-[0-9]{4}-[0-9]{4}@upslp.edu.mx
    Usa la pila para verificar la correspondencia exacta de cada símbolo esperado.
    """
    def validar(self, cadena: str) -> bool:
        plantilla = list("ITI-DDDD-DDDD@upslp.edu.mx")
        pila = ["$"] + plantilla[::-1]

        for simbolo in cadena:
            if not pila or pila[-1] == "$":
                return False  # Sobran caracteres en la entrada

            tope = pila.pop()
            if tope == "D":
                if not simbolo.isdigit():
                    return False
            else:
                if simbolo != tope:
                    return False
        return pila == ["$"]


class AutomataDePilaURL:
    def validar(self, cadena: str) -> bool:
        pila = ["$", "<RUTA_OPT>", "<DOMINIO>", "/", "/", ":", "<PROTO>"]
        idx = 0
        n = len(cadena)

        while pila:
            tope = pila.pop()

            if tope == "$":
                return idx == n

            elif tope == "<PROTO>":
                if cadena[idx:idx+5] == "https":
                    idx += 5
                elif cadena[idx:idx+4] == "http":
                    idx += 4
                else:
                    return False

            elif tope in (":", "/"):
                if idx < n and cadena[idx] == tope:
                    idx += 1
                else:
                    return False

            elif tope == "<DOMINIO>":
                inicio = idx
                while idx < n and cadena[idx] != "/":
                    idx += 1
                dominio = cadena[inicio:idx]
                etiquetas = dominio.split(".")

                # Debe tener al menos 2 etiquetas (ej. upslp.edu)
                if len(etiquetas) < 2:
                    return False

                # Validar cada etiqueta del dominio
                for etq in etiquetas[:-1]:
                    if not etq or not all(c.isalnum() or c == "-" for c in etq):
                        return False

                # Validar TLD (última etiqueta: mínimo 2 letras)
                tld = etiquetas[-1]
                if len(tld) < 2 or not tld.isalpha():
                    return False

            elif tope == "<RUTA_OPT>":
                if idx == n:
                    continue  # Ruta vacía (ε)
                if cadena[idx] != "/":
                    return False
                idx += 1
                permitidos = set("._/?=&%-")
                while idx < n:
                    if not (cadena[idx].isalnum() or cadena[idx] in permitidos):
                        return False
                    idx += 1

        return False

def validar_ip(cadena: str) -> bool:
    partes = cadena.split(".")
    if len(partes) != 4:
        return False
    return all(
        p.isdigit() and 0 <= int(p) <= 255 and (p == "0" or not p.startswith("0"))
        for p in partes
    )

def validar_contrasena(cadena: str) -> bool:
    return (
        len(cadena) >= 8
        and any(c.isupper() for c in cadena)
        and any(c.islower() for c in cadena)
        and any(c.isdigit() for c in cadena)
        and any(c in "!@#$%^&*()-_=+." for c in cadena)
    )

def validar_curp(cadena: str) -> bool:
    return bool(re.fullmatch(r"[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9][0-9]", cadena))


RECONOCEDORES: Dict[str, Callable[[str], bool]] = {
    "nombre":     crear_afd_nombre().validar,
    "correo":     AutomataDePilaCorreo().validar,
    "telefono":   crear_afd_telefono().validar,
    "curp":       validar_curp,
    "matricula":  crear_afd_matricula().validar,
    "cp":         crear_afd_cp().validar,
    "contrasena": validar_contrasena,
    "url":        AutomataDePilaURL().validar,
    "ip":         validar_ip,
}

def validar_registro(registro: Dict[str, str]) -> Tuple[bool, List[str]]:
    errores = []
    for campo, validador in RECONOCEDORES.items():
        valor = str(registro.get(campo, ""))
        if not validador(valor):
            errores.append(f"  [X] {campo}: '{valor}' -> INVÁLIDO")
    return len(errores) == 0, errores


def ejecutar_pruebas_json(ruta_archivo: str = "casos_prueba.json"):
    if not os.path.exists(ruta_archivo):
        print(f"\nError: No se encontró el archivo '{ruta_archivo}'.")
        print("Asegúrate de haberlo subido a la carpeta de archivos de Google Colab.")
        return

    with open(ruta_archivo, "r", encoding="utf-8") as f:
        casos = json.load(f)

    print(f"\nEjecutando {len(casos)} casos de prueba desde '{ruta_archivo}'...\n")
    for caso in casos:
        cid = caso.get("id", "?")
        desc = caso.get("descripcion", "")
        es_valido, errores = validar_registro(caso)
        estado = "VÁLIDO" if es_valido else "INVÁLIDO"
        print(f"--- Caso #{cid} ({desc}) -> {estado} ---")
        if errores:
            for err in errores:
                print(err)
        else:
            print("  [PASS] Todos los campos pertenecen al lenguaje.")
        print()


def ejecutar_modo_manual():
    print("\n--- INGRESO MANUAL DE CAMPOS ---")
    registro = {}
    for campo in RECONOCEDORES.keys():
        registro[campo] = input(f"Ingresa {campo}: ").strip()

    es_valido, errores = validar_registro(registro)
    print("\n=== RESULTADO DE VALIDACIÓN ===")
    if es_valido:
        print("[OK] Todos los campos ingresados son válidos.")
    else:
        print("Se encontraron los siguientes errores:")
        for err in errores:
            print(err)

def main():
    print("==============================================")
    print("  VALIDADOR CON AUTÓMATAS (UPSLP) ")
    print("==============================================")
    opcion = input("¿Deseas ejecutar pruebas desde JSON (A) o ingresar datos manualmente (M)? [A/M]: ").strip().upper()

    if opcion == "A":
        ejecutar_pruebas_json("casos_prueba.json")
    elif opcion == "M":
        ejecutar_modo_manual()
    else:
        print("Opción no válida. Ejecuta nuevamente y elige 'A' o 'M'.")


if __name__ == "__main__":
    main()
