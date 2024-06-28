
from okx.PublicData import PublicAPI

if __name__ == '__main__':

    api = PublicAPI()
    method = 'GET'
    url = '/api/v5/market/history-index-candles'
    params = {
        'instId': 'BTC-USD'
    }
    r = api.request(method, url, params=params)
    print(r.text)

