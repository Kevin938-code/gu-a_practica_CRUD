from models import Estudiante, CAMPOS_ESTUDIANTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

gestor = GestorJSON("data/estudiantes.json")

CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")
nota_minima = 0
nota_maxima = 20

def carnets_registrados(excepto_id=None):
    """CONJUNTO con los carnets ya usados. Sirve para detectar duplicados al instante."""
    return {
        str(registro.get("carnet", "")).lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }

def emails_registrados(execpto_id=None):
    return{
        registro["email"].lower()
        for registro in gestor.leer()
        if registro["id"] != execpto_id
    }

def siguiente_id():
        ids = [registro["id"] for registro in gestor.leer()]
        return max(ids) + 1 if ids else 1


def crear_estudiante(datos):
    try:
        valores = {campo: str(datos.get(campo, "")).strip() for campo in CAMPOS_ESTUDIANTE}
        
        faltantes = [campo for campo in CAMPOS_OBLIGATORIOS if not valores[campo]]
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"
        
        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no tiene un formato válido"
        
        if valores["email"].lower() in emails_registrados():
            return False, "Ese email ya está registrado"
        
        if valores["carnet"].lower() in carnets_registrados():
            return False, "Ese carnet ya está registrado"
        
        estudiante = Estudiante(siguiente_id(), **valores)
        
        registros = gestor.leer()
        registros.append(estudiante.a_diccionario())
        if not gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"
        
        return True, f"Estudiante {estudiante.obtener_nombre_completo()} creado con id {estudiante.id}"
    
    except Exception as error:
        return False, f"Error inesperado: {error}"    


def obtener_todos():
    return [Estudiante.desde_diccionario(registro) for registro in gestor.leer()]

def obtener_id(id_estudiante):
    for estudiante in obtener_todos():
        if estudiante.id == id_estudiante:
            return estudiante
    return None

def buscar_estudiante(termino):
    termino = termino.strip().lower()
    if not termino:
        return []
    
    encontrados = []
    for registro in gestor.leer():
        for campo in CAMPOS_BUSCABLES:
            if termino in str(registro.get(campo, "")).lower():
                encontrados.append(Estudiante.desde_diccionario(registro))
                break
    return encontrados

def actualizar_estudiante(id_estudiante, cambios):
    try:
        desconocidos = set(cambios) - set(CAMPOS_ESTUDIANTE)
        if desconocidos:
            return False, f"Campos no validos: {', '.join(sorted(desconocidos))}"
        
        if not cambios:
            return False, "No se indicó ningún cambio"
        
        if "email" in cambios:
            if not es_email_valido(cambios["email"]):
                return False, "El email no tiene un formato válido"
            if cambios["email"].lower() in emails_registrados(execpto_id=id_estudiante):
                return False, "Ese email ya lo usa otro estudiante"
        
        if "carnet" in cambios:
            if cambios["carnet"].lower() in carnets_registrados(excepto_id=id_estudiante):
                return False, "Ese carnet ya está registrado"
                
        registros = gestor.leer()
        posicion = None
        for indice, registro in enumerate(registros):
            if registro["id"] == id_estudiante:
                posicion = indice
                break
        
        if posicion is None:
            return False, f"No existe un estudiante con id {id_estudiante}"
        
        registros[posicion].update(cambios)
        gestor.guardar(registros)
        return True, f"Estudiante {id_estudiante} actualizado ({len(cambios)} campo/s)"
    except Exception as error:
        return False, f"Error inesperado: {error}"

def eliminar_estudiante(id_estudiante):
    registros = gestor.leer()
    quedan = [registro for registro in registros if registro["id"] != id_estudiante]
    
    if len(quedan) == len(registros):
        return False, f"No existe un estudiante con id {id_estudiante}"
    
    gestor.guardar(quedan)
    return True, f"Estudiante {id_estudiante} eliminado"

def agregar_nota(id_estudiante, materia, nota):
    try:
        materia = str(materia).strip()
        if not materia:
            return False, "La materia no puede estar vacía"

        try:
            nota = float(str(nota).strip().replace(",", "."))
        except ValueError:
            return False, "La nota debe ser un número"

        if not (nota_minima <= nota <= nota_maxima):
            return False, f"La nota debe estar entre {nota_minima} y {nota_maxima}"

        estudiante = obtener_id(id_estudiante)
        if estudiante is None:
            return False, f"No existe un estudiante con id {id_estudiante}"

        estudiante.agregar_nota(materia, nota)

        registros = gestor.leer()
        for indice, registro in enumerate(registros):
            if registro["id"] == id_estudiante:
                registros[indice] = estudiante.a_diccionario()
                break

        if not gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"
        return True, f"Nota {nota} agregada en '{materia}' a {estudiante.obtener_nombre_completo()}"
    except Exception as error:
        return False, f"Error inesperado: {error}"

def materias_ofertadas():
    materias = set()
    for registro in gestor.leer():
        materias.update(registro.get("materias", []))
    return materias

def estudiantes_en_comun(id_a, id_b):
    if id_a == id_b:
        return False, "Deben ser dos estudiantes diferentes"
    
    estudiante_a = obtener_id(id_a)
    if estudiante_a is None:
        return False, f"No existe un estudiante con id {id_a}"
    
    estudiante_b = obtener_id(id_b)
    if estudiante_b is None:
        return False, f"No existe un estudiante con id {id_b}"
    return True, estudiante_a.materias_en_comun(estudiante_b)