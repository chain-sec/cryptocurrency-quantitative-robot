from src.data_service.model.instrument_price_point import InstrumentPricePoint


# 均值回归算法


class MaInstrumentPricePoint(InstrumentPricePoint):
    # 均值价格
    ma_price: float


#

# 布林带、回归通道、肯特纳通道和包络线等技术指标

def sma(price_point_list: list[InstrumentPricePoint], n: int) -> list[MaInstrumentPricePoint]:
    """
    计算简单移动平均线(SMA)
    :param price_point_list:
    :param n:
    :return:
    """
    # 如果点不够计算的话，则直接结束即可
    if len(price_point_list) < n:
        return []

        # 先把前n个点加起来
    sum = 0
    for i in range(n):
        sum += price_point_list[i].close

    move_list = []
    index = n + 1
    while index < len(price_point_list):
        # 计算今天的ma
        now_point = MaInstrumentPricePoint()
        now_point.ma_price = sum / n
        move_list.append(now_point)

        # 然后把累计和往后叠加
        sum -= price_point_list[index - n - 1].close
        sum += price_point_list[index].close
        index += 1

# ma5，ma10,ma20，ma30，ma60，ma120，ma250


if __name__ == '__main__':
    pass
