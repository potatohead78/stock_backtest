import os
from datetime import datetime

class Message_log():
    def __init__(self) -> None:
        os.makedirs('결과', exist_ok = True)
        self.log = open('결과/' + datetime.today().strftime('%Y.%m.%d') + '.txt','a+')

    def printlog(self, message, *args) -> None:
        """메세지를 출력하고 저장함.
        
        Args: message (str): 메세지
        """
        print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message, *args)
        print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message, *args, file = self.log)

    def log_exit(self):
        self.log.close()