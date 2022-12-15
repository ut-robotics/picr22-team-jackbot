import json, time, queue
import multiprocessing as mp    
import websocket as wsc

ws = wsc.WebSocket()
ip ="192.168.89.133"
port = "8222"

def listen():
    print("Listening started")
    while True:
        try:
            msg = ws.recv()
        except wsc.WebSocketConnectionClosedException:
            print("Lost connection to referee server")
            if connect():
                print("Reconnected to referee server")
                continue
            else:
                print("Could not reconnect to referee server")
                break
        try:
            queue.put(json.loads(msg))
        except json.JSONDecodeError:
            print("Referee sent invalid message")
            continue

def connect():
    for i in range(10): # Make 10 attempts at connecting
        try:
            ws.connect("ws://" + ip + ":" + port)
        except ConnectionRefusedError:
            print("Error")
            time.sleep(2)
            continue
        else:
            print("No error")
            return True
            break
    return False
def open():
    ws = wsc.WebSocket()
    connect()
    process = mp.Process(target=listen, args=())
    process.start()

def get_cmd():
        try:
            return queue.get_nowait()
        except queue.Empty:
            return None

open()
try:
    while(True):
        print("getting")
        msg = get_cmd()
        print(msg)
        time.sleep(1)
except KeyboardInterrupt:
    
    close()
