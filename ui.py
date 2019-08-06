import sys

from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QWidget, QStyle, QStyleOption, QScrollArea
from PyQt5.QtGui import QPixmap, QIcon, QFont, QCursor, QPainter

# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout  short

import img

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.inputRowCounter = 0

        self.buttonsRegistry = {
            "fileGroupButtons": {}  # signature buttonsRegistry.fileGroupButtons[ inputRowCounter ][ btnName ] = btn
        }

        self.layout = QVBoxLayout()
        self.setStyleSheet("""
            background-color: #FFFFFF;
        """)
        self.layout.addWidget(MyBar(self))
        self.layout.addWidget(TopContentBlock(self))
        self.layout.addWidget(ProgramTitleBar(self))
        self.layout.addWidget(BottomContentBlock(self))

        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,74)
        self.layout.setSpacing(0)
        # self.layout.addStretch(-1)
        self.setMinimumSize(640,400)
        self.setWindowFlags(Qt.FramelessWindowHint)


        # self.pressing = False


class TopContentBlock(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.test_1 = 200
        self.parent = parent
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # self.content = QWidget()
        self.setFixedSize(640, 270)
        self.setStyleSheet("""
         background-color: #67BEC3;
        """)

        self.img = QLabel()
        self.img.setAlignment(Qt.AlignCenter)


        pixmap = QPixmap('main_illustration.png')
        # self.img.setPixmap(pixmap)
        self.img.setPixmap(pixmap)
        print(pixmap.width(), pixmap.height())
        # self.img.resize(pixmap.width(), pixmap.height())
        #self.img.setFixedSize(pixmap.width(), pixmap.height())

        self.layout.addWidget(self.img)
        # self.layout.addWidget(self.content)
        self.setLayout(self.layout)

class ProgramTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setContentsMargins(0, 70, 0, 30)

        self.title = QLabel("Business")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            font-weight: bold;
            font-family: Segoe UI;
            text-transform: uppercase;
            font-size: 40px;
            text-align: center;
            color: #303030;
        """)

        self.description = QLabel("select the programs you want run simultaneously")
        self.description.setStyleSheet("""
                    font-size: 16px;
                    color: rgba(0, 0, 0, 0.3);
                """)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.description)

        self.setLayout(self.layout)

class BottomContentBlock(QWidget):

    # base amount of the input rows. We can't delete a field if there are only 2 fields.
    inputRowsBaseAmount = 2
    # amount of the generated fields. Need to generate an id
    #inputRowCounter = 0

    inputRowPrefix = "inputRow_"
    btnAddPrefix = "btnAddFile_"
    btnRemoveFilePrefix = "btnRemoveFile_"
    btnMinHeight = 32
    # a left margin of the remove and add buttons
    BTN_LEFT_MARGIN = 15

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        # assign to the parent the createInputRow method
        self.parent.createInputRow = self.createInputRow
        print(parent)
        # base amount of the input rows. We can't delete a field if there are only 2 fields.
        #self.parent.inputRowsBaseAmount = 2
        # amount of the generated fields. Need to generate an id
        #self.parent.inputRowCounter = 0
        #self.parent.inputRowPrefix = "inputRow_"
        self.parent.btnAddPrefix = self.btnAddPrefix
        self.parent.btnRemoveFilePrefix = self.btnRemoveFilePrefix

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(86, 0, 56, 0)

        self.content = QWidget()


        # create a grid
        self.inputGrid = QGridLayout()

        #self.inputGrid.addLayout(self.createInputRow(), 0, 0)
        #self.inputGrid.addLayout(self.createInputRow(), 1, 0)
        # creating 2 base rows
        self.createInputRow()
        self.createInputRow()


        #self.inputGrid.addWidget(ActionPanel(self), 2, 0)


        # scrollArea.addWidget(self.inputGrid)

        self.content.setLayout(self.inputGrid)






        scrollArea = QScrollArea()
        scrollArea.setStyleSheet("""
             QScrollArea {
                border: none;
             }
             QScrollBar:vertical {
                 border: none;
                 background: transparent;
                 width: 4;
                 margin: 0 0 0 0;
                 height: 100%
             }
             QScrollBar::handle:vertical {
                 background: #C4C4C4;
                 min-height: 20px;
                 border-radius: 2px;
             }
             QScrollBar::add-line:vertical {
                 height: 0;
             }
            
             QScrollBar::sub-line:vertical {
                 height: 0;
                 
             }
             QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                border: none;
                background: none;
                height: 0;
             }
            
             QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                 background: none;
             }
        """)

        scrollArea.setWidget(self.content)
        scrollArea.setWidgetResizable(True)
        scrollArea.setFixedHeight(92)

        self.layout.addWidget(scrollArea)
        self.layout.addWidget(ActionPanel(parent))
        self.setLayout(self.layout)
        # self.content.setLayout(scrollArea)

        # create a table
        # self.inputTable = QTableWidget(2, 3)

    def createInputRow(self, withRemoveBtn=False):
        # create a row

        inputName = self.inputRowPrefix + str(self.parent.inputRowCounter)
        addBtnName = self.btnAddPrefix + str(self.parent.inputRowCounter)
        removeBtnName = self.btnRemoveFilePrefix + str(self.parent.inputRowCounter)
        # TODO: refactor it
        #inputName = self.inputRowPrefix
        #addBtnName = self.btnAddPrefix
        #removeBtnName = self.btnRemoveFilePrefix

        inputLayout = QHBoxLayout()
        inputLayout.setSpacing(self.BTN_LEFT_MARGIN)

        addBtn = QPushButton('Click to select a Program or a File')
        addBtn.setMinimumHeight(self.btnMinHeight)
        addBtn.setObjectName(addBtnName)
        addBtn.setCursor(Qt.PointingHandCursor)
        addBtn.setStyleSheet("""
                    text-align: left;
                    padding-left: 15px;
                    background-color: #EFF3F4;
                    border: none;
                    border-radius: 2px;
                """)

        inputLayout.addWidget(addBtn, 1)
        #print(self.parent.buttonsRegistry)
        self.parent.buttonsRegistry["fileGroupButtons"][self.parent.inputRowCounter] = {addBtnName: addBtn}
        #print(self.parent.buttonsRegistry)

        if withRemoveBtn:
            removeBtn = QPushButton();
            removeBtn.setObjectName(removeBtnName)
            removeBtn.setMinimumHeight(self.btnMinHeight)
            removeBtn.setCursor(Qt.PointingHandCursor)
            removeBtn.setStyleSheet("""
                               width: 14px;
                               border: none;
                               background-color: transparent;
                           """)

            icon = QIcon()
            icon.addPixmap(QPixmap(":/img/close_ic_dark.png"), QIcon.Normal, QIcon.Off)

            removeBtn.setIcon(icon)
            inputLayout.addWidget(removeBtn, 0)
            self.parent.buttonsRegistry["fileGroupButtons"][self.parent.inputRowCounter][removeBtnName] = removeBtn;
            #self.parent.buttonsRegistry[self.parent.inputRowCounter][removeBtnName] = removeBtn
            #setattr(self, removeBtnName, removeBtn)





        # we need to add these objects like a class prop to provide access for them
        #setattr(self, addBtnName, addBtn)
        #setattr(self, inputName, inputLayout)

        #print(self.inputRowCounter);

        self.inputGrid.addLayout(inputLayout, self.parent.inputRowCounter, 0)

        # updating counter to achieve an unique id for the next row
        self.parent.inputRowCounter += 1

        return inputLayout

class ActionPanel(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent # it's a MainWindow
        self.actionPanel = QVBoxLayout()

        self.actionPanel.setContentsMargins(0, 0, 15 + 15, 0)

        self.actionPanel.setObjectName("actionPanel")
        self.addFileGroupBtn = QPushButton("add one more")
        self.addFileGroupBtn.setObjectName("addFileGroup")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addFileGroupBtn.sizePolicy().hasHeightForWidth())
        self.addFileGroupBtn.setSizePolicy(sizePolicy)
        self.addFileGroupBtn.setMinimumHeight(32)
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setItalic(False)
        self.addFileGroupBtn.setFont(font)

        self.addFileGroupBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.addFileGroupBtn.setMouseTracking(False)
        self.addFileGroupBtn.setStyleSheet("""
                    background-color: #FFFFFF;
                    color: #9FB9B9;
                    border: 2px dashed #EFF3F4;
                    margin-bottom: 34px;
                """)

        icon = QIcon()
        icon.addPixmap(QPixmap(":/img/add_one_more.png"), QIcon.Normal, QIcon.Off)

        self.addFileGroupBtn.setIcon(icon)
        self.addFileGroupBtn.setAutoExclusive(False)
        self.addFileGroupBtn.setObjectName("addFileGroupBtn")

        self.savePresetBtn = QPushButton("Save preset")
        self.savePresetBtn.setObjectName("savePresetBtn")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addFileGroupBtn.sizePolicy().hasHeightForWidth())
        self.savePresetBtn.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setItalic(False)
        self.savePresetBtn.setFont(font)
        self.savePresetBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.savePresetBtn.setMouseTracking(False)
        self.savePresetBtn.setStyleSheet("""
                        background-color: #67BEC3; 
                        text-transform: uppercase; 
                        padding: 10px 6px; 
                        color: #FFFFFF; 
                        border: none;
                """)

        self.actionPanel.addWidget(self.addFileGroupBtn)
        self.actionPanel.addWidget(self.savePresetBtn)

        self.parent.buttonsRegistry["addFileGroupBtn"] = self.addFileGroupBtn
        self.parent.buttonsRegistry["savePresetBtn"] = self.savePresetBtn

        self.setLayout(self.actionPanel)


class MyBar(QWidget):


    def __init__(self, parent):
        super().__init__()
        self.setStyleSheet("""
            background-color: #67BEC3;
        """)
        self.parent = parent
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.title = QLabel("Multi Launcher - Business")

        btn_size = 32

        self.btn_min = QPushButton()
        self.btn_min.setCursor(Qt.PointingHandCursor)
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.setFixedSize(btn_size, btn_size)
        self.btn_min.setStyleSheet("""
            background: url(:/img/hide_ic.png) no-repeat center;
            border: none;
            color: red;
        """)

        self.btn_close = QPushButton()
        self.btn_close.setCursor(Qt.PointingHandCursor)
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.setFixedSize(btn_size, btn_size)
        self.btn_close.setStyleSheet("""
            background: url(:/img/close_ic.png) no-repeat center;
            border: none;
        """)

        # self.btn_max = QPushButton("+")
        # self.btn_max.clicked.connect(self.btn_max_clicked)
        # self.btn_max.setFixedSize(btn_size, btn_size)
        # self.btn_max.setStyleSheet("background-color: gray;")

        self.title.setFixedHeight(32)
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setAlignment(Qt.AlignVCenter)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.btn_min)
        # self.layout.addWidget(self.btn_max)
        self.layout.addWidget(self.btn_close)

        self.title.setStyleSheet("""
            padding-left: 22px;
            font-size: 16px;
            color: #FFFFFF;
        """)
        self.setLayout(self.layout)

        self.start = QPoint(0, 0)
        self.pressing = False

    def resizeEvent(self, QResizeEvent):
        super(MyBar, self).resizeEvent(QResizeEvent)
        self.title.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                self.mapToGlobal(self.movement).y(),
                                self.parent.width(),
                                self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False


    def btn_close_clicked(self):
        self.parent.close()

    def btn_max_clicked(self):
        self.parent.showMaximized()

    def btn_min_clicked(self):
        self.parent.showMinimized()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())


