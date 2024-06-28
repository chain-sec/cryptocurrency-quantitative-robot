from src.alg.base_function import compute_can_make_how_money
from src.data_service.model import instrument_price_point


def fuck(point_list: list[InstrumentPricePoint], index: int) -> bool:
    max_make_money = 0
    buy_price = point_list[index].open
    for step in range(1, 60 * 24):
        current_index = index + step
        if current_index >= len(point_list):
            continue
        can_make_money = compute_can_make_how_money(buy_price, 1, point_list[current_index].open)
        if can_make_money > max_make_money:
            max_make_money = can_make_money
    print(max_make_money)
    return max_make_money > 0


if __name__ == '__main__':
    inst_id = 'TNSR-USDT'
    l = InstrumentPricePoint.list_instrument_price_points(inst_id)
    can_make_money_count = 0
    for index in range(len(l)):
        if fuck(l, index):
            can_make_money_count += 1
    print(can_make_money_count / len(l) * 100)
