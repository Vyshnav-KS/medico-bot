
import socketio
import time

# Create a Socket.IO client
sio = socketio.Client()
exit_flag = False

@sio.event
def connect():
    print('Connection established')
    sio.emit('start_stream', "from client")


@sio.event
def message(data):
    print('Received message:', data)


@sio.event
def ai_res(data):
    print(data, end="")

@sio.event
def stream_complete(data):
    print('Stream complete:', data['data'])
    sio.disconnect()  

@sio.event
def stream_error(data):
    print('Stream error:', data['data'])
    sio.disconnect()

@sio.event
def connect_error(data):
    print('Connection failed')
    sio.disconnect()

@sio.event
def disconnect():
    global exit_flag
    print('Disconnected from server')
    exit_flag = True

# Connect to the server
sio.connect('http://localhost:5001')


while not exit_flag:
    time.sleep(0.5)