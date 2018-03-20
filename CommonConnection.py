import sys
import serial
from abc import ABCMeta, abstractmethod, abstractproperty

#От этого класса наследуются все испочники данных
class CommonConnection(metaclass = ABCMeta):
    @abstractmethod
    def close(self):
        """Закрыть подключение"""
        
    @abstractmethod    
    def write(self):
        """Отправить данные в источник"""
    def read(self):
        """Читать данные из источника"""
    @abstractmethod
    def isOpen(self):
        """Проверка доступности подключения"""
    def toHex(self,arg):
        """Вывод в формате 0x00 0x00"""
        tmp=arg.hex()
        result=''
        index=0
        while index<len(tmp):
            result+=tmp[index:index+2]+' '
            index+=2
        return result
    
class ComConnection(CommonConnection):
    messages=("Ок","Не открыто соединение","Не открыто соединение")
    
    def __init__(self,port='',baudrate=9600,parity='N',stopbits=1,readTimeout=0,writeTimeout=0,log=0):
        try:
            self.__connection=serial.Serial()
            self.__connection.port=port

            self.__connection.baudrate=baudrate
            self.__connection.parity=parity
            self.__connection.stopbits=stopbits
            self.__connection.timeout=readTimeout
            self.__connection.write_timeout=writeTimeout
            self.__log=log
            self.__connection.open()
        except Exception as e:
            raise Exception('Ошибка создания подключения./r Сообщение '+e.args[0])
            
    def close(self):
        self.__connection.close()

    def write(self,arg):
        if not self.__connection.is_open:
            raise messages[1]
        if isinstance(arg,bytearray):
            self.__connection.reset_input_buffer()
            self.__connection.write(arg)
            if self.__log:print('-->'+self.toHex(arg))            
        elif isinstance(arg,str):
            self.__connection.write(arg.encode('cp866'))
            
    def read(self):
        if not self.__connection.is_open:
            raise messages[1]
        result=bytearray()
        while self.__connection.in_waiting>0:
            result+=self.__connection.read(1)
        if self.__log:print('<--'+self.toHex(result))
        return result
    
    def isOpen(self):
        return self.__connection.is_open

class ConsoleConnection(CommonConnection):
    def __init__(self):
        pass
    def open(self):
        pass
    def close(self):
        pass
    def readTmp(self,arg):
        if arg==bytearray(b'\xfe\xaa\x81'):
            return bytearray(b'\xFE\xAA\x81\x01\x03\x19')
        if arg==bytearray(b'\xfe\xaa\x01\x17\x013'):
            return bytearray(b'\xfe\xaa\x01\x17\x013')
        if arg==bytearray(b'\xfe\xaa\x82'):
            return bytearray(b'\xFE\xAA\x82\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06')
        if arg==bytearray(b'\xFE\xAA\x02\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06'):
            return bytearray(b'\xFE\xAA\x02\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06')        
        return bytearray(b'\xff')
    def read(self):
        result=input('>')
        return(result)
        
    def write(self,arg):
        print(arg)
    def isOpen(self):
        return 'stdout'

if __name__=="__main__":
    try:
        con=ComConnection('COM7',9600,'N')
        print(con.isOpen())
        con.write("ZZZZZZZZZzzzzzzzzzzzzz")
        print(con.read())
        con.close()
        print(con.isOpen())
    except Exception as e:
        print(e)

    con2=ConsoleConnection()
    con2.write("Fuck the society!")
    print(con2.read())
    con2.close()
