from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QLabel, QPushButton, QCheckBox, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect, Qt, QThread
import sys
import os
import numpy as np
import PIL
from PIL import Image
from PIL.ImageQt import ImageQt
from matplotlib import cm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from segmentation.segmentator import Segmentator
from style_transfer.restyler import Restyler
from constants import MAX_ITER_NO, RestyleStatus, restyling_status_msg_map

class ImageRestyler(QMainWindow):
    def __init__(self):
        super().__init__()
        self.segmentator = Segmentator()
        self.restyler = Restyler()
        self.invert_mode = 0
        self.train_iter_no = 2
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Img-Restyler')
        self.setGeometry(100, 100, 1000, 1000)
        
        self.label = QLabel(self)
        self.label.setGeometry(150, 50, 1000, 1000)

        self.original_image = QLabel(self)
        self.original_image.setGeometry(QRect(50, 50, 250, 250))
        self.original_image.setPixmap(QPixmap(None))
        self.original_image.setScaledContents(True)
        self.original_image.setObjectName("orig_img")
        self.original_image.setStyleSheet("background-color:white")

        self.original_image_label = QLabel(self)
        self.original_image_label.setGeometry(QRect(50, 303, 250, 15))
        self.original_image_label.setText("Original Image")

        self.style_image = QLabel(self)
        self.style_image.setGeometry(QRect(350, 50, 250, 250))
        self.style_image.setPixmap(QPixmap(None))
        self.style_image.setScaledContents(True)
        self.style_image.setObjectName("style_img")
        self.style_image.setStyleSheet("background-color:white")

        self.style_image_label = QLabel(self)
        self.style_image_label.setGeometry(QRect(350, 303, 250, 15))
        self.style_image_label.setText("Style Image")

        self.original_image_mask = QLabel(self)
        self.original_image_mask.setGeometry(QRect(50, 330, 250, 250))
        self.original_image_mask.setPixmap(QPixmap(None))
        self.original_image_mask.setScaledContents(True)
        self.original_image_mask.setObjectName("orig_img_mask")
        self.original_image_mask.setStyleSheet("background-color:white")

        self.original_image_mask_label = QLabel(self)
        self.original_image_mask_label.setGeometry(QRect(50, 583, 250, 15))
        self.original_image_mask_label.setText("Mask of Original image")

        self.result_image = QLabel(self)
        self.result_image.setGeometry(QRect(540, 350, 400, 400))
        self.result_image.setPixmap(QPixmap(None))
        self.result_image.setScaledContents(True)
        self.result_image.setObjectName("result_img")
        self.result_image.setStyleSheet("background-color:white")

        self.result_image_label = QLabel(self)
        self.result_image_label.setGeometry(QRect(540, 753, 400, 15))
        self.result_image_label.setText('Result Image')

        self.status_lbl = QLabel(self)
        self.status_lbl.setGeometry(600, 850, 300, 25)
        self.status_lbl.setAlignment(Qt.AlignCenter)
        self.set_restyling_status(RestyleStatus.NOT_STARTED.value)

        self.btn_load = QPushButton('Load Original Image', self)
        self.btn_load.setGeometry(75, 700, 150, 40)
        self.btn_load.clicked.connect(self.load_original_image)

        self.btn_load = QPushButton('Load Style Image', self)
        self.btn_load.setGeometry(250, 700, 150, 40)
        self.btn_load.clicked.connect(self.load_style_image)
        
        self.btn_segment = QPushButton('Segment Image', self)
        self.btn_segment.setGeometry(75, 800, 150, 40)
        self.btn_segment.clicked.connect(self.segment_image)

        self.cb_train_iter_no = QComboBox(self)
        self.cb_train_iter_no.setGeometry(QRect(250, 750, 50, 20))
        for k in range (1, MAX_ITER_NO):
            self.cb_train_iter_no.addItem(str(k))
        self.cb_train_iter_no.setCurrentIndex(1)
        self.cb_train_iter_no.currentIndexChanged.connect(self.train_iter_no_changed)

        self.cb_train_iter_no_label = QLabel(self)
        self.cb_train_iter_no_label.setGeometry(QRect(303, 750, 150, 20))
        self.cb_train_iter_no_label.setText('Pick Iteration Number')

        self.chkbx_invert_mod = QCheckBox(self)
        self.chkbx_invert_mod.setText('Invert mode')
        self.chkbx_invert_mod.setGeometry(QRect(250, 780, 110, 20))
        self.chkbx_invert_mod.stateChanged.connect(self.update_invert_mode)
        
        self.btn_style = QPushButton('Apply Style Transfer', self)
        self.btn_style.setGeometry(250, 800, 150, 40)
        self.btn_style.clicked.connect(lambda: self.set_restyling_status(RestyleStatus.ACTIVE.value))
        self.btn_style.clicked.connect(self.style_transfer)


    def load_original_image(self):
        fname = QFileDialog.getOpenFileName(self, 'Choose Original Image', '../images/animals',"Image files (*.jpg *.png)")
        self.original_image_path = fname[0]
        self.original_image.setPixmap(QPixmap(self.original_image_path))
        self.result_image.setPixmap(QPixmap(self.original_image_path))
        self.original_image_mask.setPixmap(QPixmap(None))
        self.mask_image = None
        self.mask_image_path = None
        self.set_restyling_status(RestyleStatus.NOT_STARTED.value)

    
    def load_style_image(self):
        fname = QFileDialog.getOpenFileName(self, 'Choose Style Image', '../images/styles',"Image files (*.jpg *.png)")
        self.style_image_path = fname[0]
        self.style_image.setPixmap(QPixmap(self.style_image_path))
        self.set_restyling_status(RestyleStatus.NOT_STARTED.value)


    def set_restyling_status(self, restyle_status):
        self.status_lbl.setText(restyling_status_msg_map[restyle_status][0])
        self.status_lbl.setStyleSheet(f'background-color:{restyling_status_msg_map[restyle_status][1]}')
        self.restyle_status = restyle_status


    def update_invert_mode(self, checked):
        if checked:
            self.invert_mode = 1
        else:
            self.invert_mode = 0


    def train_iter_no_changed(self, i):
        self.train_iter_no = int(self.cb_train_iter_no.itemText(i))


    def segment_image(self):
        self.segmentator.load_model()
        self.segmentator.set_source_image(self.original_image_path)
        image_mask = self.segmentator.segment_image()
        self.mask_image_path = '../images/mask.png'
        im = Image.fromarray(np.uint8(cm.gist_earth(image_mask)*255))
        im.save(self.mask_image_path)
        qimage = ImageQt(im)
        pixmap = QPixmap.fromImage(qimage)
        self.original_image_mask.setPixmap(pixmap)


    def style_transfer(self):
        self.set_restyling_status(RestyleStatus.ACTIVE.value)
        QApplication.processEvents()
        QThread.sleep(1)
        self.restyler.add_content_image(self.original_image_path)
        self.restyler.add_style_image(self.style_image_path)
        self.restyler.add_mask_image(self.mask_image_path)
        self.result_image_path = '../images/result.png'
        result_image = self.restyler.restyle(self.train_iter_no, self.invert_mode)
        result_image = (result_image.squeeze()*255).astype(np.uint8)
        im = PIL.Image.fromarray(result_image, mode='RGB')
        im.save(self.result_image_path)
        qimage = ImageQt(im)
        pixmap = QPixmap.fromImage(qimage)
        self.result_image.setPixmap(pixmap)
        self.set_restyling_status(RestyleStatus.FINISHED.value)
