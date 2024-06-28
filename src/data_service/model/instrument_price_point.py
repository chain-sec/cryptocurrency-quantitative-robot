import time

from sqlalchemy import String
from sqlalchemy.orm import Mapped, Session
from sqlalchemy.orm import mapped_column

from src.data_service.database.engine import engine
from src.data_service.model.base import Base


class InstrumentPricePoint(Base):
    __tablename__ = "instrument_price_points"

    # 此货币在欧易上的id
    inst_id: Mapped[str] = mapped_column(String(30), primary_key=True)

    # 开始时间，Unix时间戳的毫秒数格式，如 1597026383085
    timestamp: Mapped[int] = mapped_column(primary_key=True)

    # 最高价格
    high: Mapped[float] = mapped_column()

    # 最低价格
    low: Mapped[float] = mapped_column()

    # 开盘价格
    open: Mapped[float] = mapped_column()

    # 收盘价格
    close: Mapped[float] = mapped_column()

    # K线状态
    # 0 代表 K 线未完结，1 代表 K 线已完结。
    confirm: Mapped[int] = mapped_column()

    def timestamp_to_datetime_str(self) -> str:
        t = time.localtime(self.timestamp / 1000)
        return time.strftime("%Y-%m-%d %H:%M:%S", t)

    def timestamp_to_time_str(self) -> str:
        t = time.localtime(self.timestamp / 1000)
        return time.strftime("%H:%M:%S", t)

    def timestamp_to_minute_str(self) -> str:
        t = time.localtime(self.timestamp / 1000)
        return time.strftime("%H:%M", t)


def list_instrument_price_points(inst_id: str) -> list[InstrumentPricePoint]:
    with Session(engine) as session:
        return session.query(InstrumentPricePoint).filter(InstrumentPricePoint.inst_id == inst_id).order_by(
            InstrumentPricePoint.timestamp.asc()).all()


if __name__ == '__main__':
    r = list_instrument_price_points('1INCH-USDT')
    print(r)
