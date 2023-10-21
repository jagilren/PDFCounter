import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

class Worker(QThread):
    finished = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def run(self):
        # Execute your time-consuming function here
        result = self.countPages()
        self.finished.emit(result)

    def countPages(self):
        # Simulate a time-consuming operation
        import time
        time.sleep(20)
        return 42  # Replace with your actual result

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt Thread Example")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.button = QPushButton("Generate Statistics")
        self.button.clicked.connect(self.startWorker)

        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def startWorker(self):
        self.button.setEnabled(False)

        # Create and start the worker thread
        self.worker = Worker()
        self.worker.finished.connect(self.onWorkerFinished)
        self.worker.start()

    def onWorkerFinished(self, result):
        # This slot is called when the worker has finished
        self.button.setEnabled(True)
        print("Worker finished with result:", result)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
