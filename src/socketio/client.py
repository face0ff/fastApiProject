import asyncio
import socketio

sio = socketio.AsyncClient()


@sio.event
async def connect():
    print('connection established')


@sio.event
async def my_message(data):
    print('message received with ', data)
    await sio.emit('my response', {'response': data})


@sio.event
async def disconnect():
    print('disconnected from server')


async def main():
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzdXNlckBleGFtcGxlLmNvbSIsImV4cCI6MTY5NDI1NTM5N30.u6veqs_FkxyHXneSLfChHZ8DbvLpJr01fBpu7u25rNM'  # Замените на реальный токен
    await sio.connect('http://localhost:8001', socketio_path='sockets', auth={'token': token})
    await asyncio.sleep(600)
    await sio.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
