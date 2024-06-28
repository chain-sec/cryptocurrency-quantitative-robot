import base64
import hmac
import json
import time
from threading import Thread

import websocket

from src.config.config import config


def heart_beat_thread(wsapp):
    print('begin heart beat thread')
    while True:
        time.sleep(10)
        wsapp.send('ping')


def sign(message, secret_key):
    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    return str(base64.b64encode(d), "utf-8")


def on_message(wsapp, message):
    print(message)

    if message == 'pong':
        return
        # {"event":"login","msg":"","code":"0","connId":"9c46446e"}
    message = json.loads(message)
    if message['event'] == 'login':
        on_login_success(wsapp)


def on_open(wsapp):
    login(wsapp)


def login(wsapp):
    timestamp = int(time.time())
    message = {
        'op': 'login',
        'args': [
            {
                'apiKey': config.okx.api_key,
                'passphrase': config.okx.passphrase,
                'timestamp': timestamp,
                'sign': sign(str(timestamp) + 'GET' + '/users/self/verify', config.okx.api_secret_key),
            }
        ]
    }
    wsapp.send(json.dumps(message))


def on_login_success(wsapp):
    # 获取订单信息，首次订阅不推送，只有当下单、撤单等事件触发时，推送数据
    message = {
        'op': 'subscribe',
        'args': [
            {
                'channel': 'orders',
                'instType': 'ANY',
                'instId': 'BTC-USDT',
            }
        ]
    }
    wsapp.send(json.dumps(message))

    Thread(target=heart_beat_thread, args=(wsapp,)).start()


websocket.enableTrace(True)

wsapp = websocket.WebSocketApp("wss://ws.okx.com:8443/ws/v5/private", on_open=on_open, on_message=on_message)
wsapp.run_forever()
