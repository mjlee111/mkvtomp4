import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel

class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.layout = QVBoxLayout()

        self.label = QLabel('Select an MKV file and choose an output path for the MP4 file', self)
        self.layout.addWidget(self.label)

        self.openFileButton = QPushButton('Open MKV File', self)
        self.openFileButton.clicked.connect(self.openFileDialog)
        self.layout.addWidget(self.openFileButton)

        self.saveFileButton = QPushButton('Save MP4 File As', self)
        self.saveFileButton.clicked.connect(self.saveFileDialog)
        self.layout.addWidget(self.saveFileButton)

        self.convertButton = QPushButton('Convert', self)
        self.convertButton.clicked.connect(self.convertFile)
        self.layout.addWidget(self.convertButton)

        self.setLayout(self.layout)
        self.setWindowTitle('MKV to MP4 Converter')
        self.setGeometry(300, 300, 400, 200)

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.input_file, _ = QFileDialog.getOpenFileName(self, "Open MKV File", "", "MKV Files (*.mkv);;All Files (*)", options=options)
        if self.input_file:
            self.label.setText(f"Selected MKV file: {self.input_file}")

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        self.output_file, _ = QFileDialog.getSaveFileName(self, "Save MP4 File As", "", "MP4 Files (*.mp4);;All Files (*)", options=options)
        if self.output_file:
            if not self.output_file.endswith('.mp4'):
                self.output_file += '.mp4'
            self.label.setText(f"Output MP4 file: {self.output_file}")

    def convertFile(self):
        if hasattr(self, 'input_file') and hasattr(self, 'output_file'):
            try:
                subprocess.run(['ffmpeg', '-i', self.input_file, self.output_file], check=True)
                self.label.setText(f"Successfully converted to {self.output_file}")
            except subprocess.CalledProcessError as e:
                self.label.setText(f"Error occurred: {e}")
        else:
            self.label.setText("Please select both input and output files")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ConverterApp()
    ex.show()
    sys.exit(app.exec_())

