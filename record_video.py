from threading import Thread
import cv2
from datetime import datetime, timedelta
import base64
import zmq
import time

# Generate timestamp for filenames
dtime = datetime.now().strftime('%m-%d-%Y_%H-%M-%S')
filename = '/home/pi/Desktop/UserName/Box_1/Top/Mouse1_T_' + dtime + '.mkv'
txtfile = '/home/pi/Desktop/UserName/Box_1/Top_Data/Mouse1_T_' + dtime + '.txt'

class SaveVideoStream:
    """
    Class that continuously captures frames from a video source and saves them with timestamps.
    Runs in a dedicated thread to ensure real-time video processing.
    """
    def __init__(self, src, ts, count):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.stream.set(cv2.CAP_PROP_FPS, 30)
        
        self.src = src
        self.grabbed, self.frame = self.stream.read()
        self.switchtime = datetime.now() + timedelta(hours=3)  # Duration before switching video file
        self.ts = datetime.now().strftime('%Y_%m_%d_%H:%M:%S.%f')
        self.ts1 = datetime.now().strftime('%m%d%Y %H:%M')
        
        self.count = count  # Frame counter
        self.fn = filename  # Output video filename
        self.txtfile = txtfile  # Output text file for timestamps

        # Initialize video writer
        self.out = cv2.VideoWriter(self.fn, cv2.VideoWriter_fourcc(*'H264'), 30, (640, 480))
        
        # Add timestamp overlay to first frame
        if self.frame is not None:
            cv2.putText(self.frame, self.ts1 + "  " + str(self.count), (3, self.frame.shape[0] - 470),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.25, (255, 255, 255), 1)
            self.out.write(self.frame)
        
        # Write timestamp to text file
        with open(self.txtfile, 'a') as txt:
            txt.write(str(self.count) + "  " + self.ts + '\n')
        
        self.stopped = False
    
    def start(self):
        """Start the video capture thread."""
        Thread(target=self.get, args=(), daemon=True).start()
        return self
    
    def get(self):
        """Continuously capture frames and write them to file."""
        while not self.stopped:
            self.grabbed, self.frame = self.stream.read()
            if not self.grabbed:
                self.stop()
            else:
                self.ts = datetime.now().strftime('%Y_%m_%d_%H:%M:%S.%f')
                self.ts1 = datetime.now().strftime('%m%d%Y %H:%M')
                self.count += 1

                # Add timestamp overlay to frame
                if self.frame is not None:
                    cv2.putText(self.frame, self.ts1, (3, self.frame.shape[0] - 470),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.25, (255, 255, 255), 1)
                    self.out.write(self.frame)
                
                # Append timestamp to text file
                with open(self.txtfile, 'a') as txt:
                    txt.write(str(self.count) + "  " + self.ts + '\n')
                
                # Switch video file every 3 hours
                if self.switchtime < datetime.now():
                    self.switchtime = datetime.now() + timedelta(hours=3)
                    self.dtime = datetime.now().strftime('%m-%d-%Y_%H-%M-%S')
                    self.fn = '/home/pi/Desktop/UserName/Box_1/Top/Mouse1_T_' + self.dtime + '.mkv'
                    self.txtfile = '/home/pi/Desktop/UserName/Box_1/Top_Data/Mouse1_T_' + self.dtime + '.txt'
                    self.out = cv2.VideoWriter(self.fn, cv2.VideoWriter_fourcc(*'H264'), 30, (640, 480))
    
    def stop(self):
        """Stop the video capture."""
        self.stopped = True
        self.stream.release()
        self.out.release()

class VideoStreamSocket:
    """
    Class to stream video frames over a network using ZeroMQ.
    """
    def __init__(self):
        self.fs = footage_socket  # Network socket for streaming
        self.stopped = False
    
    def start(self):
        """Start the streaming thread."""
        Thread(target=self.get, args=(), daemon=True).start()
        return self
    
    def get(self):
        """Continuously capture and send frames over the network."""
        while not self.stopped:
            frame = video_stream.frame
            if frame is not None:
                encoded, buffer = cv2.imencode('.jpg', frame)
                jpg_as_text = base64.b64encode(buffer)
                self.fs.send(jpg_as_text)
            time.sleep(0.25)  # Delay to control frame rate
    
    def stop(self):
        """Stop the video streaming."""
        self.stopped = True

# Initialize video streaming
ts = datetime.now().strftime('%Y_%m_%d_%H:%M:%S.%f')
video_stream = SaveVideoStream(0, ts, 0).start()

# Setup ZeroMQ for video streaming
sock = 5555
context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.bind('tcp://*:' + str(sock))

# Start video streaming over the network
video_socket = VideoStreamSocket().start()
