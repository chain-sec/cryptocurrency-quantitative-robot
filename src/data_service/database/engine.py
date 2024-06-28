from sqlalchemy import create_engine, insert
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session

from src.data_service.model.base import Base

engine = create_engine("mysql+pymysql://root:123456@localhost:3306/cryptocurrency-quantitative", echo=True)
# 创建表结构
Base.metadata.create_all(engine)


def get_engine():
    return engine


def save(o):
    """

    :param o:
    :return:
    """
    return save_all([o])


def save_all(o_list):
    """

    :param o_list:
    :return:
    """
    with Session(engine) as session:
        session.bulk_save_objects(o_list)
        session.commit()


def to_dict(o):
    old_dict = vars(o)
    new_dict = {}
    for k, v in old_dict.items():
        if k == '_sa_instance_state':
            continue
        # 空字段就直接忽略了
        if v is None:
            continue
        new_dict[str(k)] = v
    return new_dict


def upsert(o):
    return upsert_all([o])


def upsert_all(o_list):
    with Session(engine) as session:
        for item in o_list:
            insert_stmt = insert(type(item)).values(to_dict(item))
            on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(to_dict(item))
            session.execute(on_duplicate_key_stmt)
            session.commit()


def find_all(table_class):
    object_list = []
    with Session(engine) as session:
        for row in session.query(table_class):
            object_list.append(row)
    return object_list
