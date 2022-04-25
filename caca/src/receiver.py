import time
import numpy as np 
import zmq
import cv2 as cv
from mycodec import decode

def listen_for_frames(port: int):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.setsockopt(zmq.RCVTIMEO, 2000)
    socket.bind(f"tcp://*:{port}")
    frame_times = []    
    while True:
        try: 
            message = socket.recv()
        except:
            print("Timeout, closing renderer")
            break
        frame_times.append(time.time())
        frame = decode(message)
        cv.imshow("Streaming game", frame)
        cv.waitKey(1)
        socket.send(b"ready")
    frame_time = np.array(frame_times)
    delta_time = frame_time[1:] - frame_time[:-1]
    print(f"Tiempo promedio {np.mean(delta_time)*1000:0.4f} [ms] y desviación estándar {np.std(delta_time)*1000:0.4f} [ms]")
    socket.close()
    context.term()

if __name__ == "__main__":
    listen_for_frames(5555)
