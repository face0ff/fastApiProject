import asyncio

import uvicorn
import socketio
import aio_pika

mgr = socketio.AsyncAioPikaManager('amqp://rabbit-user:1542@localhost:5672/rabbit-wallet-vhost')
sio = socketio.AsyncServer(
    async_mode='asgi',
    client_manager=mgr,
    logger=True,
    engineio_logger=True)
app = socketio.ASGIApp(
    socketio_server=sio,
    socketio_path='sockets')


async def send_token_to_rabbit(token):
    connection = await aio_pika.connect_robust("amqp://rabbit-user:1542@localhost:5672/rabbit-wallet-vhost")
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=token.encode()),
            routing_key="token"
        )


@sio.event
async def connect(sid, environ, auth):
    print("connect ", sid)
    print("environ ", environ)
    print("auth ", auth)
    await send_token_to_rabbit(auth['token'])


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


# app.router.add_static('/static', 'static')
# app.router.add_get('/', index)

if __name__ == '__main__':
    uvicorn.run("sockets:app", port=8001, host='127.0.0.1', reload=True)
