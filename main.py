import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore
import ui  # Это наш конвертированный файл дизайна

import re
import subprocess
import threading


class MultiLauncher(ui.MainWindow):
    fileRegistry = {}

    def __init__(self):
        super().__init__()

        #print(self.buttonsRegistry)
        self.assignHandlersToFileGroupBtns()

        #TODO: make it dynamic somehow
        self.buttonsRegistry["addFileGroupBtn"].clicked.connect(self.addFieldGroup)
        self.buttonsRegistry["savePresetBtn"].clicked.connect(self.saveConfig)
        self.parseConfig()
        #print(self.inputRowCounter)
        #print(self.btnAddFile_0)

    def parseConfig(self):
        file = None
        try:
            #TODO: remove hardcode file name
            file = open("./config.ini", "r")
        except:
            return

        clearedFileContent = [x.strip() for x in file.readlines()]
        for idx in range(len(clearedFileContent)):
            if idx > 1:
                self.createInputRow(True)
                self._addListenerToAddFileBtn(idx)
                self._addListenerToRemoveFileBtn(idx)

            self.buttonsRegistry["fileGroupButtons"][idx][self.btnAddPrefix + str(idx)].setText(clearedFileContent[idx])
            # self.assignHandlersToFileGroupBtns()



        print("parse config")

    def assignHandlersToFileGroupBtns(self):
        groupButtonsDict = self.buttonsRegistry["fileGroupButtons"]
        for key in groupButtonsDict:

            if key < 2:
                self._addListenerToAddFileBtn(key)
            else:
                print("key, {}".format(key))
                #TODO: rename file to fileGroup as we are deleting the whole input
                groupButtonsDict[key][self.btnRemoveFilePrefix + str(key)].clicked.connect(self.removeFileGroup)
                # self._addListenerToRemoveFileBtn(key)

    def _addListenerToAddFileBtn(self, groupId):
        addBtnName = self.btnAddPrefix + str(groupId)
        self.buttonsRegistry["fileGroupButtons"][groupId][addBtnName].clicked.connect(self.addFile)

    def _addListenerToRemoveFileBtn(self, groupId):
        removeBtnName = self.btnRemoveFilePrefix + str(groupId)
        self.buttonsRegistry["fileGroupButtons"][groupId][removeBtnName].clicked.connect(self.removeFileGroup)

    def getGroupNumInStr(self, qtSender):
        sender_name = qtSender.objectName()
        print(sender_name)
        file_group_number = re.search('\d+', sender_name).group(0)
        return str(file_group_number)

    def addFile(self):
        print("add file")
        groupId = self.getGroupNumInStr(self.sender())
        # sender = self.sender()
        print(groupId)


        dlg = QtWidgets.QFileDialog()
        file_picker_response = dlg.getOpenFileName()
        chosen_file_path = file_picker_response[0]

        if len(chosen_file_path) > 0:
            self.buttonsRegistry["fileGroupButtons"][int(groupId)][self.btnAddPrefix + str(groupId)].setText(chosen_file_path)
            self.addFileToRegistry("group_" + groupId, chosen_file_path)

            print(self.fileRegistry)



    def addFileToRegistry(self, file_name, file_path):
        self.fileRegistry[file_name] = file_path

    def removeFileGroup(self):
        sending_button = self.sender()
        search_match = re.search("\d", sending_button.objectName())
        input_row_id = search_match.group()
        self.deleteInputRow(input_row_id)

    def addFieldGroup(self):
        print("add file group")
        print(self.createInputRow)
        self.createInputRow(True)

    def saveConfig(self):
        print("save conf")
        with open('./config.ini', 'w') as file:
            #  json.dump(self.fileRegistry, file)
            for k, v in self.fileRegistry.items():
                file.write(v + "\n")

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MultiLauncher() # Создаём объект класса ExampleApp
    window.show(); #show window
    app.exec_() # run app

if __name__ == '__main__': #if we run the file directly, not importing to somene
    main(); # run main