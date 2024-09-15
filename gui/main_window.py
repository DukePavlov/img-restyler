from PyQt5.QtWidgets import QMainWindow, QFileDialog, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QRect


class ImageRestyler(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Img-Restyler')
        self.setGeometry(100, 100, 800, 640)
        
        self.label = QLabel(self)
        self.label.setGeometry(150, 50, 500, 400)

        self.original_image = QLabel(self)
        self.original_image.setGeometry(QRect(0, 0, 330, 330))
        self.original_image.setText("Original Image")
        self.original_image.setPixmap(QPixmap(None))
        self.original_image.setScaledContents(True)
        self.original_image.setObjectName("photo")

        self.btn_load = QPushButton('Load Image', self)
        self.btn_load.setGeometry(50, 500, 100, 40)
        self.btn_load.clicked.connect(self.load_image)
        
        self.btn_segment = QPushButton('Segment Image', self)
        self.btn_segment.setGeometry(175, 500, 150, 40)
        self.btn_segment.clicked.connect(self.segment_image)
        
        self.btn_style = QPushButton('Apply Style Transfer', self)
        self.btn_style.setGeometry(350, 500, 150, 40)
        self.btn_style.clicked.connect(self.style_transfer)

        self.btn_retrain = QPushButton('Retrain Model', self)
        self.btn_retrain.setGeometry(600, 500, 150, 40)
        self.btn_retrain.clicked.connect(self.retrain_model)
    

    def load_image(self):
        fname = QFileDialog.getOpenFileName(self, 'Choose Image', '../images',"Image files (*.jpg *.png)")
        self.original_image_path = fname[0]
        print(self.original_image_path)
        self.original_image.setPixmap(QPixmap(self.original_image_path))


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
