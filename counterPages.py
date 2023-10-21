import time
from os import path
import datetime
from PyPDF2 import PdfReader
import os
import csv
from main import CalendarApp
from PyQt5.QtCore import QTimer
def search_files_in_directory(root_path, extension,dateIni, dateFin):
    dateIni= datetime.datetime.strptime(dateIni, '%Y-%m-%d %H:%M:%S').date()
    dateFin = datetime.datetime.strptime(dateFin, '%Y-%m-%d %H:%M:%S').date()
    sources = []
    for root, dirs, files in os.walk(root_path):
        for file in files:
            fileTimeStamp= datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(root, file))).date()
            if file.upper().endswith(extension) and (dateIni <= fileTimeStamp <= dateFin):
                sources.append(
                    {'path': os.path.join(root, file), 'file': file, 'date': fileTimeStamp})
    try:
        waitAppBox = CalendarApp()
        msgbox = waitAppBox.msg_box
        msgbox.setWindowTitle("Procesando Archivos.  Por Favor espere")
        msgbox.setText("Procesando Archivos.  Por favor espere")
        #msgbox.setWindowModality(2)
        msgbox.exec_()
        '''    timer = QTimer()
        timer.timeout.connect(msgbox.accept())
        timer.start(3000)
        '''
    except:
        print('Error al llamar msgBox Procesando Archivos')

    print("Hola estamos viendo un QMessageBox")
    numeroPaginas = read_pdf(root_path, sources)


def read_pdf(root_folder, sources):
    results = []
    counter_pages = 0
    results.append(['Ruta', 'Documento', 'Fecha', 'Número de páginas'])
    for source in sources:
        pdfFileObject= PdfReader(source.get('path'))
        counter = len(pdfFileObject.pages)
        results.append([source.get('path'), source.get('file'), source.get('date'), counter])
        counter_pages += counter

    results.append(['Total de paginas: ' + str(counter_pages)])
    if counter_pages == 0:
        app1 = CalendarApp()
        msgbox= app1.msg_box
        msgbox.setText("En la  ubicación seleccionada no se encontraron  archivos válidos  entre  las fechas específicadas")
        showDialog = app1.msg_box.exec_()
        return 0
    home_folder = os.path.expanduser("~")
    nameFile= f"results--{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
    writeCSV(os.path.join(home_folder, nameFile), results)


def writeCSV(csv_location, items):
    with open(csv_location, 'w', newline='') as file:
        writer = csv.writer(file)
        for i in items:
            writer.writerow(i)
    sucessAppBox = CalendarApp()
    msgbox = sucessAppBox.msg_box
    msgbox.setWindowTitle("Proceso Exitoso")
    msgbox.setText("Se ha generado el archivo CSV del movimiento solicitado")
    # msgbox.setWindowModality(2)
    msgbox.exec_()
