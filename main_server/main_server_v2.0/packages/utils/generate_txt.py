import logging
from PyQt5.QtCore import QThread, pyqtSignal
import time
import random

class TestTxt(QThread):
    signal = pyqtSignal(str, str)

    def __init__(self, model, sem):
        super().__init__()
        self._model = model #추가 #deque([[cls,x,y,w,h,...],[cls,x,y,w,h],],maxlen=10)
        self._sem = sem     #추가
        # Log format 설정
        FORMAT = '%(asctime)s : %(message)s'
        logging.basicConfig(format=FORMAT)

        # queue 및 변수 설정
        self.test_info = ["WARNING", "ERR"]

    def run(self) -> None:
        """
        스테드 run
        @params: None
        @return: None
        """
        
        #for i in range(30):

            # TODO: 통합시 수정요망
            # random info - test용
            #self._sem.acquire()
            #rand_no = random.randint(0, 1)
            #info = self.test_info[rand_no]

            # 메시지 작성
            # msg = f"[{info}] test 목적으로 log 데이터를 보냅니다."
            # if info == "INFO":
            #     logging.info(test_msg)
            # elif info == "WARNING":
            #     logging.warning(test_msg)
            # elif info == "ERR":
            #     logging.error(test_msg)
            #self._sem.release()
            #time.sleep(0.1)

            # data를 외부에 전달
            #self.signal.emit(info, msg)

        while(1):
            self._sem.acquire()
            if(len(self._model.lux_buf)):
                lux = float(self._model.lux_buf[-1])                
                ...
            
            if(len(self._model.temp_buf)):
                temp = float(self._model.temp_buf[-1])
                if(temp > 27 and temp <= 28):
                    info = "WARNING"
                    msg = f"[{info}] TEST.. 현재 온도는 {temp} 입니다"
                    self.signal.emit(info, msg)
                elif(temp > 28):
                    info = "ERR"
                    msg = f"[{info}] TEST.. 온도가 너무 높습니다. 현재온도 : {temp}"
                    self.signal.emit(info, msg)
                ...
            
            if(len(self._model.humi_buf)):
                humi = float(self._model.humi_buf[-1])
                if(humi > 60 and humi <= 63):
                    info = "WARNING"
                    msg = f"[{info}] TEST.. 현재 습도는 {humi} 입니다."
                    self.signal.emit(info, msg)
                elif(humi > 63):
                    info = "ERR"
                    msg = f"[{info}] TEST.. 습도가 너무 높습니다. 현재습도 : {humi}"
                    self.signal.emit(info, msg)
                ...
            #진동값은 주기가 10hz 라서 0.5초 sleep 주면 잘 출력 안됨
            """if(len(self._model.acc_z_buf)):
                acc_z = float(self._model.acc_z_buf[-1])
                print("??? acc_z",acc_z)
                if(acc_z > abs(2) and acc_z <= abs(3)):
                    info = "WARNING"
                    msg = f"[{info}] 진동이 발생했습니다. ACC_Z : {acc_z}"
                    self.signal.emit(info, msg)
                elif(acc_z > abs(3)):
                    info = "ERR"
                    msg = f"[{info}] 큰 진동 발생. ACC_Z : {acc_z}"
                    self.signal.emit(info, msg)"""

            """
            if(len(self._model.det_buf)):
                self.det = self._model.det_buf.pop()
                print("???????",self._model.det_buf)
                info = "DET"
                msg = f"[{info}] {self.det[0]}, Conf : {self.det[2]} "
                self.signal.emit(info, msg)
            """
            self._sem.release()
            time.sleep(0.5)
            ...


    def quitThread(self) -> None:
        """
        스레드 중지
        @params: None
        @return: None
        """
        self.quit()
