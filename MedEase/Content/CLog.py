import datetime
import os.path 
import os
from typing import Self






class CustomLog:
    FileLog = None
    _instance = None
    def __new__(cls, *args, **vargs) -> Self:
        if cls._instance == None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @staticmethod
    def Get():
        return CustomLog._instance
    
    def __init__(self):
        
        self.__timeNow = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.__name = os.path.abspath('logs\\' + 'log_' + self.__timeNow + '.txt')
        self.fLog = open(file = self.__name, mode = 'w', newline='\n')
        self.Info("Logging On")
        # self._EraseOldLogFiles(10)
        CustomLog.FileLog = self.fLog
    
    def __del__(self):
        CLog.Info('Log Class Begin Destruction')
        self.Info('Logging Off')
        CLog.Info('Log Class End Destruction')
        print('\n\n\n')
        self.fLog.write('\n\n\n')
        self.fLog.close()

    def _EraseOldLogFiles(self, logsCountToKeep: int):
        path = os.path.abspath('logs')
        dirs = os.listdir(path)
        dirs.sort( reverse=False )
        for i in range(len(dirs)):
            dirs[i] = os.path.join(path, dirs[i])
            
        if (len(dirs) > logsCountToKeep):
            countDel = len(dirs) - logsCountToKeep
            for i in range(countDel):
                os.remove(dirs[i])
        
    def Info(self, msg: str = "", end="\n"):
        print("\x1b[36m" +
                "Infos   : " + msg + end + "\x1b[0m", end='')
        self.fLog.write("Infos   : " + msg + end)

    def Trace(self, msg: str = "", end="\n"):
        print("\x1b[32m" +
                "Traces  : " + msg + end + "\x1b[0m", end='')
        self.fLog.write("Traces  : " + msg + end)

    def Warn(self, msg: str = "", end="\n"):
        print("\x1b[33m" +
                "Warning : " + msg + end + "\x1b[0m", end='')
        
        self.fLog.write("Warning : " + msg + end)

    def Error(self, msg: str = "", end="\n"):
        print("\x1b[31m" +
                "Errors  : " + msg + end + "\x1b[0m", end='')
        
        self.fLog.write("Errors  : " + msg + end)

    def Fatal(self, msg: str = "", end="\n"):
        print("\x1b[35m" + "Fatals  : " + msg + end + "\x1b[0m", end='')
        self.fLog.write("Fatals  : " + msg + end)
        
        raise Exception(__file__)

    def Log(self, msg: str, R: int = 255, G: int = 255, B: int = 255, end: str = "\n"):
        print(f"\x1b[38;2;{R};{G};{B}m" + "Custom  : " + msg + end + "\x1b[0m", end='')
        self.fLog.write("Custom  : " + msg + end)
        

    def Input(self, msg: str = "", R: int = 255, G: int = 255, B: int = 255, end: str = "\n"):
        print(f"\x1b[38;2;{R};{G};{B}m" + "\n          " + msg + end + "\x1b[0m", end='')
        return input()


CLog = CustomLog()

if __name__ == '__main__':
    CLog.Log("this is Log", R = 150, G = 20,B = 20)
    CLog.Info("this is info")
    CLog.Trace("this is trace")
    CLog.Warn("this is Warning")
    CLog.Error("this is error")
    CLog.Fatal("this is fatal")
    pass

