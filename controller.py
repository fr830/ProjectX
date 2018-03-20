import sys
from CommonConnection import ComConnection
import Protocols

_address=1
_port='COM7'
_baudrate=9600
_parity='N'
_stopbit=2
_readTimeout=0
_writeTimeout=0
_timeout=5
_delays=bytearray([6,6,6,6,6,6,6,6,6,0,0,0,0,0,0,0])
_delayM=8.16

tips=(
    'settings port={0} baudrate={1} parity={2} stopbit={3} r/timeout={4} w/timeeout={5}',
    'connect создать соединение с текущими настройками',
    'setup  изменить текущие настройки',
    'Оk',
    'Неудачно'
    )

def mWriteCoil():
    try:
        tmpStartAddress=int(input('Адрес реле (0-65535)='))
        tmpAction=bool(int(input('Вкл\Выкл (1\0)=')))
        _prot2.writeSingleCoil(_address,tmpStartAddress,tmpAction)
        print(tips[3])
    except Exception as e:
        print(e)
        
def mReadRegister():
    try:
        tmpStartAddress=int(input('Адрес регистра (0-65535)='))
        print(_prot2.readInputRegisters(_address,tmpStartAddress,3))
        print(tips[3])
    except Exception as e:
        print(e)
        
def listDelays():
    tmp=''
    for i in _delays:
        tmp+=str(i*_delayM)+' '
    print(tmp)
    
def sReadDelays():
    try:
        global _delays
        _delays=_prot1.readDiSettings()
        print(tips[3])
    except Exception as e:
        print(e)
        
def sWriteDelays():
    try:
        _prot1.writeDiSettings(_delays)
        print(tips[3])
    except Exception as e:
        print(e)
        
def sSetDelay():
    try:
        tmpAddress=int(input('Номер (0-15)='))
        tmpValue=int(input('Значение (0-255)='))
        global _delays
        _delays[tmpAddress]=tmpValue
        print(tips[3])        
    except Exception as e:
        print(e)
        
def sReadSet():
    try:
        result=_prot1.readIntSettings()
        print(result)
        global _baudrate
        global _parity
        global _stopbit
        _baudrate=result['baudrate']
        tmp=result['fpdu']
        _parity=tmp[1]
        _stopbit=tmp[2]
        print(result['baudrate'],result['fpdu'],_baudrate,_parity)
    except Exception as e:
        print(e)
        
def sWriteSet():
    try:
        _prot1.writeIntSettings(_address,'8'+_parity+str(_stopbit),_baudrate)
        print(tips[3])
    except Exception as e:
        print(e)
        
def listSet():
    print(tips[0].format(_port,_baudrate,_parity,_stopbit,_readTimeout,_writeTimeout))
    
def setup():
    #Настройки
    try:
        global _address
        _address=int(input('Адрес='))
        
        global _baudrate
        _baudrate=int(input('Скорость='))
        
        global _port
        _port=input('Имя порта=')
        
        global _parity
        tmp=input('Формат кадра [N|O|E] (N)=')
        if tmp!='':
            _parity='N'
            
        global _stopbit
        tmp=input('Стопбит [1|2] (1)=')
        if tmp!='':
            _stopbit=int(tmp)
        else:
            _stopbit=1
            
        global _timeout
        tmp=input('Глобальный таймаут (0.1)=')
        if tmp!='':
            _timeout=float(tmp)
        else:
            _timeout=0.1
            
        if not _port or not _baudrate:
            raise ValueError('Не указан порт,скорость или формат кадра!')
        print(tips[3])
    except Exception as e:
        print(e)
        print('Ошибка при вводе команды')
        
def connect():
    #Подкллючение
    try:
        if _stopbit and _parity:
            global _con
            _con=ComConnection(_port,_baudrate,_parity,_stopbit,log=1)
        else:
            _con=ComConnection(_port,_baudrate)
        if _con.isOpen:
            global _prot1
            _prot1=Protocols.ServiceProtocol(_con,_timeout)
            global _prot2
            _prot2=Protocols.ModbusProtocol(_con,_timeout)
            print(tips[3])
        else:
            print(tips[4])
    except Exception as e:
        print(tips[4])
        print(e)
        
def helpMe():
    print('#Доступные команды#')
    print('setup\tнастройки соединения')
    print('connect\tустановить соединение с текущими настройками')
    print('close\tзакрыть соединение')
    print('ls\tизменить текущие настройки соединения')
    print('rs\tсчитать настройки соединения с устройства')
    print('ws\tзаписать текущие настройки на устройство')
    print('delays\tтекущие значения задержек')
    print('sd\tизменить значение задержки')
    print('rd\tсчитать задержки с устройства')
    print('wd\tзаписать текущие значения задержек на устройство')
    print('mrr\tсчитать регистр')
    print('mwc\tуправление реле')
    print('exit\tвыход')
    print('? help\tпомощь')
    
def close():
    try:
        _con.close()
    except Exception as e:
        pass
    
#Консольный контроллер
print(u'###Консольный контроллер v0.01###')
print(u'Перечень команд ?')

while True:
    tmpInput=input('>')
    tmpInput=tmpInput.split(' ')
    command=tmpInput[0]
    if command=='setup':
        setup()
    if command=='help' or command=='?':
        helpMe()
    if command=='connect':
        connect()
    if command=='close':
        close()
    if command=='exit':
        close()
        break
    if command=='ls':
        listSet()
    if command=='rs':
        sReadSet()
    if command=='ws':
        sWriteSet()
    if command=='delays':
        listDelays()
    if command=='rd':
        sReadDelays()
    if command=='wd':
        sWriteDelays()
    if command=='sd':
        sSetDelay()
    if command=='mrr':
        mReadRegister()
    if command=='mwc':
        mWriteCoil()
    if command=='about':
        print('#copyright Software Burnin Hardware Shevcov#')
