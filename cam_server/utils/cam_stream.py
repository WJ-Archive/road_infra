# -----------------------------------------------------------------------------
# Copyright (c) 2022, Lucid Vision Labs, Inc.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# -----------------------------------------------------------------------------

from arena_api.system import system
from arena_api.buffer import *

import ctypes
import numpy as np
import cv2
import time

#change code

"""
demonstrates live stream
(1) Start device stream
(2) Get a buffer and create a copy
(3) Requeue the buffer
(4) Calculate bytes per pixel for reshaping
(5) Create array from buffer cpointer data
(6) Create a NumPy array with the image shape
(7) Display the NumPy array using OpenCV
(8) When Esc is pressed, stop stream and destroy OpenCV windows
"""

class Stream_Vision_Cam:
    def __init__(self):
        
        self.width = 640
        self.height = 480           
        self.pixelformat = 'BGR8'
        self.curr_frame_time = 0
        self.prev_frame_time = 0        
        self.fc = 0                 #frame Count

    def __del__(self):
        self.device.stop_stream()   #End Stream
        system.destroy_device()     #Clear Device

    
    def setup(self):
        
        print('\nWARNING:\nTHIS EXAMPLE MIGHT CHANGE THE DEVICE(S) SETTINGS!')
        print('\nCam Setup started... \n')

        self.devices = self.create_devices_with_tries()     # waits for the user to connect a device before raising
        self.device = self.devices[0]                   

        self.nodemap = self.device.nodemap
        self.nodes = self.nodemap.get_node(['Width', 'Height', 'PixelFormat'])

        self.nodes['Width'].value = self.width
        self.nodes['Height'].value = self.height
        self.nodes['PixelFormat'].value = self.pixelformat

        self.num_channels = 3

        # Stream nodemap
        self.tl_stream_nodemap = self.device.tl_stream_nodemap
        self.tl_stream_nodemap["StreamBufferHandlingMode"].value = "NewestOnly"
        self.tl_stream_nodemap['StreamAutoNegotiatePacketSize'].value = True
        self.tl_stream_nodemap['StreamPacketResendEnable'].value = True
        
        
        
        print('\nStart Stream... \n')
        self.device.start_stream() # Start Stream


    def create_devices_with_tries(self):
        print("search CAM")
        tries = 0
        tries_max = 6
        sleep_time_secs = 10

        while tries < tries_max:  # Wait for device for 60 seconds
            devices = system.create_device()
            if not devices:
                print(
                    f'Try {tries+1} of {tries_max}: waiting for {sleep_time_secs} '
                    f'secs for a device to be connected!')
                for sec_count in range(sleep_time_secs):
                    time.sleep(1)
                    print(f'{sec_count + 1 } seconds passed ',
                        '.' * sec_count, end='\r')
                tries += 1
            else:
                print(f'Created {len(devices)} device(s)')
                return devices
        else:
            raise Exception(f'No device found! Please connect a device and run '
                            f'the example again.')

    
    # Due to yolov5 LoadStream structure, one frame should be taken...
    def capture(self):
        #print("Cap1")

        #with self.device.start_stream():      
        self.curr_frame_time = time.time()     # Used to display FPS on stream
        self.buffer = self.device.get_buffer() # Copy buffer and requeue to avoid running out of buffers
        self.item = BufferFactory.copy(self.buffer)
        self.device.requeue_buffer(self.buffer)

        self.buffer_bytes_per_pixel = int(len(self.item.data)/(self.item.width * self.item.height))
        self.array = (ctypes.c_ubyte * self.num_channels * self.item.width * self.item.height).from_address(ctypes.addressof(self.item.pbytes)) # Buffer data as cpointers can be accessed using buffer.pbytes
        
        self.npndarray = np.ndarray(buffer=self.array, dtype=np.uint8, shape=(self.item.height, self.item.width, self.buffer_bytes_per_pixel)) # Create a reshaped NumPy array to display using OpenCV
        self.fps = 1/(self.curr_frame_time - self.prev_frame_time)
        self.fc += 1

        BufferFactory.destroy(self.item) # Destroy the copied item to prevent memory leaks
        self.prev_frame_time = self.curr_frame_time
    
        return self.npndarray, self.fps

    """
    
    def stream(self):
        curr_frame_time = 0
        prev_frame_time = 0

        with self.device.start_stream():
 
            while True:

                self.fc += 1
                # Used to display FPS on stream
                curr_frame_time = time.time()
                buffer = self.device.get_buffer() # Copy buffer and requeue to avoid running out of buffers
                item = BufferFactory.copy(buffer)
                self.device.requeue_buffer(buffer)
                buffer_bytes_per_pixel = int(len(item.data)/(item.width * item.height))
                array = (ctypes.c_ubyte * num_channels * item.width * item.height).from_address(ctypes.addressof(item.pbytes)) # Buffer data as cpointers can be accessed using buffer.pbytes
                self.npndarray = np.ndarray(buffer=array, dtype=np.uint8, shape=(item.height, item.width, buffer_bytes_per_pixel)) # Create a reshaped NumPy array to display using OpenCV
                self.fps = round(1/(curr_frame_time - prev_frame_time),2)
                BufferFactory.destroy(item) # Destroy the copied item to prevent memory leaks
                prev_frame_time = curr_frame_time
            
            self.device.stop_stream()
        system.destroy_device()
    """
    






    
# if __name__ == '__main__':
    # test = Stream_Vision_Cam()
	
'''
Live Stream: Introduction
    This example introduces the basics of running a live stream 
    from a single device. This includes creating a device, selecting
    up stream dimensions, getting bufferprint('\nWARNING:\nTHIS EXAMPLE MIGHT CHANGE THE DEVICE(S) SETTINGS!') cpointer data, creating an
    array of the data and reshaping it to fit image dimensions using
    NumPy and displaying using OpenCV-Python.
'''

'''
#original code
def create_devices_with_tries():
	"""
	This function waits for the user to connect a device before raising
		an exception
	"""

	tries = 0
	tries_max = 6
	sleep_time_secs = 10
	while tries < tries_max:  # Wait for device for 60 seconds
		devices = system.create_device()
		if not devices:
			print(
				f'Try {tries+1} of {tries_max}: waiting for {sleep_time_secs} '
				f'secs for a device to be connected!')
			for sec_count in range(sleep_time_secs):
				time.sleep(1)
				print(f'{sec_count + 1 } seconds passed ',
					'.' * sec_count, end='\r')
			tries += 1
		else:
			print(f'Created {len(devices)} device(s)')
			return devices
	else:
		raise Exception(f'No device found! Please connect a device and run '
						f'the example again.')


def setup(device):
    """
    Setup stream dimensions and stream nodemap
        num_channels changes based on the PixelFormat
        Mono 8 would has 1 channel, RGB8 has 3 channels
    """
    nodemap = device.nodemap
    nodes = nodemap.get_node(['Width', 'Height', 'PixelFormat'])

    nodes['Width'].value = 1280
    nodes['Height'].value = 720
    nodes['PixelFormat'].value = 'BGR8'

    num_channels = 3

    # Stream nodemap
    tl_stream_nodemap = device.tl_stream_nodemap

    tl_stream_nodemap["StreamBufferHandlingMode"].value = "NewestOnly"
    tl_stream_nodemap['StreamAutoNegotiatePacketSize'].value = True
    tl_stream_nodemap['StreamPacketResendEnable'].value = True

    return num_channels


def example_entry_point():
    """
    demonstrates live stream
    (1) Start device stream
    (2) Get a buffer and create a copy
    (3) Requeue the buffer
    (4) Calculate bytes per pixel for reshaping
    (5) Create array from buffer cpointer data
    (6) Create a NumPy array with the image shape
    (7) Display the NumPy array using OpenCV
    (8) When Esc is pressed, stop stream and destroy OpenCV windows
    """

    devices = create_devices_with_tries()
    device = devices[0]

    # Setup
    num_channels = setup(device)

    curr_frame_time = 0
    prev_frame_time = 0

    with device.start_stream():
        """
        Infinitely fetch and display buffer data until esc is pressed
        """
        while True:
            # Used to display FPS on stream
            curr_frame_time = time.time()

            buffer = device.get_buffer()
            """
            Copy buffer and requeue to avoid running out of buffers
            """
            item = BufferFactory.copy(buffer)
            device.requeue_buffer(buffer)

            buffer_bytes_per_pixel = int(len(item.data)/(item.width * item.height))
            """
            Buffer data as cpointers can be accessed using buffer.pbytes
            """
            array = (ctypes.c_ubyte * num_channels * item.width * item.height).from_address(ctypes.addressof(item.pbytes))
            """
            Create a reshaped NumPy array to display using OpenCV
            """
            npndarray = np.ndarray(buffer=array, dtype=np.uint8, shape=(item.height, item.width, buffer_bytes_per_pixel))
            
            fps = str(1/(curr_frame_time - prev_frame_time))
            cv2.putText(npndarray, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)

            cv2.imshow('Lucid', npndarray)
            """
            Destroy the copied item to prevent memory leaks
            """
            BufferFactory.destroy(item)

            prev_frame_time = curr_frame_time

            """
            Break if esc key is pressed
            """
            key = cv2.waitKey(1)
            if key == 27:
                break
            
        device.stop_stream()
        cv2.destroyAllWindows()
    
    system.destroy_device()


if __name__ == '__main__':
	print('\nWARNING:\nTHIS EXAMPLE MIGHT CHANGE THE DEVICE(S) SETTINGS!')
	print('\nExample started\n')
	example_entry_point()
	print('\nExample finished successfully')
'''