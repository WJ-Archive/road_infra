from collections import deque

class Data_Queue():
    def __init__(self):
        que_len = 1

        self.latlon_buf = deque([], maxlen=2)

        #self.lux_buf = deque([0 for i in range(que_len)], maxlen=que_len)
        #self.temp_buf = deque([0 for i in range(que_len)], maxlen=que_len)
        #self.humi_buf = deque([0 for i in range(que_len)], maxlen=que_len)
        #self.acc_x_buf = deque([0 for i in range(que_len)], maxlen=que_len)
        #self.acc_y_buf = deque([0 for i in range(que_len)], maxlen=que_len)
        #self.acc_z_buf = deque([0 for i in range(que_len)], maxlen=que_len)
        #self.pth_buf = deque([0 for i in range(que_len)], maxlen=que_len)

        self.lux_buf = deque([0],maxlen=que_len)
        self.temp_buf = deque([0],maxlen=que_len)
        self.humi_buf = deque([0],maxlen=que_len)
        self.acc_x_buf = deque([0],maxlen=que_len)
        self.acc_y_buf = deque([0],maxlen=que_len)
        self.acc_z_buf = deque([0],maxlen=que_len)
        self.pth_buf = deque([0],maxlen=que_len)

        self.acc_xyz = deque([self.acc_x_buf[0], self.acc_y_buf[0], self.acc_z_buf[0]], maxlen=3)
        self.det_buf = deque(maxlen=que_len)
        self.front_frame_buf = deque(maxlen=1)
        self.back_frame_buf = deque(maxlen=1)

        self.save_flag = 0

