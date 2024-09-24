from PyQt5.QtWidgets import QMainWindow, QFileDialog, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QRect
import sys
import os
import numpy as np
from PIL import Image
from PIL.ImageQt import ImageQt
from matplotlib import cm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from segmentation.segmentator import Segmentator
from style_transfer.restyler import Restyler

class ImageRestyler(QMainWindow):
    def __init__(self):
        super().__init__()
        self.segmentator = Segmentator()
        # self.restyler = Restyler()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Img-Restyler')
        self.setGeometry(100, 100, 1000, 1000)
        
        self.label = QLabel(self)
        self.label.setGeometry(150, 50, 1000, 1000)

        self.original_image = QLabel(self)
        self.original_image.setGeometry(QRect(50, 50, 250, 250))
        self.original_image.setText("Original Image")
        self.original_image.setPixmap(QPixmap(None))
        self.original_image.setScaledContents(True)
        self.original_image.setObjectName("orig_img")

        self.style_image = QLabel(self)
        self.style_image.setGeometry(QRect(350, 50, 250, 250))
        self.style_image.setText("Style Image")
        self.style_image.setPixmap(QPixmap(None))
        self.style_image.setScaledContents(True)
        self.style_image.setObjectName("style_img")

        self.result_image = QLabel(self)
        self.result_image.setGeometry(QRect(650, 0, 330, 330))
        self.result_image.setText("Result Image")
        self.result_image.setPixmap(QPixmap(None))
        self.result_image.setScaledContents(True)
        self.result_image.setObjectName("result_img")

        self.btn_load = QPushButton('Load Original Image', self)
        self.btn_load.setGeometry(75, 700, 150, 40)
        self.btn_load.clicked.connect(self.load_original_image)

        self.btn_load = QPushButton('Load Style Image', self)
        self.btn_load.setGeometry(250, 700, 150, 40)
        self.btn_load.clicked.connect(self.load_style_image)
        
        self.btn_segment = QPushButton('Segment Image', self)
        self.btn_segment.setGeometry(75, 800, 150, 40)
        self.btn_segment.clicked.connect(self.segment_image)
        
        self.btn_style = QPushButton('Apply Style Transfer', self)
        self.btn_style.setGeometry(250, 800, 150, 40)
        self.btn_style.clicked.connect(self.style_transfer)

        self.btn_retrain = QPushButton('Retrain Model', self)
        self.btn_retrain.setGeometry(600, 800, 150, 40)
        self.btn_retrain.clicked.connect(self.retrain_model)
    

    def load_original_image(self):
        fname = QFileDialog.getOpenFileName(self, 'Choose Original Image', '../images',"Image files (*.jpg *.png)")
        self.original_image_path = fname[0]
        self.original_image.setPixmap(QPixmap(self.original_image_path))
        self.result_image.setPixmap(QPixmap(self.original_image_path))

    
    def load_style_image(self):
        fname = QFileDialog.getOpenFileName(self, 'Choose Style Image', '../images',"Image files (*.jpg *.png)")
        self.style_image_path = fname[0]
        self.style_image.setPixmap(QPixmap(self.style_image_path))


    def display_image(self, img_array):
        height, width = img_array.shape[:2]
        qimg = QImage(img_array.data, width, height, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qimg)
        self.label.setPixmap(pixmap)


    def segment_image(self):
        self.segmentator.load_model()
        self.segmentator.set_source_image(self.original_image_path)
        image_mask = self.segmentator.segment_image()
        print(image_mask, image_mask.shape)
        im = Image.fromarray(np.uint8(cm.gist_earth(image_mask)*255))
        qimage = ImageQt(im)
        pixmap = QPixmap.fromImage(qimage)
        self.result_image.setPixmap(pixmap)


    def style_transfer(self):
        pass


    def retrain_model(self):
        pass
