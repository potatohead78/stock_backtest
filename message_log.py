import os
from datetime import datetime

class Message_log():
    def __init__(self) -> None:
        os.makedirs('결과', exist_ok = True)
        self.log = open(f"결과/{datetime.now().strftime('%Y.%m.%d.%H%M%S')}.txt",'a+')
        print(datetime.now().strftime('[%m/%d %H:%M:%S]'), "시작", file = self.log)

    def printlog(self, message, *args) -> None:
        """메세지를 출력하고 저장함.
        
        Args: message (str): 메세지
        """
        print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message, *args)
        print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message, *args, file = self.log)

    def log_exit(self):
        self.log.close()