import collections
import threading
import time
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://BigMarco302:Vazquez1976@clustermarco.w6s7tqg.mongodb.net/?retryWrites=true&w=majority"

# Lock para sincronizar la impresión de mensajes en la consola
lock_consola = threading.Lock()

def conectar_base_de_datos():
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)
        return None

def escribir_base_de_datos(client, hilo_id, pedido):
    db = client["mydb"]
    users_collection = db["Burguer"]

    usuario = {
        "hilo": pedido,
    }

    result = users_collection.insert_one(usuario)
    print(f"Hilo {hilo_id}: Usuario insertado con ID: {result.inserted_id}")

def tomar_pedido():
    # Implementación de la función tomar_pedido
    pass

def procesar_pedido(pedido, pedidos_ejecutados, client):
    for item in pedido.items:
        time.sleep(2)
        print(pedido.items)

    escribir_base_de_datos(client, threading.current_thread().name, pedido)
    print(f"---------->Pedido {pedido.identificador} listo.")
    pedidos_ejecutados.append(pedido)

def mostrar_pedidos_ejecutados(pedidos_ejecutados):
    with lock_consola:
        print("\nPedidos ejecutados:")
        # Implementación de la función mostrar_pedidos_ejecutados

def main():
    client = conectar_base_de_datos()
    if client is None:
        return

    pedidos_ejecutados = []

    while True:
        print("\nBienvenido a Burger King. ¿Qué desea hacer?")
        print("  1. Tomar un nuevo pedido")
        print("  2. Mostrar todos los pedidos ejecutados")
        print("  3. Salir")

        opcion = input("Ingrese el número de la opción: ")

        if opcion == '1':
            nuevo_pedido = tomar_pedido()
            if nuevo_pedido:
                procesar_pedido(nuevo_pedido, pedidos_ejecutados, client)
                print(f"\nPedido {nuevo_pedido.identificador} agregado a la cola.")

        elif opcion == '2':
            mostrar_pedidos_ejecutados(pedidos_ejecutados)

        elif opcion == '3':
            client.close()
            break

        else:
            print("Opción no válida. Inténtelo de nuevo.")
