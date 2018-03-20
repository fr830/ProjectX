import sys
import serial.tools.list_ports as list_ports
from PyQt5.QtWidgets import QApplication,QMessageBox,QWidget,QComboBox,QLabel,QPushButton,QLineEdit
from PyQt5 import uic
from PyQt5.QtCore import QTimer
import sController

    
#Главная форма 
class MainForm(QWidget):
    def __init__(self,*args):
        super(MainForm,self).__init__(*args)
        uic.loadUi('main.ui',self)
        
        self.globalTimeout=5000

        self.sController=sController.Controller()        
        self.listPorts()

        #Сигналы
        self.stateList=list()
        self.stateList.append(self.btnState1)
        self.stateList.append(self.btnState2)
        self.stateList.append(self.btnState3)
        self.stateList.append(self.btnState4)
        self.stateList.append(self.btnState5)
        self.stateList.append(self.btnState6)
        self.stateList.append(self.btnState7)
        self.stateList.append(self.btnState8)
        self.stateList.append(self.btnState9)
        self.stateList.append(self.btnState10)
        self.stateList.append(self.btnState11)
        self.stateList.append(self.btnState12)
        self.stateList.append(self.btnState13)
        self.stateList.append(self.btnState14)
        self.stateList.append(self.btnState15)
        self.stateList.append(self.btnState16)
        
        #########################################
        #Задержки
        self.delayList=list()
        self.delayList.append(self.sbDelayValue_1)
        self.delayList.append(self.sbDelayValue_2)
        self.delayList.append(self.sbDelayValue_3)
        self.delayList.append(self.sbDelayValue_4)
        self.delayList.append(self.sbDelayValue_5)
        self.delayList.append(self.sbDelayValue_6)
        self.delayList.append(self.sbDelayValue_7)
        self.delayList.append(self.sbDelayValue_8)
        self.delayList.append(self.sbDelayValue_9)
        self.delayList.append(self.sbDelayValue_10)
        self.delayList.append(self.sbDelayValue_11)
        self.delayList.append(self.sbDelayValue_12)
        self.delayList.append(self.sbDelayValue_13)
        self.delayList.append(self.sbDelayValue_14)
        self.delayList.append(self.sbDelayValue_15)
        self.delayList.append(self.sbDelayValue_16)
        #
        self.sbDelayValue_1.setMaximum(self.sController._delayCost*255)
        self.sbDelayValue_1.setSingleStep(self.sController._delayCost)
        self.sbDelayValue_2.setMaximum(self.sController._delayCost*255)
        self.sbDelayValue_2.setSingleStep(self.sController._delayCost)
        self.sbDelayValue_3.setMaximum(self.sController._delayCost*255)
        self.sbDelayValue_3.setSingleStep(self.sController._delayCost)
        self.sbDelayValue_4.setMaximum(self.sController._delayCost*255)
        self.sbDelayValue_4.setSingleStep(self.sController._delayCost)
        self.sbDelayValue_5.setMaximum(self.sController._delayCost*255)
        self.sbDelayValue_5.setSingleStep(self.sController._delayCost)
        self.sbDelayValue_6.setMaximum(self.sController._delayCost*255)
        self.sbDelayValue_6.setSingleStep(self.sController._delayCost)
        self.sbDelayValue_7.setMaximum(self.sController._delayCost*255)
        self.sbDelayValue_7.setSingleStep(self.sController._delayCost)
        self.sbDelayValue_8.setMaximum(self.sController._delayCost*255)
        self.sbDelayValue_8.setSingleStep(self.sController._delayCost)
        self.sbDelayValue_9.setMaximum(self.sController._delayCost*255)
        self.sbDelayValue_9.setSingleStep(self.sController._delayCost)
        self.sbDelayValue_10.setMaximum(self.sController._delayCost*255)
        self.sbDelayValue_10.setSingleStep(self.sController._delayCost)
        self.sbDelayValue_11.setMaximum(self.sController._delayCost*255)
        self.sbDelayValue_11.setSingleStep(self.sController._delayCost)
        self.sbDelayValue_12.setMaximum(self.sController._delayCost*255)
        self.sbDelayValue_12.setSingleStep(self.sController._delayCost)
        self.sbDelayValue_13.setMaximum(self.sController._delayCost*255)
        self.sbDelayValue_13.setSingleStep(self.sController._delayCost)
        self.sbDelayValue_14.setMaximum(self.sController._delayCost*255)
        self.sbDelayValue_14.setSingleStep(self.sController._delayCost)
        self.sbDelayValue_15.setMaximum(self.sController._delayCost*255)
        self.sbDelayValue_15.setSingleStep(self.sController._delayCost)
        self.sbDelayValue_16.setMaximum(self.sController._delayCost*255)
        self.sbDelayValue_16.setSingleStep(self.sController._delayCost)
        ##############################################################
        
        self.sbDelayValue_1.editingFinished.connect(self.delayValueChange)
        self.sbDelayValue_2.editingFinished.connect(self.delayValueChange)
        self.sbDelayValue_3.editingFinished.connect(self.delayValueChange)
        self.sbDelayValue_4.editingFinished.connect(self.delayValueChange)
        self.sbDelayValue_5.editingFinished.connect(self.delayValueChange)
        self.sbDelayValue_6.editingFinished.connect(self.delayValueChange)
        self.sbDelayValue_7.editingFinished.connect(self.delayValueChange)
        self.sbDelayValue_8.editingFinished.connect(self.delayValueChange)
        self.sbDelayValue_9.editingFinished.connect(self.delayValueChange)
        self.sbDelayValue_10.editingFinished.connect(self.delayValueChange)
        self.sbDelayValue_11.editingFinished.connect(self.delayValueChange)
        self.sbDelayValue_12.editingFinished.connect(self.delayValueChange)
        self.sbDelayValue_13.editingFinished.connect(self.delayValueChange)
        self.sbDelayValue_14.editingFinished.connect(self.delayValueChange)
        self.sbDelayValue_15.editingFinished.connect(self.delayValueChange)
        self.sbDelayValue_16.editingFinished.connect(self.delayValueChange)
        #
        #
        self.btnCoilPush.setChecked(False)
        self.btnConnect.clicked.connect(self.connectButtonClick)
        self.btnRefresh.clicked.connect(self.refreshButtonClick)
        self.btnReadSettings.clicked.connect(self.readSetButtonClick)
        self.btnWriteSettings.clicked.connect(self.writeSetButtonClick)
        self.btnCoilPush.clicked.connect(self.coilButtonClick)
        self.btnWriteROM.clicked.connect(self.writeRomButtonClick)
        self.cbDeviceBaudRate.currentIndexChanged.connect(self.deviceBaudRateChange)
        self.cbDevicePduFormat.currentIndexChanged.connect(self.devicePduFormatChange)
        self.btnRefreshAuto.clicked.connect(self.refreshAutoButtonClick)
        #Таймер для обновления
        self.timer=QTimer()
        self.timer.timeout.connect(self.modbusUpdate)
        self.btnRefreshAuto.clicked.connect(self.modbusUpdate)
        #
        self.show()
        
    def refreshAutoButtonClick(self):
        if self.sender().isChecked():
            self.timer.start(self.globalTimeout)
        else:
            self.timer.stop()
            
    #Изменение настроек соединения на устройстве    
    def deviceBaudRateChange(self,index):
        try:
            self.sController._deviceBaudrate=int(self.cbDeviceBaudRate.currentText())
        except Exception as e:
            pass
        
    def devicePduFormatChange(self,index):
        try:
            self.sController.setPduStr(self.cbDevicePduFormat.currentText())
        except Exception as e:
            pass
    #
    #Автообновление. Ошибки игнорируются.
    def modbusUpdate(self):
        try:
            print('Timer works')
            if self.sController.isConnect():
                tmp=self.sController.mReadAiRegisters()
                self.tAnalogInput1.setText(str(self.sController._aiReg1))
                self.tAnalogInput2.setText(str(self.sController._aiReg2))
                self.tDigitalInput1.setText(self.sController._diReg1)
                self.setStates(self.sController._diReg1)
        except Exception as e:
            pass
        
    def test(self):
        try:
            print(self.sController._diReg1)
            self.setStates(self.sController._diReg1)
        except Exception as e:
            print(e)
            
    def setStates(self,arg):
        count=15
        for tmpObj in self.stateList:
            if arg[count]=='1':
                tmpObj.setChecked(True)
            else:
                tmpObj.setChecked(False)                
            count-=1
            
    #Изменение значений задержек
    def delayValueChange(self):
        try:
            sender=self.sender()
            tmpPos=self.delayList.index(sender)
            print(tmpPos,sender.value())
            self.sController.setDelay(tmpPos,sender.value())
            
            sender.setValue(self.sController.getDelay(tmpPos))
        except Exception as e:
            QMessageBox.critical(self,'Ошибка приложения!',str(e))
            
    def delayIndexChange(self,arg):
        try:
            tmp=self.sController.getDelay(arg)
            self.sbDelayValue.setValue(tmp)
        except Exception as e:
            QMessageBox.critical(self,'Ошибка приложения!',str(e))
    ##############################
            
    def writeRomButtonClick(self):
        try:
            self.sController.sWriteRom()
        except Exception as e:
            QMessageBox.critical(self,'Ошибка приложения!',str(e))
            
    def coilButtonClick(self):
        try:
            if self.btnCoilPush.isChecked():
                self.sController.mWriteCoil(0,1)
                self.btnCoilPush.setText('Coil on')                
            else:
                self.sController.mWriteCoil(0,0)
                self.btnCoilPush.setText('Coil off')
        except Exception as e:
            self.btnCoilPush.setChecked(False)
            QMessageBox.critical(self,'Ошибка приложения!',str(e))
        
    def listPorts(self):
        tmp=list_ports.comports()
        tmp.sort()
        for i in tmp:
            self.cbComPorts.addItem(i.device)
            
    def writeSetButtonClick(self):
        try:
            self.sController.sWriteSet()
            self.sController.sWriteDelays() 
        except Exception as e:
            QMessageBox.critical(self,'Ошибка приложения!',str(e))
        
    def readSetButtonClick(self):
        try:
            if self.sController.isConnect():
                #Настройки соединенияч
                self.sController.sReadSet()               
                tmp=self.cbBaudRateSets.findText(str(self.sController._deviceBaudrate))
                if tmp>0:
                    self.cbBaudRateSets.setCurrentIndex(tmp)

                tmp=self.cbPduFormatSets.findText(self.sController.getPduStr())
                if tmp>0:
                    self.cbPduFormatSets.setCurrentIndex(tmp)
                #Задержки
                self.sController.sReadDelays()
                self.updateDelays()
        except Exception as e:
            QMessageBox.critical(self,'Ошибка приложения!',str(e))
            
    def updateDelays(self):
        tmpCount=0
        for i in self.delayList:
            i.setValue(self.sController.getDelay(tmpCount))
            tmpCount+=1
            
    def refreshButtonClick(self):
        try:        
            if self.sController.isConnect():
                tmp=self.sController.mReadAiRegisters()
                self.tAnalogInput1.setText(str(self.sController._aiReg1))
                self.tAnalogInput2.setText(str(self.sController._aiReg2))
                self.tDigitalInput1.setText(self.sController._diReg1)
                self.setStates(self.sController._diReg1)
                
        except Exception as e:
            QMessageBox.critical(self,'Ошибка приложения!',str(e))
                
    def connectButtonClick(self):
        tmpName=self.btnConnect.text()
        try:
            if tmpName=='Connect':
                self.sController.setup(self.tSlaveAddress.text(),
                                       self.cbComPorts.currentText(),
                                       int(self.cbBaudRate.currentText()),
                                       timeout=self.globalTimeout,
                                       log=1,
                                       pduString=self.cbPduFormat.currentText()
                                       )
                self.sController.connect()
                #tmp=self.sController.isConnect()
                #print(tmp)
                self.btnConnect.setText('Disconnect')                
            else:
                self.disconnect()
                #tmp=self.sController.isConnect()
                #print(tmp)                
                self.btnConnect.setText('Connect')
        except Exception as e:
            QMessageBox.critical(self,'Ошибка приложения!',str(e))

    def disconnect(self):
        try:
            self.sController.close()
        except Exception as e:
            pass
        
    def closeEvent(self,event):
        self.disconnect()
        event.accept()
        
app=QApplication(sys.argv)
mainForm=MainForm()
sys.exit(app.exec_())
