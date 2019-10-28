# Programa para controlar rover Loyola CLIENTE#
from tkinter import *
import socket
from tkinter import messagebox
from threading import Thread
from time import sleep

ip_server = 0
port = 5151
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
running_motor_1 = False
running_motor_2 = False
running_backwards = False


# --------------------------------Ventana de Control Loyola_Rover------------------------#

def forward(speed, clientSocket):
    speed_set = speed.get()
    clientSocket.send(bytes("AF%s" %speed_set, 'utf-8'))
    sleep(0.01)
    clientSocket.send(bytes("BF%s" %speed_set, 'utf-8'))


def backwards(speed, clientSocket):
    speed_set = speed.get()
    clientSocket.send(bytes("AR%s" %speed_set, 'utf-8'))
    sleep(0.01)
    clientSocket.send(bytes("BR%s" %speed_set, 'utf-8'))


def left(speed, clientSocket):
    speed_set = speed.get()
    clientSocket.send(bytes("AF0", 'utf-8'))
    sleep(0.01)
    clientSocket.send(bytes("BF%s" %speed_set, 'utf-8'))


def right(speed, clientSocket):
    speed_set = speed.get()
    clientSocket.send(bytes("AF%s" %speed_set, 'utf-8'))
    sleep(0.01)
    clientSocket.send(bytes("BF0" %speed_set, 'utf-8'))


def stop(clientSocket):
    clientSocket.send(bytes("AF0", 'utf-8'))
    clientSocket.send(bytes("BF0", 'utf-8'))


def control_rover(rover_main, clientSocket):
    speed = Scale(rover_main, orient=HORIZONTAL, length=100, tickinterval=30)
    speed.grid(row=4, column=1)
    Label(rover_main, text="Velocidad").grid(row=3, column=1)
    # ------------Boton hacia adelante----------#
    button_up = Button(rover_main, text="▲", command=lambda: forward(speed, clientSocket))
    button_up.grid(row=0, column=1)
    # ----------Boton de reversa----------------#
    button_down = Button(rover_main, text="▼", command=lambda: backwards(speed, clientSocket))
    button_down.grid(row=2, column=1)
    # ----------Boton de izquierda--------------#
    button_left = Button(rover_main, text="◄", command=lambda: left(speed, clientSocket))
    button_left.grid(row=1, column=0)
    # -----------Boton de derecha---------------#
    button_right = Button(rover_main, text="►", command=lambda: right(speed, clientSocket))
    button_right.grid(row=1, column=2)
    # -----------Boton de Parada---------------#
    button_stop = Button(rover_main, text="■", command=lambda: stop(clientSocket))
    button_stop.grid(row=1, column=1)


    def cerrando_conexion():
        if messagebox.askokcancel("Cerrar", "Realmente deseas cerrar?"):
            clientSocket.send(bytes("final", 'utf-8'))
            clientSocket.close()
            rover_main.destroy()
            print("Exito de cierre de socket del cliente")

    rover_main.protocol("WM_DELETE_WINDOW", cerrando_conexion)


# ----------------------------------Ventana de ingreso de IP-----------------------------#
# ------Validar IP------#
def validate_ip(ip_server, ip_window):
    server = ip_server.get()
    try:
        clientSocket.connect(('%s' %server, 5151))
        print("Conexión exitosa")
        ip_window.destroy()
        control_rover(rover_main, clientSocket)
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
