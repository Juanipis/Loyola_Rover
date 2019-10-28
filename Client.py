# Programa para controlar rover Loyola CLIENTE#
from tkinter import *
import socket
from tkinter import messagebox
from threading import Thread
from time import sleep

ip_server = 0
port = 8000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
running_motor_1 = False
running_motor_2 = False
running_backwards = False


# --------------------------------Ventana de Control Loyola_Rover------------------------#

def forward(event):
    global running_motor_1
    global running_motor_2
    running_motor_1 = True
    running_motor_2 = True


def backwards(event):
    global running_backwards
    running_backwards = True


def left(event):
    global running_motor_1
    global running_motor_2
    running_motor_1 = True
    running_motor_2 = False


def right(event):
    global running_motor_1
    global running_motor_2
    running_motor_1 = False
    running_motor_2 = True


def stop(event):
    global running_motor_1
    global running_motor_2
    global running_backwards
    running_motor_1 = False
    running_motor_2 = False
    running_backwards = False
    clientSocket.send(bytes("stop", 'utf-8'))


def move(speed, clientsocket):
    while True:
        speed_set = speed.get()
        if running_motor_1 and running_motor_2:
            clientsocket.send(bytes("A:%s" % speed_set, 'utf-8'))
            print("Adelante : %s" % speed_set)
            sleep(0.05)
        elif running_motor_1:
            clientsocket.send(bytes("I:%s" % speed_set, 'utf-8'))
            sleep(0.05)
        elif running_motor_2:
            clientsocket.send(bytes("D: %s" % speed_set, 'utf-8'))
            sleep(0.05)
        elif running_backwards:
            clientsocket.send(bytes("B:%s" % speed_set, 'utf-8'))
            sleep(0.05)


def control_rover(rover_main):
    speed = Scale(rover_main, orient=HORIZONTAL, length=100, tickinterval=30)
    speed.grid(row=4, column=1)
    Label(rover_main, text="Velocidad").grid(row=3, column=1)
    # ------------Boton hacia adelante----------#
    button_up = Button(rover_main, text="▲")
    button_up.grid(row=0, column=1)
    button_up.bind('<ButtonPress-1>', forward)
    button_up.bind('<ButtonRelease-1>', stop)
    # ----------Boton de reversa----------------#
    button_down = Button(rover_main, text="▼")
    button_down.grid(row=2, column=1)
    button_down.bind('<ButtonPress-1>', backwards)
    button_down.bind('<ButtonRelease-1>', stop)
    # ----------Boton de izquierda--------------#
    button_left = Button(rover_main, text="◄")
    button_left.grid(row=1, column=0)
    button_left.bind('<ButtonPress-1>', left)
    button_left.bind('<ButtonRelease-1>', stop)
    # -----------Boton de derecha---------------#
    button_right = Button(rover_main, text="►", )
    button_right.grid(row=1, column=2)
    button_right.bind('<ButtonPress-1>', right)
    button_right.bind('<ButtonRelease-1>', stop)

    # ----Hilo para verificar estados--------#
    t = Thread(target=move, args=(speed, clientSocket))
    t.start()

    def cerrando_conexion():
        if messagebox.askokcancel("Cerrar", "Realmente deseas cerrar?"):
            clientSocket.close()
            rover_main.destroy()
            print("Exito de cierre de socket del cliente")

    rover_main.protocol("WM_DELETE_WINDOW", cerrando_conexion)


# ----------------------------------Ventana de ingreso de IP-----------------------------#
# ------Validar IP------#
def validate_ip(ip_server, ip_window):
    server = ip_server.get()
    try:
        clientSocket.connect((server, port))
        print("Conexión exitosa")
        ip_window.destroy()
        control_rover(rover_main)
    except TimeoutError:
        print("Conexión fallida")


# -----Ventana de ingreso de IP----------------#
def enter_ip(rover_main):
    ip_window = Toplevel(rover_main)
    ip_window.title("Ip Rover")
    Label(ip_window, text="Por favor ingresa la direccion ip del rover").grid(row=0, column=0)
    ip_server = Entry(ip_window)
    ip_server.grid(row=1, column=0)
    send_ip = Button(ip_window, text="Conectar", command=lambda: validate_ip(ip_server, ip_window)).grid(row=2, column=0)


# ---------------------------------------------------------------------------------------#


rover_main = Tk()
enter_ip(rover_main)

rover_main.mainloop()
