import sys
from CommonConnection import ComConnection
import Protocols

class Controller():
    #Контроллер программы#
    #********************#
    #Сообщения#
    _tips=(
        'Неверные настройки соединения! ',
        'Не удалось создать соединение! '
    )
    #
    def __init__(self):
        self._address=1
        #настройки соединения
        self._port='COM1'
        self._baudrate=9600
        self._parity='N'
        self._stopbit=2
        #настройки связи на устройстве
        self._deviceBaudrate=9600
        self._deviceParity='N'
        self._deviceStopbit=2
        #
        self._readTimeout=0
        self._writeTimeout=0
        self._timeout=5
        self._rTimeout=0.01
        self._wTimeout=0.01
        self._delays=bytearray([6,6,6,6,6,6,6,6,6,0,0,0,0,0,0,15])
        self._delayCost=8.16
        self._aiCost=4.887585
        self._log=0
        self._aiReg1=0
        self._aiReg2=0
        self._diReg1='{0:016b}'.format(0)

        
    def setup(self,address,port,baudrate,parity='N',stopbit=2,timeout=0.1,rTimeout=0.01,wTimeout=0.01,log=0,pduString=''):
        #Настройки
        try:
            #self._diReg1='{0:016b}'.format(45300)
            
            self._address=int(address)
        
            self._baudrate=baudrate
        
            self._port=port
        
            self._parity=parity
            
            self._stopbit=stopbit
            
            self._timeout=timeout
    
            self._rTimeout=rTimeout

            self._wTimeout=wTimeout

            self._log=log

            if pduString:
                self.setPduStr(pduString)
                
            if not self._port or not self._baudrate:
                raise ValueError(self._tips[0])
        except Exception as e:
            raise Exception(self._tips[0]+e.args[0])

    def connect(self):
        #Подключение
        try:
            self._con=ComConnection(
                self._port,
                self._baudrate,
                self._parity,
                self._stopbit,
                self._rTimeout,
                self._wTimeout,
                self._log)
        
            if self._con.isOpen:
                self._prot1=Protocols.ServiceProtocol(self._con,self._timeout)
                self._prot2=Protocols.ModbusProtocol(self._con,self._timeout)
            else:
                ValueError(self._tips[1])
        except Exception as e:
            raise Exception(e)

    def close(self):
        try:
            self._con.close()
            del(self._prot1)
            del(self._prot2)
        except Exception as e:
            pass
    
    def isConnect(self):
        try:
            return self._con.isOpen()        
        except:
            return False
        return False

    def mReadAiRegisters(self):
        try:
            tmp=self._prot2.readInputRegisters(self._address,0,3)
            print(tmp)
            self._diReg1='{0:016b}'.format(int.from_bytes(tmp[0:2],'little'))
            self._aiReg1=self._aiCost*int.from_bytes(tmp[2:4],'big')
            self._aiReg2=self._aiCost*int.from_bytes(tmp[4:6],'big')
        except Exception as e:
            raise e
        
    def sReadSet(self):
        try:
            result=self._prot1.readIntSettings()
            print(result)
            self._deviceBaudrate=result['baudrate']
            tmp=result['fpdu']
            self._deviceParity=tmp[1]
            self._deviceStopbit=tmp[2]
            return result
        except Exception as e:
            raise e
            
    def sReadDelays(self):
        try:
            self._delays=self._prot1.readDiSettings()            
        except Exception as e:
            raise e
        
    def sWriteSet(self):
        try:
            self._prot1.writeIntSettings(self._address,self.getPduStr(),self._deviceBaudrate)
        except Exception as e:
            raise e        
    #Под формат pdu Размер_кадра|Чётность|Стопбит
    #В
    def getPduStr(self):
        return '8'+self._deviceParity+str(self._deviceStopbit)
                 
    #Из
    def setPduStr(self,arg):
        try:
            if len(arg)<3:
                return
            #длинна кадра
            #self.length=arg[0]
            self._deviceParity=arg[1]
            self._deviceStopbit=int(arg[2])
        except Exception as e:
            raise e
        
    def getDelay(self,arg):
        try:
            return self._delayCost*self._delays[arg]
        except Exception as e:
            raise e
        
    def setDelay(self,index,arg):
        try:
            self._delays[index]=int(arg/self._delayCost)
        except Exception as e:
            raise e
        
    def sWriteDelays():
        try:
            _prot1.writeDiSettings(self._delays)
        except Exception as e:
            raise e

    def mWriteCoil(self,address,action):
        try:
            self._prot2.writeSingleCoil(self._address,address,action)
        except Exception as e:
            raise e
        
    def sWriteRom(self):
        try:
            self._prot1.writeSettingsROM()
        except Exception as e:
            raise e
        
if __name__=="__main__":
    cntrl=Controller()
    cntrl.setup(1,'COM6',9600)
    cntrl.connect()
    print(cntrl.isConnect())
    cntrl.close()
