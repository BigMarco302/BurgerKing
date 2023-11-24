import collections
import threading
import time

class Pedido:
    def __init__(self, identificador, items):
        self.identificador = identificador
        self.items = items

MENU = {
    1: "Hamburguesa",
    2: "Helado",
    3: "Papas",
    4: "Refresco",
    5: "Hamburguesa con Queso",
    6: "Nuggets"
}

# Lock para sincronizar la impresión de mensajes en la consola
lock_consola = threading.Lock()

def tomar_pedido():
    print("Menú:")
    for num, item in MENU.items():
        print(f"  {num}. {item}")

    items = []
    while True:
        seleccion = input("Ingrese el número del ítem del menú (o escriba 'fin' para finalizar): ")
        if seleccion.lower() == 'fin':
            break
        try:
            num_seleccion = int(seleccion)
            if num_seleccion in MENU:
                items.append(MENU[num_seleccion])
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
            # print(f"  Preparando: {item}")
        print(f"---------->Pedido {pedido.identificador} listo.")
        pedidos_ejecutados.append(pedido)

def mostrar_pedidos(cola):
    with lock_consola:
        print("\nPedidos en cola:")
        for pedido in cola:
            print(f"  Pedido {pedido.identificador}: {pedido.items}")

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
        print("  2. Mostrar todos los pedidos en cola")
        print("  3. Mostrar todos los pedidos ejecutados")
        print("  4. Salir")

        opcion = input("Ingrese el número de la opción: ")

        if opcion == '1':
            nuevo_pedido = Pedido(identificador_pedido, tomar_pedido())
            identificador_pedido += 1
            cola_pedidos.append(nuevo_pedido)
            print(f"\nPedido {nuevo_pedido.identificador} agregado a la cola.")

        elif opcion == '2':
            mostrar_pedidos(cola_pedidos)

        elif opcion == '3':
            mostrar_pedidos_ejecutados(pedidos_ejecutados)

        elif opcion == '4':
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
