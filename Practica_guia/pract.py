#Ejercicio 1 · Quitar duplicados conservando el orden
ciudades = ["Quito","Guayaquil","Quito","Cuenca","Guayaquil"]

ciudades_unicas = []
for ciudad in ciudades:
    if ciudad not in ciudades_unicas:
        ciudades_unicas.append(ciudad)
print(ciudades_unicas)

#Ejercicio 2 · Contar con un diccionario
contador = {}
for ciudad in ciudades:
    contador[ciudad] = contador.get(ciudad, 0) + 1
print(contador)

#Ejercicio 3 · Conjuntos en acción
inscritos_matematica = {"Ana","Luis","Sol","Marco"}
inscritos_ingles = {"Luis","Marco","Ruth"}

print("estan en ambas: ", inscritos_matematica & inscritos_ingles)
print("solo en matematicas: ", inscritos_matematica - inscritos_ingles)
print("distintos: ", len(inscritos_matematica | inscritos_ingles))

#Ejercicio 4 · De lista de diccionarios a índice
clientes = [{"id":1,"nombre":"Ana"},{"id":2,"nombre":"Luis"}]

indice = {cliente["id"]: cliente for cliente in clientes}
print(indice[2]["nombre"])

#Ejercicio 5 · Tuplas como registros inmutables
ventas = [("enero", 1500), ("febrero", 1800), ("marzo", 1200)]

monto_total = sum(monto for mes, monto in ventas)
mejor_mes, mejor_monto = max(ventas, key=lambda venta: venta[1])

print(f"Total: {monto_total}")
print(f"Mejor mes: {mejor_mes} con {mejor_monto}")
for mes, monto in ventas:
    print(f"{mes:<8}: {monto:>6}")
