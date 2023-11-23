from sqlalchemy import create_engine, Integer, String, \
    Column, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, relationship, Session, sessionmaker

engine = create_engine("postgresql+psycopg2://test_db:test_db_pass@localhost/test_db")
engine.connect()


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    tg_id = Column(Integer())
    nick = Column(String(200))
    name = Column(String(200))
    surname = Column(String(200))
    email = Column(String())
    orders = relationship('Orders')
    is_admin = Column(Boolean())
    reg_date = Column(DateTime)


class QuestsInfo(Base):
    __tablename__ = 'quests_info'

    id = Column(Integer(), primary_key=True)
    qid = Column(Integer())
    name = Column(String())
    price = Column(Integer())
    desc = Column(String())
    loc = Column(String())
    start = Column(String())
    time = Column(Integer())


class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer(), primary_key=True)
    datetime = Column(DateTime())
    sum = Column(Integer())
    user_id = Column(ForeignKey("users.id"))
    quest_id = Column(ForeignKey('quests_info.id'))
    discount = Column(Integer())


#Base.metadata.drop_all(engine)

Base.metadata.create_all(engine)

# session = sessionmaker(bind=engine)
session = Session(bind=engine)

