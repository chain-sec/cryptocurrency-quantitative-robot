from src.data_service.model.instrument_price_point import InstrumentPricePoint


class JiHuiInstrumentPricePoint(InstrumentPricePoint):
    pass


def find_ji_hui(price_point_list: list[InstrumentPricePoint]) -> list[JiHuiInstrumentPricePoint]:
    """
    看一下每个价格点的机会
    :param price_point_list:
    :return:
    """
    for index, price_point in price_point_list:
        pass


def find_next_can_make_money_point(price_point_list: list[InstrumentPricePoint], index: int) -> JiHuiInstrumentPricePoint:
    pass


if __name__ == '__main__':
    pass
