from sqlalchemy import String
from sqlalchemy.orm import Mapped, Session
from sqlalchemy.orm import mapped_column

from src.data_service.database.engine import engine
from src.data_service.model.base import Base


class Instrument(Base):
    """
    用于存储当前所有的货币
    """
    __tablename__ = "instruments"

    # 货币在okx上的id
    inst_id: Mapped[str] = mapped_column(String(30), primary_key=True)

    # 交易货币币种，如 BTC-USDT 中的 BTC ，仅适用于币币/币币杠杆
    base_ccy: Mapped[str] = mapped_column(String(30))

    # 层级
    lever: Mapped[str] = mapped_column(String(30))

    # 这个货币当前的监控状态，1表示在监控，0表示未在监控
    monitor_status: Mapped[int] = mapped_column()

    # 表示下次查询的同时从哪个时间开始同步
    last_timestamp: Mapped[int] = mapped_column()

    def is_usdt(self) -> bool:
        """
        判断是否是 USDT货币单位
        :return:
        """
        if self.inst_id is None:
            return False
        return str(self.inst_id).endswith('-USDT')


def find_by_inst_id(inst_id):
    with Session(engine) as session:
        q = Instrument()
        q.inst_id = inst_id
        return session.query(Instrument).filter(Instrument.inst_id == inst_id).first()


def update_last_timestamp(inst_id, last_timestamp):
    with Session(engine) as session:
        session.query(Instrument).filter(Instrument.inst_id == inst_id).update(
            {Instrument.last_timestamp: last_timestamp})
        session.commit()


if __name__ == '__main__':
    r = find_by_inst_id('ACH-USDT')
    print(r)
