from okx.PublicData import PublicAPI
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.data_service.database.engine import engine


def run():
    list_need_monitor_inst()


def sync_inst_history_price():
    pass





def list_need_monitor_inst():
    with Session(engine) as session:
        stmt = select(InstrumentMonitorStatus).where(InstrumentMonitorStatus.monitor_status == 1)
        return session.scalars(stmt)




if __name__ == '__main__':
    list_all_inst()
