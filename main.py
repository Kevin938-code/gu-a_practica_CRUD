from models import CAMPOS_ESTUDIANTE
from shared.herramientas import (imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar)
from views import (agregar_nota, crear_estudiante, estudiantes_en_comun, obtener_todos, obtener_id, buscar_estudiante, 
                actualizar_estudiante, eliminar_estudiante, materias_ofertadas)


def pausa():
    input("\n Presione Enter para continuar...")


def mostrar_tabla(estudiantes):
    print(f"{'ID':<5}{'NOMBRE':<25}{'EMAIL':<28}{'CARNET':<12}")
    print("-"*85)
    for estudiante in estudiantes:
        print(f"{estudiante.id:<5}{estudiante.obtener_nombre_completo():<25}"
            f"{estudiante.email:<28}{estudiante.carnet:<12}")
    print("-"*85)
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")


def opcion_crear():
    imprimir_titulo("CREAR UN NUEVO ESTUDIANTE")
    datos = {}
    for campo in CAMPOS_ESTUDIANTE:
        datos[campo]= input(f"{campo.capitalize()}: ")
    
    exito, mensaje = crear_estudiante(datos)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()

def opcion_ver_todos():
    imprimir_titulo("LISTA DE ESTUDIANTES")
    estudiantes = obtener_todos()
    if not estudiantes:
        imprimir_info("Todavía no hay estudiantes. Use la opción 1 para crear el primero")
    else:
        mostrar_tabla(estudiantes)
    pausa()

def opcion_buscar():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, email, carnet: ")
    encontrados = buscar_estudiante(termino)

    if not encontrados:
        imprimir_info(f"Ningún estudiante coincide con '{termino}'.")
    else:
        mostrar_tabla(encontrados)
    pausa()


def opcion_ver_por_id():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
            imprimir_error("El id debe ser un número entero")
            return pausa()
    
    estudiante = obtener_id(id_estudiante)
    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
    else:
        for clave, valor in estudiante.a_diccionario().items():
            print(f"  {clave.capitalize():<12}: {valor}")
    pausa()

def opcion_actualizar():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = obtener_id(id_estudiante)
    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        return pausa()

    imprimir_info(f"Editando a {estudiante.obtener_nombre_completo()}")
    print("Deje en blanco el campo que no quiera cambiar.\n")

    cambios = {}
    for campo in CAMPOS_ESTUDIANTE:
        actual = getattr(estudiante, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    exito, mensaje = actualizar_estudiante(id_estudiante, cambios)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()

def opcion_eliminar():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = obtener_id(id_estudiante)
    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        return pausa()

    imprimir_info(f"Se eliminará: {estudiante}")
    if confirmar("¿Confirma la eliminación?"):
        exito, mensaje = eliminar_estudiante(id_estudiante)
        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)
    else:
        imprimir_info("Operación cancelada")
    pausa()

def opcion_agregar_nota():
    imprimir_titulo("AGREGAR NOTA")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    materia = input("Materia: ")
    nota = input("Nota (0-20): ")

    exito, mensaje = agregar_nota(id_estudiante, materia, nota)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()

def opcion_ver_promedio():
    imprimir_titulo("VER PROMEDIO")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = obtener_id(id_estudiante)
    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
    else:
        imprimir_info(f"estudiante: {estudiante.obtener_nombre_completo()}")
        for materia, lista in sorted(estudiante.notas.items()):
            print(f" {materia:<20}: {', '.join(str(n) for n in lista)}")
        imprimir_exito(f"Promedio: {estudiante.obtener_promedio()}")
    pausa()

def opcion_materias_en_comun():
    imprimir_titulo("MATERIAS EN COMUN")
    try:
        id_a = int(input("Id del primer estudiante: "))
        id_b = int(input("Id del segundo estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()
    
    exito, resultado = estudiantes_en_comun(id_a, id_b)
    if not exito:
        imprimir_error(resultado)
    elif not resultado:
        imprimir_info("No tienen materias en común")
    else:
        imprimir_exito(f"Materias en común: {', '.join(sorted(resultado))}")
    pausa()

def opcion_materias_ofertadas():
    imprimir_titulo("MATERIAS OFERTADAS")
    materias = materias_ofertadas()
    if not materias:
        imprimir_info("No hay materias ofertadas")
    else:
        for materia in sorted(materias):
            print(f" - {materia}")
        imprimir_info(f"Total: {len(materias)} materia(s)")
    pausa()

OPCIONES = {
    "1": ("Crear un nuevo estudiante", opcion_crear),
    "2": ("Ver todos los estudiantes", opcion_ver_todos),
    "3": ("Buscar estudiante", opcion_buscar),
    "4": ("Ver estudiante por id", opcion_ver_por_id),
    "5": ("Actualizar estudiante", opcion_actualizar),
    "6": ("Eliminar estudiante", opcion_eliminar),
    "7": ("Agregar nota", opcion_agregar_nota),
    "8": ("Ver promedio de un estudiante", opcion_ver_promedio),
    "9": ("Ver materias en común entre dos estudiantes", opcion_materias_en_comun),
    "10": ("Ver materias ofertadas", opcion_materias_ofertadas),
    "0": ("Salir", None),
}

def mostrar_menu():
    imprimir_titulo("MENÚ PRINCIPAL")
    for clave, (texto, _) in OPCIONES.items():
        print(f" {clave:>2}. {texto}")

def main():
    while True:
        mostrar_menu()
        eleccion = input("\nElija una opción: ").strip()
        if eleccion == "0":
            imprimir_info("¡Hasta luego! (^_^)")
            break
        
        if eleccion in OPCIONES:
            OPCIONES[eleccion][1]()
        else:
            imprimir_error("Opción no valida")
            pausa()

if __name__ == "__main__":
    main()