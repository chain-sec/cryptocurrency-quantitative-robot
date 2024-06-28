from okx.Trade import TradeAPI

from src.config.config import config

trade_api = TradeAPI(api_key=config.okx.api_key, api_secret_key=config.okx.api_secret_key,
                     passphrase=config.okx.passphrase, flag='0')

if __name__ == '__main__':
    # r = trade_api.place_order(instType='SPOT', instId='TNSR-USDT')
    # r = trade_api.cancel_order(instType='SPOT', instId='TNSR-USDT')
    # r = trade_api.get_order_list(instType='SPOT', instId='TNSR-USDT')
    # print(r)

    # 下订单卖
    # r = trade_api.place_order(instId='TNSR-USDT', tdMode='cash', side='sell', ordType='limit', sz=1, px=6.6)
    # print(r)

    # 下订单买
    r = trade_api.place_order(instId='DOGE-USDT', tdMode='cash', side='buy', ordType='limit', sz=10, px=0.14160)
    print(r)
