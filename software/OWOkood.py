import json, time, queue
import multiprocessing as mp    
import websocket as wsc
name = "jackbot"

class Referee_cmd_client:
    def __init__(self):
        self.ip = "192.168.3.35"
        self.port = "8222"
        
        self.queue = mp.Queue()
      

    def open(self):
        self.ws = wsc.WebSocket()
        self.connect()
        self.process = mp.Process(target=self.listen, args=())
        self.process.start()
       
    def close(self):
        self.process.join()
        self.ws.close()
      
    def connect(self):
        for i in range(10): # Make 10 attempts at connecting
            try:
                self.ws.connect("ws://" + self.ip + ":" + self.port)
            except ConnectionRefusedError:
                print("Error")
                time.sleep(2)
                continue
            else:
                print("No error")
                return True
                break
        return False

    def get_cmd(self):
        try:
            return self.queue.get_nowait()
        except queue.Empty:
            return None

    def listen(self):
        print("Listening started")
        while True:
            try:
                msg = self.ws.recv()
            except wsc.WebSocketConnectionClosedException:
                print("Lost connection to referee server")
                if self.connect():
                    print("Reconnected to referee server")
                    continue
                else:
                    print("Could not reconnect to referee server")
                    break
            try:
                self.queue.put(json.loads(msg))
            except json.JSONDecodeError:
                print("Referee sent invalid message")
                continue

if __name__ == "__main__":
    
    client = Referee_cmd_client()
    client.open()
    last_msg = ""
    try:
        while(True):
            msg = client.get_cmd()
            if msg != last_msg and msg != None:
                
                print("Message:",msg["signal"])
                last_msg = msg
                if name in msg["targets"]:
                    if msg["signal"]=="start":
                        if msg["targets"][1] == name:
                            print("GOGOGOGOGOGOGO",msg["baskets"][1])
                        elif msg["targets"][0] == name:
                            print("GOGOGOGOGOGOGO",msg["baskets"][0])
                    else:
                        print("STOOOOOP!")

            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
        client.close()