# Validador de Formularios y Documentos con Autómatas

Sistema de validación léxica y sintáctica desarrollado en **Python** que aplica los fundamentos de la **Teoría de la Computación y Lenguajes Formales** (alfabetos, expresiones regulares, Autómatas Finitos Deterministas, Gramáticas Libres de Contexto y Autómatas de Pila) para verificar nueve tipos de campos y estructuras de documentos institucionales (UPSLP).

---

## Características Principales

* **Motor Genérico de Autómatas Finitos Deterministas (AFD):** Implementación formal de la tupla $M = (Q, \Sigma, \delta, q_0, F)$ mediante funciones y tablas de transición de estados sin depender exclusivamente de expresiones regulares prefabricadas.
* **Autómatas de Pila (AP):** Implementación de memoria LIFO (`PUSH` / `POP`) para la validación estructural del correo institucional (`ITI-XXXX-XXXX@upslp.edu.mx`) y las fases sintácticas de una URL.
* **Gramática Libre de Contexto (GLC):** Definición formal en notación BNF/LL(1) para validar bloques estructurados de documentos (`USUARIO { ... }`).
* **Doble Modo de Ejecución:**
  * **Modo Automático (`A`):** Auditoría por lotes leyendo registros desde el archivo `casos_prueba.json`.
  * **Modo Manual (`M`):** Captura interactiva por consola con diagnóstico inmediato de errores por campo.

---

## Campos y Lenguajes Formales Soportados

| Campo | Mecanismo de Reconocimiento | Lenguaje / Patrón Formal |
| :--- | :--- | :--- |
| **Nombre** | AFD (`crear_afd_nombre`) | `[a-zA-ZáéíóúÁÉÍÓÚñÑ]{2,}( [a-zA-ZáéíóúÁÉÍÓÚñÑ]+)*` |
| **Correo** | Autómata de Pila (`AutomataDePilaCorreo`) | `ITI-[0-9]{4}-[0-9]{4}@upslp\.edu\.mx` |
| **Teléfono** | AFD (`crear_afd_telefono`) | `[0-9]{10}` |
| **CURP** | Regex / Estructural (`validar_curp`) | `[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9][0-9]` |
| **Matrícula** | AFD (`crear_afd_matricula`) | `ITI-[0-9]{4}-[0-9]{4}` |
| **Código Postal** | AFD (`crear_afd_cp`) | `[0-9]{5}` |
| **Contraseña** | Intersección de Lenguajes Regulares | Mín. 8 caracteres: 1 mayúscula, 1 minúscula, 1 dígito y 1 símbolo |
| **URL** | Autómata de Pila (`AutomataDePilaURL`) | `(http\|https)://([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/[a-zA-Z0-9._/?=&%-]*)?` |
| **Dirección IP** | Validación de Octetos (`validar_ip`) | 4 octetos decimales en rango `[0, 255]` sin ceros a la izquierda |

---

## Estructura del Proyecto

```text
├── validador_automatas.py   # Código fuente principal (AFD, AP y modos de ejecución)
├── casos_prueba.json        # Conjunto de 10 casos de prueba (válidos e inválidos)
└── README.md                # Documentación del proyecto
