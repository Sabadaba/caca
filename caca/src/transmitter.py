import argparse
import zmq
from game import Game
from mycodec import code


def transmit_frames(IP: str, port: int):
    frames = Game()
    frame_height, frame_width = frames.get_resolution()
    print(f"Resolución del juego: {frame_width}x{frame_height}p")
    print(f"Cuadros por segundo: {frames.get_fps()}")

    print(f"Enviando cuadros a {IP}:{port}")
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{IP}:{port}")

    for frame in frames:
        #frame_denoise = denoise(frame)
        message = code(frame)
        socket.send_string(message)
        status = socket.recv()
        # print(status)

if name == "main":
    parser = argparse.ArgumentParser(description='Envía los frames al computador del cliente')
    parser.add_argument('--IP', dest='ip', type=str, help='La IP del cliente en formato 0:0:0:0')
    args = parser.parse_args()
    transmit_frames(args.ip, 5555)
