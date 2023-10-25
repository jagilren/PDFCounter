#Workers with Error at F10
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QPushButton, QVBoxLayout, QWidget, QFrame, QFileDialog, QLabel, QHBoxLayout,QMessageBox
from PyQt5.QtCore import QDate, pyqtSlot
from PyQt5.QtCore import Qt, QThread,  pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor
from threading import *
from datetime import datetime, time, timedelta
import logging
import counterPages

pasos = 0
retorno1=""
class MyMessageBox(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom MessageBox")
        self.setText("This is a custom QMessageBox.")
        #self.setStandardButtons(QMessageBox.Ok)
        self.setWindowTitle("Error en selección de datos")
        self.setIcon(QMessageBox.Information)
        custom_button = QPushButton("OK")
        custom_button.setStyleSheet("background-color: #3498db; color: white;")
        self.addButton(custom_button, QMessageBox.AcceptRole)


class CountPDFThread(QThread):
    def __init__(self,datetimeIni_label, datetimeEnd_label, route_label, window_instance):
        super().__init__()
        self.is_running = False
        self.lock = Lock()
        self.datetimeIni_label=datetimeIni_label
        self.datetimeEnd_label=datetimeEnd_label
        self.route_label=route_label
        self.window_instance = window_instance
        global retorno1
        #disable_button = pyqtSignal()
        #call_contarPDF = pyqtSignal()
        #enable_button = pyqtSignal()
        finished = pyqtSignal()
        #mostrarMensaje = pyqtSignal()
    def run(self):
        global retorno1
        self.window_instance.label_foot.setText("Procesando2")
        cal1App = CalendarApp()
        print("Running countPDF method inside of QThread...")
        #cal1App.label_foot.setText("Procesando2")
        retorno1 = cal1App.generateCsv(self.datetimeIni_label,self.datetimeEnd_label, self.route_label)
        self.finished.emit()

class CalendarApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        # Create a QMessageBox
        self.msg_box = QMessageBox(self)
        self.msg_box.setWindowTitle("Error en selección de datos")
        self.msg_box.setIcon(QMessageBox.Information)
        custom_button = QPushButton("OK")
        custom_button.setStyleSheet("background-color: #3498db; color: white;")
        self.msg_box.addButton(custom_button, QMessageBox.AcceptRole)

    def thread(self):
        t1 = Thread(target=self.generateCsv(self.datetimeIni_label,self.datetimeEnd_label, self.route_label))
        t1.start()

    def startCountPDFThread(self):
        # Create an instance of the CountPDFThread and start it
        self.generateCsv_button.setEnabled(False)
        self.folder_button.setEnabled(False)
        self.countPDF_thread = CountPDFThread(self.datetimeIni_label, self.datetimeEnd_label, self.route_label,self)
        self.countPDF_thread.finished.connect(self.onCountPDFFinished)
        #self.countPDF_thread.mostrarMensaje.connect(self.OnmostrarMensaje)
        self.countPDF_thread.start()

    def onCountPDFFinished(self):
        global pasos
        if pasos == 0:
            pasos = 1 if pasos == 0 else 0
            print("countPDF method is complete.")
            self.generateCsv_button.setEnabled(True)
            self.folder_button.setEnabled(True)
            self.label_foot.setText("...")
            global retorno1
            self.vbaMessageBox = MyMessageBox()
            self.vbaMessageBox.setText(retorno1)
            self.vbaMessageBox.exec_()
        else:
            pasos = 1 if pasos == 0 else 0

    def OnmostrarMensaje(self):
        global retorno1
        print(retorno1)



    def initUI(self):
        self.setWindowTitle("Indicador de Rendimiento CAD")
        self.setGeometry(500, 500, 500, 300)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        frame_root = QVBoxLayout()


        # Create two frames to enclose the calendar widgets
        frame_calendars = QFrame()
        frame_operations = QFrame()
        frame1 = QFrame()
        frame1.setLineWidth(3)
        frame2 = QFrame()
        frame2.setLineWidth(3)
        frame_path = QFrame()
        frame_csv = QFrame()
        frame_foot = QFrame()
        self.label_foot = QLabel("...")


        # Set frame borders
        '''frame_calendars.setFrameShape(QFrame.Box)'''
        frame_operations.setFrameShape(QFrame.Box)
        frame1.setFrameShape(QFrame.Box)
        frame2.setFrameShape(QFrame.Box)
        '''frame_path.setFrameShape(QFrame.Box)'''
        '''frame_csv.setFrameShape(QFrame.Box)'''

        # Set a fixed size for frame1 and frame2
        frame_calendars.setFixedWidth(810)
        frame_operations.setFixedWidth(810)
        frame1.setFixedHeight(300)
        frame2.setFixedHeight(300)
        frame1.setFixedWidth(400)
        frame2.setFixedWidth(400)
        frame_path.setFixedWidth(400)
        frame_csv.setFixedWidth(400)

        # Create calendar widgets inside the frames
        calendar1 = QCalendarWidget()
        self.calendar2 = QCalendarWidget()
        calendar1.clicked.connect(self.update_selected_dateIni)
        self.calendar2.clicked.connect(self.update_selected_dateEnd)

        # Create a push button to set the date
        dateIni_button = QPushButton("Set Date")
        dateIni_button.clicked.connect(self.setIni_date)
        dateEnd_button = QPushButton("Set Date")
        dateEnd_button.clicked.connect(self.setEnd_date)
        # Create a QFont to set font properties
        font = QFont()
        font.setFamily("Arial")  # Set the font family to Arial
        font.setPixelSize(20)  # Set the font family to Arial
        font.setBold(True)  # Set font weight to bold
        font.setItalic(True)  # Set font style to italic

        # Create a push button to select a folder
        self.folder_button = QPushButton("Select Folder")
        self.folder_button.clicked.connect(self.select_folder)
        # Create a push button to Generate Report
        self.generateCsv_button = QPushButton("Generar Reporte")
        #self.generateCsv_button.clicked.connect(lambda:self.generateCsv(self.datetimeIni_label,self.datetimeEnd_label, self.route_label))
        #self.generateCsv_button.clicked.connect(self.startCountPDFThread)
        self.generateCsv_button.clicked.connect(self.startCountPDFThread)

        # Add a QLabel to display the selected folder path
        self.Fecha_Inicial_Label = QLabel("Seleccione Fecha Inicial: ")
        self.Fecha_Final_Label = QLabel("Seleccione Fecha Final: ")
        self.dateIni_label = QLabel("Fecha inicial")
        self.datetimeIni_label = QLabel(datetime.now().date().strftime("%Y-%m-%d %H:%M:%S"))
        self.datetimeEnd_label = QLabel((datetime.now().date() + timedelta(days=1, seconds=0)).strftime("%Y-%m-%d %H:%M:%S"))
        self.dateEnd_label = QLabel("Fecha Final")
        self.route_label = QLabel("Route path: ")
        self.generateCsv_label = QLabel("Generar Reporte: ")
        self.Fecha_Inicial_Label.setFont(font)
        self.Fecha_Inicial_Label.setStyleSheet("color: green;")
        self.Fecha_Final_Label.setFont(font)
        self.Fecha_Final_Label.setStyleSheet("color: red;")

        # Add calendar widgets and buttons to frames
        frame1_layout = QVBoxLayout()
        frame1_layout.addWidget(self.Fecha_Inicial_Label)
        frame1_layout.addWidget(calendar1)
        #frame1_layout.addWidget(dateIni_button)
        frame1_layout.addWidget(self.dateIni_label)
        frame1_layout.addWidget(self.datetimeIni_label)
        frame1_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        frame1.setLayout(frame1_layout)

        frame2_layout = QVBoxLayout()
        frame2_layout.addWidget(self.Fecha_Final_Label)
        frame2_layout.addWidget(self.calendar2)
        #frame2_layout.addWidget(dateEnd_button)
        frame2_layout.addWidget(self.dateEnd_label)
        frame2_layout.addWidget(self.datetimeEnd_label)
        frame2_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        frame2.setLayout(frame2_layout)

        frame_path_layout = QVBoxLayout()
        frame_path_layout.addWidget(self.folder_button)
        frame_path_layout.addWidget(self.route_label)
        frame_path_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop | Qt.AlignVCenter ) #Align of Widget inside Frame
        frame_path.setLayout(frame_path_layout)

        frame_csv_layout = QVBoxLayout()
        frame_csv_layout.addWidget(self.generateCsv_label)
        frame_csv_layout.addWidget(self.generateCsv_button)
        frame_csv_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop | Qt.AlignVCenter) #Align of Widget inside Frame
        frame_csv.setLayout(frame_csv_layout)

        # Frame para mostrar estado del Proceso
        frame_foot_layout = QVBoxLayout()
        frame_foot_layout.addWidget(self.label_foot)
        frame_foot_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop | Qt.AlignVCenter)  # Align of Widget inside Frame
        frame_foot.setLayout(frame_foot_layout)

        frame_calendars_layout = QHBoxLayout()
        frame_calendars_layout.addWidget(frame1)
        frame_calendars_layout.addWidget(frame2)
        frame_calendars_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        frame_calendars.setLayout(frame_calendars_layout)

        frame_operations_layout = QHBoxLayout()
        frame_operations_layout.addWidget(frame_path)
        frame_operations_layout.addWidget(frame_csv)
        frame_operations_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop | Qt.AlignVCenter )
        frame_operations.setLayout(frame_operations_layout)

        frame_root.addWidget(frame_calendars)
        frame_root.addWidget(frame_operations)
        frame_root.addWidget(frame_foot)
        frame_root.setAlignment(Qt.AlignHCenter | Qt.AlignTop | Qt.AlignVCenter)
        central_widget.setLayout(frame_root)


    def select_folder(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", "", options=options)
        if folder_path:
            self.route_label.setText("Path: " + folder_path)

    def generateCsv(self, datetime1, datetime2, rutaRaiz):
        print(f'Entraste a generateCSV:  {datetime1.text()}')
        consistenciaFechas = self.deltaBetweenDateTimes(datetime1.text(),datetime2.text())
        distanciaEntreFechas = self.gapBetweenDates(datetime1.text(),datetime2.text())
        if consistenciaFechas and distanciaEntreFechas:
            try:
                if rutaRaiz.text().split("Path: ")[1][0].upper():
                    #self.generateCsv_button.setEnabled(False)
                    retorno2= counterPages.search_files_in_directory(rutaRaiz.text().split("Path: ")[1],'PDF',datetime1.text(),datetime2.text())
                    return retorno2
            except Exception as error:
                error_description = str(error)
                msg_box = MyMessageBox()
                #msg_box.exec_()
                ''''self.msg_box.setText(
                    "Debes Seleccionar una carpeta válida, donde se encuentren los Archivos PDF de imagenes")
                showDialog = self.msg_box.exec_()'''''
                print("Debes Seleccionar una carpeta válida, donde se encuentren los Archivos PDF de imagenes")
                return "Debes Seleccionar una carpeta válida, donde se encuentren los Archivos PDF de imagenes"
        else:
            if not(consistenciaFechas):
                msg_box = MyMessageBox()
                #msg_box.exec_()
                ''''self.msg_box.setText("Fecha final debe ser mayor o igual a Fecha inicial")
                showDialog = self.msg_box.exec_()'''''
                print("Fecha final debe ser mayor o igual a Fecha inicial")
                return "Fecha final debe ser mayor o igual a Fecha inicial"
            elif not(distanciaEntreFechas):
                msg_box = MyMessageBox()
                #msg_box.exec_()
                '''self.msg_box.setText("No puedes seleccionar un rango mayor a 16 días")
                showDialog = self.msg_box.exec_()'''
                print("No puedes seleccionar un rango mayor a 16 días")
                return "No puedes seleccionar un rango mayor a 16 días"
            else:
                msg_box = MyMessageBox()
                #msg_box.exec_()
                '''self.msg_box.setText("Error no determinado.  Comuníque al administrador del sistema")
                showDialog = self.msg_box.exec_()'''
                print("Error no determinado.  Comuníque al administrador del sistema")
                return "Error no determinado.  Comuníque al administrador del sistema"

    def deltaBetweenDateTimes(self,date_string1,date_string2):
        # Convert the datetime strings to datetime objects
        date_time1 = datetime.strptime(date_string1, "%Y-%m-%d %H:%M:%S")
        date_time2 = datetime.strptime(date_string2, "%Y-%m-%d %H:%M:%S")

        # Calculate the time difference
        time_difference = date_time2 - date_time1
        if time_difference.days >= 0:
            return True
        return False

        # Extract components of the time difference
        days = time_difference.days
        seconds = time_difference.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

    def gapBetweenDates(self,date_string1,date_string2):
        # Convert the datetime strings to datetime objects
        date_time1 = datetime.strptime(date_string1, "%Y-%m-%d %H:%M:%S")
        date_time2 = datetime.strptime(date_string2, "%Y-%m-%d %H:%M:%S")

        # Calculate the time difference
        time_difference = date_time2 - date_time1
        if time_difference.days <=16:
            return True
        return False


        # Extract components of the time difference
        days = time_difference.days
        seconds = time_difference.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

    def setIni_date(self):
        # Set the date in the first calendar widget to December 31, 2023
        date = QDate(2023, 12, 31)
        self.centralWidget().layout().itemAt(0).widget().layout().itemAt(0).widget().layout().itemAt(1).widget().setSelectedDate(date)

    def setEnd_date(self):
        # Set the date in the first calendar widget to December 31, 2023
        date = QDate(2024, 12, 31)
        self.centralWidget().layout().itemAt(0).widget().layout().itemAt(1).widget().layout().itemAt(1).widget().setSelectedDate(date)

    def update_selected_dateIni(self, date):
        # Combine the date and time to get a datetime object
        calendar2Qdate = QDate(date)
        combined_datetime = datetime.combine(datetime.strptime(date.toString(Qt.ISODate), "%Y-%m-%d").date(),time(0,0,0))
        self.datetimeIni_label.setText(combined_datetime.strftime("%Y-%m-%d %H:%M:%S"))
        self.calendar2.setSelectedDate(calendar2Qdate)
        combined_datetime2 = datetime.combine(datetime.strptime(date.toString(Qt.ISODate), "%Y-%m-%d").date(),
                                             time(23, 59, 59))
        self.datetimeEnd_label.setText(combined_datetime2.strftime("%Y-%m-%d %H:%M:%S"))
    def update_selected_dateEnd(self, date):
        # Combine the date and time to get a datetime object
        combined_datetime = datetime.combine(datetime.strptime(date.toString(Qt.ISODate), "%Y-%m-%d").date(),time(23,59,59))
        self.datetimeEnd_label.setText(combined_datetime.strftime("%Y-%m-%d %H:%M:%S"))



def main():
    app = QApplication(sys.argv)
    window = CalendarApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
