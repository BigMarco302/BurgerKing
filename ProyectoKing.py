import collections
import threading
import time
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://BigMarco302:Vazquez1976@clustermarco.w6s7tqg.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
def escribir_base_de_datos(hilo_id,pedido):
    # Realizar la conexión a la base de datos
    client = MongoClient(uri)
    db = client["mydb"]
    users_collection = db["Burguer"]

    # Insertar el valor en la base de datos
    usuario = {
        "hilo": pedido,
    }

    result = users_collection.insert_one(usuario)
    print(f"Hilo {hilo_id}: Usuario insertado con ID: {result.inserted_id}")

    # Cerrar la conexión
    client.close()
class Pedido:
    def __init__(self, identificador, items):
        self.identificador = identificador
        self.items = items

MENU = {
    1: {"nombre": "Hamburguesa", "cantidad_vendida": 0},
    2: {"nombre": "Helado", "cantidad_vendida": 0},
    3: {"nombre": "Papas", "cantidad_vendida": 0},
    4: {"nombre": "Refresco", "cantidad_vendida": 0},
    5: {"nombre": "Hamburguesa con Queso", "cantidad_vendida": 0},
    6: {"nombre": "Nuggets", "cantidad_vendida": 0}
}

# Lock para sincronizar la impresión de mensajes en la consola se encarga que cuando
#el hilo1 llega y se procrece pero si llega otro hilo2 este quedara en espera hasta que termine el hilo1
lock_consola = threading.Lock()


def tomar_pedido():
    global cantidad_vendida
    print("Menú:")
    for num, item in MENU.items():
        print(f"  {num}. {item['nombre']} - {item['cantidad_vendida']} vendidos")

    items = []
    while True:
        seleccion = input("Ingrese el número del ítem del menú (o escriba 'fin' para finalizar): ")
        if seleccion.lower() == 'fin':
            break
        try:
            num_seleccion = int(seleccion)
            if num_seleccion in MENU:
                item_seleccionado = MENU[num_seleccion]
                if item_seleccionado['cantidad_vendida'] < 30:
                    items.append(item_seleccionado['nombre'])
                    item_seleccionado['cantidad_vendida'] += 1
                else:
                    print("¡Ya no hay suficiente producto!")
            else:
                print("Número no válido. Intente nuevamente.")
        except ValueError:
            print("Entrada no válida. Ingrese un número o 'fin'.")

    return items


def procesar_pedido(pedido, pedidos_ejecutados):
    with lock_consola:
        print(f"\nProcesando pedido {pedido.identificador}...")
        for item in pedido.items:
            # Simulación de tiempo de preparación
            time.sleep(2)
            print(pedido.items)
            # print(f"  Preparando: {item}")
        # escribir_base_de_datos(threading.current_thread().name, pedido)
        print(f"---------->Pedido {pedido.identificador} listo.")
        pedidos_ejecutados.append(pedido)

def mostrar_pedidos_ejecutados(pedidos_ejecutados):
    with lock_consola:
        print("\nPedidos ejecutados:")
        for pedido in pedidos_ejecutados:
            print(f"  Pedido {pedido.identificador}: {pedido.items}")

def main():
    cola_pedidos = collections.deque()
    pedidos_ejecutados = []
    identificador_pedido = 1

    while True:
        print("\nBienvenido a Burger King. ¿Qué desea hacer?")
        print("  1. Tomar un nuevo pedido")
        print("  2. Mostrar todos los pedidos ejecutados")
        print("  3. Salir")

        opcion = input("Ingrese el número de la opción: ")

        if opcion == '1':
            nuevo_pedido = Pedido(identificador_pedido, tomar_pedido())
            identificador_pedido += 1
            cola_pedidos.append(nuevo_pedido)
            print(f"\nPedido {nuevo_pedido.identificador} agregado a la cola.")

        elif opcion == '2':
            mostrar_pedidos_ejecutados(pedidos_ejecutados)

        elif opcion == '3':
            break

        else:
            print("Opción no válida. Intente nuevamente.")

        # Procesar automáticamente los pedidos en la cola si hay alguno
        if cola_pedidos:
            pedido_actual = cola_pedidos.popleft()
            # print(f"\nProcesando automáticamente pedido {pedido_actual.identificador} de la cola...")
            hilo_procesamiento = threading.Thread(target=procesar_pedido, args=(pedido_actual, pedidos_ejecutados))
            hilo_procesamiento.start()

if __name__ == "__main__":
    main()
