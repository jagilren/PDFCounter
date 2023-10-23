#Workers with Error at F10
import time
from os import path
import datetime
from PyPDF2 import PdfReader
import os
import csv
from main import CalendarApp
from PyQt5.QtCore import Qt, QThread,  pyqtSignal
from PyQt5.QtCore import QTimer
import logging

# Create a logger
logger = logging.getLogger(__name__)

class Worker(QThread):
    finished = pyqtSignal(int)
    def __init__(self, root_folder,sources):
        super().__init__()
        self.root_folder = root_folder
        self.sources = sources
    def run(self):
        # Execute your time-consuming function here
        numeroPaginas = self.read_pdf()
        self.finished.emit(numeroPaginas)

    def read_pdf_simulated(self):
        # Simulate a time-consuming operation
        print(self.root_folder, self.sources)
        import time
        time.sleep(5)
        numeroPaginas = 42
        return numeroPaginas # Replace with your actual result

    def read_pdf(self):
        results = []
        counter_pages = 0
        results.append(['Ruta', 'Documento', 'Fecha', 'Número de páginas'])
        for source in self.sources:
            pdfFileObject = PdfReader(source.get('path'))
            counter = len(pdfFileObject.pages)
            results.append([source.get('path'), source.get('file'), source.get('date'), counter])
            counter_pages += counter

        results.append(['Total de paginas: ' + str(counter_pages)])
        if counter_pages == 0:
            app1 = CalendarApp()
            msgbox = app1.msg_box
            msgbox.setText(
                "En la  ubicación seleccionada no se encontraron  archivos válidos  entre  las fechas específicadas")
            showDialog = app1.msg_box.exec_()
            return 0
        home_folder = os.path.expanduser("~")
        nameFile = f"results--{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
        writeCSV(os.path.join(home_folder, nameFile), results)
        return counter_pages

    '''def readPDF1(self):
        # Simulate a time-consuming operation
        import time
        time.sleep(20)
        return 42  # Replace with your actual result
    '''
def startWorker(root_path, sources):
    #mainWindowInstance=CalendarApp()
    #mainWindowInstance.generateCsv_button.setEnabled(False)
    # Create and start the worker thread
    try:
        logger.info('Before Worker instance')
        worker = Worker(root_path,sources)
        worker.finished.connect(onWorkerFinished)
        worker.start()
        logger.info('After Worker start')
    except Exception as error:
        error_description = str(error)
        print(f'Error en Bloque Workers:  {error_description}')

def onWorkerFinished(numeroPaginas):
        # This slot is called when the worker has finished
        #mainWindowInstance = CalendarApp()
        #mainWindowInstance.generateCsv_button.setEnabled(True)
        print("Worker finished with result:", numeroPaginas)


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
        print('Procesando Archivos')
        '''        waitAppBox = CalendarApp()
        msgbox = waitAppBox.msg_box
        msgbox.setWindowTitle("Procesando Archivos.  Por Favor espere")
        msgbox.setText("Procesando Archivos.  Por favor espere")
        #msgbox.setWindowModality(2)
        msgbox.exec_()
        '''
    except:
        print('Error al llamar msgBox Procesando Archivos')

    print("Hola estamos viendo un QMessageBox")
    '''numeroPaginas = read_pdf(root_path, sources)'''
    logger.info('Before StarWorker')
    startWorker(root_path,sources)



def writeCSV(csv_location, items):
    with open(csv_location, 'w', newline='') as file:
        writer = csv.writer(file)
        for i in items:
            writer.writerow(i)
    return None
    try:
        sucessAppBox = CalendarApp()
        msgbox = sucessAppBox.msg_box
        msgbox.setWindowTitle("Proceso Exitoso")
        msgbox.setText("Se ha generado el archivo CSV del movimiento solicitado")
        msgbox.exec_()
    except:
        print('Error al llamar msgBox Proceso Finalizado con éxito')

