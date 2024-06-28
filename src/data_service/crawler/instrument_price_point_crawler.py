from okx.PublicData import PublicAPI

from src.data_service.database.engine import upsert_all
from src.data_service.model.instrument_price_point import InstrumentPricePoint


def list_inst_history_price_point(inst_id: str, before: int = None, after: int = None):
    r = crawl_inst_history_price_point(inst_id, before, after)
    return convert(inst_id, r)


def crawl_inst_history_price_point(inst_id: str, before: int = None, after: int = None):
    for i in range(1, 10):
        try:
            api = PublicAPI()
            method = 'GET'
            url = '/api/v5/market/history-index-candles'

            params = {
                'instId': inst_id
            }
            if before:
                params['before'] = before
            if after:
                params['after'] = after

            return api.request(method, url, params=params).json()
        except Exception as e:
            print(e)


def convert(inst_id, response):
    price_point_list = []
    for item in response['data']:
        point = InstrumentPricePoint()
        point.id = None
        point.inst_id = inst_id
        point.timestamp = int(item[0])
        point.open = float(item[1])
        point.high = float(item[2])
        point.low = float(item[3])
        point.close = float(item[4])
        point.confirm = int(item[5])
        price_point_list.append(point)
    return price_point_list


if __name__ == '__main__':
    pass
