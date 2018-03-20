import sys
from abc import ABCMeta, abstractmethod, abstractproperty
import CommonConnection
import time
class Protocols(metaclass = ABCMeta):
    _messages=(
            "Ок",
            "Не открыто соединение ",
            "Неверный формат ответа ",
            "Ожидается экземпляр класса CommonConnection! ",
            "Неверный формат параметра ",
            "Modbus Ошибка протокола ")
    #От этого класса наследуются Протоколы, которые связаны с источником данных
    #класс CommonConnection
    @abstractproperty
    def source():
        """Связанный источник"""
        return 'source'
    
    @abstractmethod
    def getName():
        pass
    
    def checkAddress(self,arg):
        if arg>247 or arg<0:
            raise Exception

class ModbusProtocol(Protocols):
    def __init__(self,arg,timeout=0.1):
        self.source=arg
        self.timeout=timeout
        
    @property
    def source(self):
        return self._source
    
    @source.setter
    def source(self,arg):
        if not isinstance(arg,CommonConnection.CommonConnection):
            raise Exception        
        self._source=arg
    def getName(self):
        pass
    
    def checkStartAddress(self,arg):
        """Проверка стартового адреса
        Вход:
            arg int адрес
        Выход:
            Исключение с кодом 2
        """
        if arg<0 and arg>65535:
            raise ValueError(2)
        
    def make16bits(self,arg):
        """Проверка стартового адреса
        Вход:
            arg int адрес
        Выход:
            bytes 2 байта big endian
        """
        return arg.to_bytes(2,'big')
    
    def regIntFromByteArray(self,arg):
        tmp=0
        result=list()
        while tmp<len(arg):
            result.append(int.from_bytes(arg[tmp:tmp+2],'big'))
            tmp+=2
        return result
            
    def checkQuantity(self,arg):
        if arg<1 and arg>125:
            raise ValueError(3)
        
    def writeSingleCoil(self,address,start,action):
        """Вкл/вкл реле
        Вход:
            address int адрес устройства
            start   int адрес катушки
            action  bool вкл\выкл True\False 
        """
        func=0x05
        error=0x85
        #Запрос
        try:
            self.checkAddress(address)
            self.checkStartAddress(start)
            tmpAction=bytearray([0x00,0x00])
            if action==True: tmpAction=bytearray([0xFF,0x00])
            request=bytearray([address,func])
            request+=self.make16bits(start)
            request+=tmpAction
            crc=self.calculateCrcString(request)
            #print(request,crc)
            request+=crc
            self.source.write(request)
        except Exception as e:
            raise e
        #Таймаут
        time.sleep(self.timeout)
        #Обработка ответа
        try:
            responce=self.source.read()
            #responce=bytearray([0x01,0x05,0x00,0x00,0xFF,0x00,0x8C,0x3A])
            tmpCount=responce[2]
            if not responce:
                raise ValueError(self._messages[2])
            if responce!=request:
                raise ValueError(self._messages[5]+str(tmpCount))           
        except Exception as e:
             raise e
        
    def readInputRegisters(self,address,start=1,count=1):
        """Чтение группы регистров
        Вход:
            address int адрес устройства
            start   int стартовый адрес
            count   int количество регистров
        """
        func=0x04
        error=0x84
        #Запрос
        try:
            self.checkAddress(address)
            self.checkStartAddress(start)
            self.checkQuantity(count)
            request=bytearray([address,func])
            request+=start.to_bytes(2,'big')
            request+=count.to_bytes(2,'big')
            crc=self.calculateCrcString(request)
            request+=crc
            self.source.write(request)
        except Exception as e:
            raise e
        #Таймаут
        time.sleep(self.timeout)
        #Обработка ответа
        try:
            #Длинна заголовка 1(addr)+1(func)+1(count*2) данные +2(crc)=5
            responce=self.source.read()
            #responce=bytearray([0x01,0x04,0x06,0x01,0x00,0x02,0x37,0x00,0x01,0x10,0xF4])
            #responce=bytearray([0x01,0x84,0x02])
            tmpLenResponce=len(responce)
            if not tmpLenResponce:
                raise ValueError(self._messages[2])
            tmpAddress=responce[0]
            tmpFunc=responce[1]
            tmpCount=responce[2]
            #print(tmpAddress,tmpFunc,tmpCount)
            #Ошибка протокола
            if tmpFunc==error:
                raise ValueError(self._messages[5]+str(tmpCount))
            if address!=tmpAddress or func!=tmpFunc or count!=tmpCount/2:
                raise ValueError(self._messages[2])
            tmpData=responce[3:tmpLenResponce-2]
            tmpCrc=responce[tmpLenResponce-2:]
            crc=self.calculateCrcString(responce[:tmpLenResponce-2])
            if crc!=tmpCrc:
                raise ValueError(self._messages[2])
            #print(tmpAddress,tmpFunc,tmpCount,tmpData,tmpCrc,crc)
        except Exception as e:
            raise e
        return tmpData
    
    def calculateCrcString(self,arg):
        """Вычисление CRC16 для  Modbus.
        Вход:
            Args    Bytes
        Выход:
            2 байта LH
        """
        if not isinstance(arg,bytearray):
            raise ValueError(self._messages[4])
        
        _CRC16TABLE = (
            0, 49345, 49537,   320, 49921,   960,   640, 49729, 50689,  1728,  1920, 
        51009,  1280, 50625, 50305,  1088, 52225,  3264,  3456, 52545,  3840, 53185, 
        52865,  3648,  2560, 51905, 52097,  2880, 51457,  2496,  2176, 51265, 55297, 
         6336,  6528, 55617,  6912, 56257, 55937,  6720,  7680, 57025, 57217,  8000, 
        56577,  7616,  7296, 56385,  5120, 54465, 54657,  5440, 55041,  6080,  5760, 
        54849, 53761,  4800,  4992, 54081,  4352, 53697, 53377,  4160, 61441, 12480, 
        12672, 61761, 13056, 62401, 62081, 12864, 13824, 63169, 63361, 14144, 62721, 
        13760, 13440, 62529, 15360, 64705, 64897, 15680, 65281, 16320, 16000, 65089, 
        64001, 15040, 15232, 64321, 14592, 63937, 63617, 14400, 10240, 59585, 59777, 
        10560, 60161, 11200, 10880, 59969, 60929, 11968, 12160, 61249, 11520, 60865, 
        60545, 11328, 58369,  9408,  9600, 58689,  9984, 59329, 59009,  9792,  8704, 
        58049, 58241,  9024, 57601,  8640,  8320, 57409, 40961, 24768, 24960, 41281, 
        25344, 41921, 41601, 25152, 26112, 42689, 42881, 26432, 42241, 26048, 25728, 
        42049, 27648, 44225, 44417, 27968, 44801, 28608, 28288, 44609, 43521, 27328, 
        27520, 43841, 26880, 43457, 43137, 26688, 30720, 47297, 47489, 31040, 47873, 
        31680, 31360, 47681, 48641, 32448, 32640, 48961, 32000, 48577, 48257, 31808, 
        46081, 29888, 30080, 46401, 30464, 47041, 46721, 30272, 29184, 45761, 45953, 
        29504, 45313, 29120, 28800, 45121, 20480, 37057, 37249, 20800, 37633, 21440, 
        21120, 37441, 38401, 22208, 22400, 38721, 21760, 38337, 38017, 21568, 39937, 
        23744, 23936, 40257, 24320, 40897, 40577, 24128, 23040, 39617, 39809, 23360, 
        39169, 22976, 22656, 38977, 34817, 18624, 18816, 35137, 19200, 35777, 35457, 
        19008, 19968, 36545, 36737, 20288, 36097, 19904, 19584, 35905, 17408, 33985, 
        34177, 17728, 34561, 18368, 18048, 34369, 33281, 17088, 17280, 33601, 16640, 
        33217, 32897, 16448)
        register = 0xFFFF
        for i in arg:
            register = (register >> 8) ^ _CRC16TABLE[(register ^ i) & 0xFF]
            
        try:
            result=register.to_bytes(2,'little')
        except:
            raise ValueError(self._messages[4])
        return result

class ServiceProtocol(Protocols):
    """Работает в синхронном режиме
        Запрос-Ответ
    """

    #Значения
    #Формат кадра
    _pduFormat={0x01:'8N2',0x02:'8E1',0x03:'8O1'}
    #Скорость
    _baudrate={
            0xCF:2400,
            0x67:4800,
	    0x33:9600,
	    0x19:19200,
	    0x0C:38400,
	    0x08:57600}
    
    def getName(self):
        return 'Hello!'
    
    def __init__(self,arg,timeout=0.1):
        self.source=arg
        self.timeout=timeout
        
    @property
    def source(self):
        return self._source
    
    @source.setter
    def source(self,arg):
        if not isinstance(arg,CommonConnection.CommonConnection):
            raise Exception
        self._source=arg
        
    def checkDelays(self,arg):
        if not isinstance(arg,bytearray):
            raise Exception                
        for i in arg:
            if i<1 and i>255:
                raise Exception
            
    def getFPduValue(self,arg):
        result=self._pduFormat.get(arg)
        if not result:
            raise Exception
        return result
    
    def getFPduKey(self,arg):
        result=''
        for i in self._pduFormat:
            if self._pduFormat[i]==arg:result=i
        if result=='':raise Exception
        return result
            
    def getBaudrateValue(self,arg):
        result=self._baudrate.get(arg)
        if not result:
            raise Exception
        return result
    
    def getBaudrateKey(self,arg):
        result=''
        for i in self._baudrate:
            if self._baudrate[i]==arg:result=i
        if result=='':raise Exception
        return result
    
    def readIntSettings(self):
        """Команда на считывание настроек соединения устройства
        Запрос FF AA 81
        Ответ  FE AA 81 Адрес Формат_кадра Скорость
        """
        command=bytearray([0xFE,0xAA,0x81])
        maxLen=6
        result=''        
        #посылка запроса
        try:
            self.source.write(command)
        except Exception as e:
            raise e       
        #задержка по таймауту 
        if self.timeout>0:
            time.sleep(self.timeout)
        #чтение ответа
        try:
            #responce=self.source.readTmp(command)
            responce=self.source.read()
            #print(responce)
            if len(responce)>maxLen:raise ValueError(self._messages[2]) 
            header=responce[:3]
            if responce[:3]!=command:raise ValueError(self._messages[2])
            #Заголовок ответа верный, проверяем аргументы
            address=responce[3]
            self.checkAddress(address)
            fpdu=self.getFPduValue(responce[4])
            baudrate=self.getBaudrateValue(responce[5])
        except Exception as e:
            raise ValueError(self._messages[2])
        result={'address':address,'fpdu':fpdu,'baudrate':baudrate}
        #print('Получено Адрес=',responce[3],' Формат=',responce[4],' Скорость=',responce[5])
        return result
    
    def writeIntSettings(self,address,fpdu,baudrate):
        """Команда на запись настроек соединения с устройством
        Запрос  FE AA 81 Адрес Формат_кадра Скорость
        Ответ   Эхо
        """
        command=bytearray([0xFE,0xAA,0x01])
        maxLen=6
        result=''
        try:
            self.checkAddress(int(address))
            command.append(int(address))
            command.append(self.getFPduKey(fpdu))
            command.append(self.getBaudrateKey(baudrate))
        except Exception as e:
            raise ValueError(self._messages[4])

        try:
            self.source.write(command)
            #задержка по таймауту 
            if self.timeout>0:
                time.sleep(self.timeout)
            #responce=self.source.readTmp(command)
            responce=self.source.read()
            #print('Получено',responce)            
            if responce!=command:
                raise ValueError(self._messages[2])
            #print(responce[5])
        except Exception as e:
            raise e
        
    def readDiSettings(self):
        """Команда на чтение задержек DI
        Запрос  FE AA 82
        Ответ   FE AA 82 16_байт_Значений_задержек
        """
        command=bytearray([0xFE,0xAA,0x82])
        maxLen=19
        result=''        
        #посылка запроса
        try:
            self.source.write(command)
        except Exception as e:
            raise e       
        #задержка по таймауту 
        if self.timeout>0:
            time.sleep(self.timeout)
        #чтение ответа
        try:
            #responce=self.source.readTmp(command)
            responce=self.source.read()
            #print('Получено',responce)
            if len(responce)>maxLen:raise ValueError(self._messages[2]) 
            header=responce[:3]
            if responce[:3]!=command:raise ValueError(self._messages[2])
            #Заголовок ответа верный, проверяем аргументы
            delays=responce[3:]
            self.checkDelays(delays)
        except Exception as e:
            raise ValueError(self._messages[2])
        result=delays
        #print(result)
        return result
    
    def writeDiSettings(self,arg):
        """Команда на запись задержек DI
        Запрос  FE AA 82
        Ответ   FE AA 82 16_байт_Значений_задержек
        """
        command=bytearray([0xFE,0xAA,0x02])
        maxLen=19
        maxLenArg=16
        result=''
        try:
            self.checkDelays(arg)
            command.extend(arg)
        except Exception as e:
            raise ValueError(self._messages[4])

        try:
            #посылка запроса
            self.source.write(command)
            #задержка по таймауту 
            if self.timeout>0:
                time.sleep(self.timeout)
            #чтение ответа
            #responce=self.source.readTmp(command)
            responce=self.source.read()
            #print('Получено',responce)            
            if responce!=command:
                raise ValueError(self._messages[2])
            #print(responce[5])
        except Exception as e:
            raise e
        
    def writeSettingsROM(self):
        """Команда на запись в ROM
        Запрос  FE AA EE
        Ответ   FE AA EE
        """
        command=bytearray([0xFE,0xAA,0xEE])
        maxLen=3       
        #посылка запроса
        try:
            self.source.write(command)
        except Exception as e:
            raise e       
        #задержка по таймауту 
        if self.timeout>0:
            time.sleep(self.timeout)
        #чтение ответа
        try:
            responce=self.source.read()
            header=responce[:3]
            if responce[:3]!=command:raise ValueError(self._messages[2])
        except Exception as e:
            raise ValueError(self._messages[2])
        
if __name__=="__main__":
    #con=CommonConnection.ConsoleConnection()
    #prot1=ServiceProtocol(con)
    #s=prot1.readIntSettings()
    #print(s)
    #prot1.writeIntSettings(23,'8N2',9600)
    #prot1.readDiSettings()
    #prot1.writeDiSettings(bytearray([6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6]))
    con=CommonConnection.ComConnection(port='COM7',baudrate=9600,log=1)
    #prot1=ServiceProtocol(con,1)
    #print(prot1.readIntSettings())
    #prot1.writeIntSettings(1,'8O1',9600)
    #prot1.readDiSettings()
    #prot1.writeDiSettings(bytearray([7,6,6,6,6,6,6,6,6,6,6,6,6,6,6,8]))
    #prot1.writeSettingsROM()
    prot1=ModbusProtocol(con,5)
    #s=prot1.calculateCrcString(bytes([0x01,0x05,0x00,0x00,0xFF,0x00]))
    #print(s,s[0],s[1])
    #print(prot1.readInputRegiters(1,0,3))
    prot1.writeSingleCoil(1,0,True)
    con.close()
