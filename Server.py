import RPi.GPIO as GPIO
import os
import socket

#------------Se definen las variables del servidor------#
ip_server = '127.0.0.1' #Cambiar por la ip del rover
port = 8000

#------------Se definen las entradas del rover----------#
#---Motor 1---#
ena = 18
in1 = 23
in2 = 24
#---Motor 2---#
enb = 19
in3 = 6
in4 = 5
#Configura los pines segun el microprocesador Broadcom
GPIO.setmode(GPIO.BCM)
#Configura los pines como salidas
GPIO.setup(ena, GPIO.OUT)
GPIO.setup(enb, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
#Define las salidas PWM
pwm_a = GPIO.PWM(ena, 500)
pwm_b = GPIO.PWM(enb, 500)
#Inicializan los PWM con un duty cycle de cero
pwm_a.start(0)
pwm_b.start(0)

#------------Funciones de movimiento------------#
def forward(speed):
    GPIO.output(in1, False)
    GPIO.output(in2, True)
    GPIO.output(in3, False)
    GPIO.output(in3, True)
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)

def backward(speed):
    GPIO.output(in1, True)
    GPIO.output(in2, False)
    GPIO.output(in3, True)
    GPIO.output(in3, False)
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)

def left(speed):
    GPIO.output(in1, False)
    GPIO.output(in2, True)
    GPIO.output(in3, False)
    GPIO.output(in3, True)
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(int(0))

def right(speed):
    GPIO.output(in1, False)
    GPIO.output(in2, True)
    GPIO.output(in3, False)
    GPIO.output(in3, True)
    pwm_a.ChangeDutyCycle(int(0))
    pwm_b.ChangeDutyCycle(int(speed))

def stop():
    GPIO.output(in1, False)
    GPIO.output(in2, True)
    GPIO.output(in3, False)
    GPIO.output(in3, True)
    pwm_a.ChangeDutyCycle(int(0))
    pwm_b.ChangeDutyCycle(int(0))

#---Comienzo del programa--#
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((ip_server, port))
#---Se empiezan a escuchar solicitudes de conexion--#
serverSocket.listen(1)
clientsocket, clientaddress = serverSocket.accept()
print ('Conexion desde: ', clientaddress)
#-----Bucle para recivir movimientos---#
while True:
    data = clientsocket.recv(1024)
    data_decoded = data.decode('utf-8')
    if not data: break
    if (data == "stop"):
        stop()
    direction = data_decoded[0]
    speed = data_decoded[1:2]
    if direction == 'A':
        forward(speed)
    elif direction == 'B':
        backward(speed)
    elif direction == 'L':
        left(speed)
    elif direction == 'R':
        right(speed)
    else:
        stop()
#------Comandos finales----#
pwm_a.stop()
pwm_b.stop()
os.system('clear')
clientsocket.close()
print("Cierre con exito :3")


