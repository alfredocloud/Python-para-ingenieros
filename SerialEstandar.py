import sys, time
from timeit import default_timer

from PyQt5 import uic, QtWidgets

 
#Graphics
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib.figure import Figure 
import matplotlib.pyplot as plt 

from datetime import datetime 
import serial
import numpy as np
import xlwt


#Inicializa las ventanas
qtCreatorFile = "SerialEstandar.ui" 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile) 


# #Define variable
i = 0

led_state = True

y = []
x = []

# tiempo = []
tiempo = 0

# creamos el fichero excel y csv
wb = xlwt.Workbook()
# añadimos hoja
ws = wb.add_sheet('Datos sensor')
# escribimos encabezados
ws.write(0,0,'Tiempo')
ws.write(0,1,'Tensión')



# Abrimos el puerto del arduino a 9600
# ser = serial.Serial('/dev/ttyACM0',9600)
ser = serial.Serial('COM3',9600)
ser.close()
ser.open()

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow): 


    def update(self):

        global i, tiempo
        t_inicio = default_timer()


   
        data = ser.readline() 
        time.sleep(0.02)

        


        x.append(tiempo)

        y.append(float(data.decode()))

        self.ax.clear()
        self.ax.grid()
        self.ax.plot(x, y)
    

        self.ax.set(xlabel='Tiempo (s)', ylabel='Tensión (Volts)',
        title='Gráfica')
        self.ax.legend('1')
        self.ax.set_ylim([-1, 6])


        self.ax.figure.canvas.draw()
        i += 1
        print(default_timer() - t_inicio+.09)
        tiempo += round(default_timer() - t_inicio +.09 ,4)
        
      

    def led(self):

        global led_state
        if led_state:
            ser.write(b'd')
            led_state = False
            self.On_off.setText('Encendido')
            self.Led.setStyleSheet("background-color: green")
        else:
            ser.write(b'i')
            led_state = True
            self.On_off.setText('Apagado')
            self.Led.setStyleSheet("background-color: black")

    def open(self):
        ser.reset_input_buffer()
        #Begin to graph
        self.timer = self.plotWidge.new_timer(100, [(self.update, (), {})])
        self.timer.start()


    
    def stop(self):
        ser.reset_input_buffer()
        self.timer.stop()

    



    def __init__(self):

        QtWidgets.QMainWindow.__init__(self) 
        Ui_MainWindow.__init__(self) 
        self.setupUi(self) 
        self.inicio.clicked.connect(self.open)
        self.parar.clicked.connect(self.stop)
        self.On_off.clicked.connect(self.led)

        self.show()


        #Graficar
        self.plotWidge = FigureCanvas(Figure(figsize=(5, 3)))
        self.grafica.addWidget(self.plotWidge)
        self.ax = self.plotWidge.figure.subplots()
        self.ax.plot([], [])
        





if __name__ == "__main__": 

    app = QtWidgets.QApplication(sys.argv) 
    window = MyApp() 
    app.exec_()


for n in range(len(y)):
  ws.write(n+1, 0, x[n])
  ws.write(n+1, 1, y[n])


# grabo Fichero ecel.
wb.save('Datos.xls')
