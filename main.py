#создай тут фоторедактор Easy Editor!
#Подключение
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os
from PIL import Image,ImageFilter

#Окно
app = QApplication([])
window = QWidget()
window.resize(1600,900)
window.showFullScreen()

#Кнопки
K1 = QPushButton("Лево")
K2 = QPushButton("Право")
K3 = QPushButton("Зеркало")
K4 = QPushButton("Резкость")
K5 = QPushButton("Ч\Б")
K6 = QPushButton("Папка")
K7 = QPushButton("Контур")
K8 = QPushButton("Детали")
#Картинка
kartinka = QLabel("Картинка")

#Список
spisok = QListWidget()

#Линии
L1 = QVBoxLayout()
L2 = QVBoxLayout()
L3 = QHBoxLayout()
L4 = QHBoxLayout()

#Насаждение
L1.addWidget(K6)
L1.addWidget(spisok)

L2.addWidget(kartinka)

L4.addWidget(K1)
L4.addWidget(K2)
L4.addWidget(K3)
L4.addWidget(K4)
L4.addWidget(K5)
L4.addWidget(K7)
L4.addWidget(K8)

L2.addLayout(L4)

L3.addLayout(L1,20)

L3.addLayout(L2,80)

window.setLayout(L3)

#Функция
workdir = ""
def chooseWorkdir():
    global workdir #Обрашение к глобальной переменной
    workdir = QFileDialog.getExistingDirectory()

def filter(files, exceptions):
    spisok2 = []
    for file in files:
        for exception in exceptions:
            if file.endswith(exception):
                spisok2.append(file)
    return(spisok2)            

def showFilenamesList():
    chooseWorkdir()
    spisok1 = ['png','jpg','jpeg','gif','tiff','raw','jfif'] 
    h = filter(os.listdir(workdir),spisok1)
    spisok.clear()
    spisok.addItems(h)

#Созданеи класса
class ImageProcessor():
    def __init__(self):
        self.image = None

        self.nameimage = None

        self.safedir = "Papka/"

    def loadImage(self,filename):
        self.filename = filename
    
        imagedir = os.path.join(workdir,filename)

        self.image = Image.open(imagedir)

    def showImage(self, path):
        kartinka.hide()
        pixmapimage = QPixmap(path)
        w,h=kartinka.width(),kartinka.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        kartinka.setPixmap(pixmapimage)
        kartinka.show()

    def saveImage(self):
        path = os.path.join(workdir,self.safedir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    #Фильтры

    def do_chb(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir,self.safedir,self.filename)
        self.showImage(image_path)

    def rotate(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir,self.safedir,self.filename)
        self.showImage(image_path)

    def blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(workdir,self.safedir,self.filename)
        self.showImage(image_path)   

    def rotatei(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir,self.safedir,self.filename)
        self.showImage(image_path)

    def flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir,self.safedir,self.filename)
        self.showImage(image_path)

    def contur(self):
        self.image = self.image.filter(ImageFilter.CONTOUR)
        self.saveImage()
        image_path = os.path.join(workdir,self.safedir,self.filename)
        self.showImage(image_path)

    def detal(self):
        self.image = self.image.filter(ImageFilter.DETAIL)
        self.saveImage()
        image_path = os.path.join(workdir,self.safedir,self.filename)
        self.showImage(image_path)

workname = ImageProcessor()

def showChosenImage():
    if spisok.currentRow() >= 0:
        filename = spisok.currentItem().text()
        workname.loadImage(filename)
        image_path = os.path.join(workdir,workname.filename)
        workname.showImage(image_path)

#Обработка нажатия кнопки
spisok.currentRowChanged.connect(showChosenImage)
K8.clicked.connect(workname.detal)
K7.clicked.connect(workname.contur)
K6.clicked.connect(showFilenamesList)
K5.clicked.connect(workname.do_chb)
K1.clicked.connect(workname.rotate)
K2.clicked.connect(workname.rotatei)
K4.clicked.connect(workname.blur)
K3.clicked.connect(workname.flip)
#Окно
window.show()
app.exec()