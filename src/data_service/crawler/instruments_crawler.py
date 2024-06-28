from okx.TradingData import TradingDataAPI

from src.config.config import config
from src.data_service.database.engine import upsert_all
from src.data_service.model.instrument import Instrument


def list_all_inst(inst_type: str = 'SPOT'):
    """
    获取平台上所有的币，以框架内部的数据结构表示
    :param inst_type:
    :return:
    """
    response = crawl_all_inst(inst_type)
    return convert(response)


def crawl_all_inst(inst_type: str = 'SPOT'):
    """
    获取欧易平台上所有的货币
    :param inst_type:
    :return:
    """
    trading_data_api = TradingDataAPI(api_key=config.okx.api_key, api_secret_key=config.okx.api_secret_key,
                                      passphrase=config.okx.passphrase, flag='0')
    request_path = '/api/v5/account/instruments'
    params = {
        'instType': inst_type
    }
    return trading_data_api._request_with_params(method='GET', request_path=request_path, params=params)


def convert(response) -> list[Instrument]:
    """
    把原始的字典数据结构转换为框架内部使用的格式
    :param response:
    :return:
    """
    instrument_list = []
    for item in response['data']:
        instrument = Instrument()
        instrument.inst_id = item['instId']
        instrument.base_ccy = item['baseCcy']
        instrument.lever = item['lever']
        instrument.monitor_status = None
        instrument.last_timestamp = None
        instrument_list.append(instrument)
    return instrument_list


def init_instrument_table():
    """
    初始化 instruments 表
    :return:
    """
    instrument_list = list_all_inst('SPOT')
    upsert_all(instrument_list)


if __name__ == '__main__':
    init_instrument_table()
