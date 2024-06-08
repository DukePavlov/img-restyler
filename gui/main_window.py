from PyQt5.QtWidgets import QMainWindow, QFileDialog, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage


class ImageRestyler(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Img-Restyler')
        self.setGeometry(100, 100, 800, 640)
        
        self.label = QLabel(self)
        self.label.setGeometry(150, 50, 500, 400)
        
        self.btn_segment = QPushButton('Segment Image', self)
        self.btn_segment.setGeometry(50, 500, 150, 40)
        self.btn_segment.clicked.connect(self.segment_image)
        
        self.btn_style = QPushButton('Apply Style Transfer', self)
        self.btn_style.setGeometry(250, 500, 150, 40)
        self.btn_style.clicked.connect(self.style_transfer)

        self.btn_retrain = QPushButton('Retrain Model', self)
        self.btn_retrain.setGeometry(600, 500, 150, 40)
        self.btn_retrain.clicked.connect(self.retrain_model)
    

    def display_image(self, img_array):
        height, width = img_array.shape[:2]
        qimg = QImage(img_array.data, width, height, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qimg)
        self.label.setPixmap(pixmap)

    def segment_image(self):
        pass


    def style_transfer(self):
        pass


    def retrain_model(self):
        pass
