def compute_buy_fee(buy_count: float = 1, buy_fee_ratio: float = 0.1) -> float:
    """
    计算买入费率，返回的单位是要买入的币（与okx订单核对无误）
    :param buy_count: 有多少个币，默认是一个币，这个单位是由具体的币决定的
    :param buy_fee_ratio: 费率，默认是 0.1%，cc的账号费率是这个样子的
    :return: 买入的手续费是多少个币，根据手续费费率计算
    """
    # 买入的手续费是收取的买入的具体币种
    return buy_count * buy_fee_ratio / 100


def compute_buy_real_receive(buy_count: float = 1, buy_fee_ratio: float = 0.1) -> float:
    """
    计算购买的时候实际收到的币的数量（与okx订单核对无误）
    :param buy_count: 买入的币的数量
    :param buy_fee_ratio: 买入的手续费的费率
    :return: 实际到账的币的数量，是要扣除完手续费才是真实到账的币的数量
    """
    return buy_count - compute_buy_fee(buy_count, buy_fee_ratio)


def compute_sell_fee(sell_price: float, sell_count: float = 1, sell_fee_ratio: float = 0.1) -> float:
    """
    计算卖出费率，单位是USDT （与okx订单核对无误）
    :param sell_price: 卖出的价格，以USDT价格为单位
    :param sell_count: 卖出了多少个币
    :param sell_fee_ratio: 卖出的费率，默认为 0.1%，cc的账号费率是这个样子的
    :return: 卖出手续费是多少个USDT
    """
    # 卖出的手续费收取的是 u
    return sell_price * sell_count * sell_fee_ratio / 100


def compute_sell_real_receive(sell_price: float, sell_count: float = 1, sell_fee_ratio: float = 0.1) -> float:
    """
    计算卖出的话实际能够收到的USDT是多少 （与okx订单核对无误）
    :param sell_price: 卖出的价格，单位是USDT
    :param sell_count: 实际卖出的币的数量
    :param sell_fee_ratio: 卖出的费率
    :return: 以这个价格卖出的话，实际到账的u有多少
    """
    return sell_price * sell_count - compute_sell_fee(sell_price, sell_count, sell_fee_ratio)


def compute_can_make_how_money(buy_price: float, buy_count: float, sell_price: float, buy_fee_ratio: float = 0.1,
                               sell_fee_ratio: float = 0.1) -> float:
    """
    给定买价和卖价以及币的数量，计算能够实际盈利多少，单位是USDT
    :param buy_price: 购买时的价格，单位是USDT
    :param buy_count: 购买了多少个币
    :param sell_price: 卖出时的价格，单位是USDT
    :param buy_fee_ratio: 购买时的手续费率
    :param sell_fee_ratio: 卖出时的手续费率
    :return: 以这个价格卖出的话，能够赚到的u有多少，如果是负数的话则表示要亏多少u
    """
    # 计算买入时实际入账的币有多少，因为等下卖出的时候实际上只有这些币可以卖
    real_buy_count = compute_buy_real_receive(buy_count, buy_fee_ratio)
    # 卖出这些币实际能够收到的钱
    sell_real_money = compute_sell_real_receive(sell_price, real_buy_count, sell_fee_ratio)
    # 卖出时实际能够收到的钱，减去买入时实际花费的钱，就是实际赚到的钱
    return sell_real_money - buy_price * buy_count


def compute_sell_at_least_price(buy_price: float, buy_count: float = 1, buy_fee_ratio: float = 0.1,
                                sell_fee_ratio: float = 0.1):
    """
    计算卖出价格至少是多少时才能盈利，否则的话就是亏本的
    :param buy_price: 购买时的价格，单位是u
    :param buy_count: 购买的币的数量
    :param buy_fee_ratio: 购买时的手续费率
    :param sell_fee_ratio: 卖出时的手续费率
    :return: 卖出价格至少要高出这么多u，要不然就没得赚
    """
    # 计算实际到账的币有多少
    buy_real_count = compute_buy_real_receive(buy_count, buy_fee_ratio)
    # 购买的时候实际花费的usdt有多少
    buy_cost_usdt = buy_price * buy_count
    # 假设卖出的价格为x，则x的取值要保证下面的这个不等式成立才能赚到钱
    # (x * buy_real_count * (100 - sell_fee_ratio) / 100 - buy_cost_usdt) > 0
    # 则 x > (buy_cost_usdt * 100 / (100 - sell_fee_ratio) / buy_real_count)
    return buy_cost_usdt * 100 / (100 - sell_fee_ratio) / buy_real_count


def is_zero(value: float) -> bool:
    """
    判断浮点数的值是否等于0
    :param value:
    :return:
    """
    return abs(value) < 0.0000000001


def compute_buy_fee_ratio(buy_count: float, buy_fee: float = 0.1) -> float:
    """
    计算购买币时的费率
    :param buy_count:
    :param buy_fee:
    :return:
    """
    return buy_fee / buy_count


if __name__ == '__main__':
    # r = compute_sell_price(100)
    # print(r)
    # print(compute_buy_fee(0.773343, 0.1))
    # print(compute_can_new_how_money(2.25, 1, 1.3885))
    # print(compute_sell_at_least_price(100, 1))
    # print(compute_can_make_how_money(100, 1, 100.2003004005006))
    # print(is_zero(compute_can_make_how_money(100, 1, 100.2003004005006)))
    # print(compute_buy_fee_ratio(10, 0.14160))
    print(compute_sell_at_least_price(0.14160, 10, ))
