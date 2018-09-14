from typing import List, TypeVar

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

T = TypeVar('T')


class Repository:

    def __init__(self, session: Session):
        super().__init__()
        self._session = session

    def get(self, entity: T, entity_id: int) -> T:
        return self._session.query(entity).get(entity_id)

    def get_all(self, entity: T) -> List[T]:
        return self._session.query(entity).all()

    def save_or_update(self, entity: T) -> None:
        try:
            self._session.add(entity)
            self._session.commit()
        except:
            self._session.rollback()
            raise


def init_repository(usr, passwd, host, port, dbname) -> Repository:
    if not usr or not passwd or not host or not port or not dbname:
        raise RuntimeError('Error, cannot init db, at least one of parameters is empty')

    engine = create_engine('postgres://{usr}:{password}@{host}:{port}/{dbname}'.format(
        usr=usr, password=passwd, host=host, port=port, dbname=dbname))

    return Repository(sessionmaker(engine)())
