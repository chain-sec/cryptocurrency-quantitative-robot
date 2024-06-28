import time

from src.data_service.crawler.instrument_price_point_crawler import list_inst_history_price_point
from src.data_service.database.engine import find_all, upsert_all
from src.data_service.model.instrument import Instrument, find_by_inst_id, update_last_timestamp


def crawl_all_instrument_price_point():
    l = find_all(Instrument)
    for item in l:

        # 不是USDT单位的忽略，我也没有那些币啊
        if not item.is_usdt():
            continue

        inst_id = item.inst_id
        now = int(time.time() * 1000)

        # 看下上次的更新时间，不要更新太频繁
        inst = find_by_inst_id(inst_id)
        if inst is None:
            continue
        if not is_need_sync(inst, now):
            continue

        list_all_inst_history_price_point(inst_id, item.last_timestamp)

        update_last_timestamp(inst_id, now - 1000 * 60 * 3)


def list_all_inst_history_price_point(inst_id: str, last_timestamp: int = 0):
    last_timestamp = last_timestamp or 0
    after = int(time.time() * 1000) - 1000 * 60 * 60
    while True:
        price_point_list = list_inst_history_price_point(inst_id, after=after)
        if len(price_point_list) == 0:
            return

        upsert_all(price_point_list)

        for item in price_point_list:
            if item.timestamp < last_timestamp:
                return
            if item.timestamp < after:
                after = item.timestamp


def is_need_sync(inst, now):
    if inst.last_timestamp is None:
        return True
    return now - inst.last_timestamp > 1000 * 60 * 60 * 3


if __name__ == '__main__':
    crawl_all_instrument_price_point()
    # list_all_inst_history_price_point('TNSR-USDT')
