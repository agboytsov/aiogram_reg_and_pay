from db.db_models import *
import datetime

async def check_user(from_user):
    s = session.query(User).filter(User.tg_id == from_user.id).first()
    if s is None:
        await register_user(from_user)
        return False, 0
    else:
        return True, s.id


async def register_user(from_user):
    session.add(User(
        tg_id=from_user.id,
        name=from_user.first_name,
        surname=from_user.last_name,
        nick=from_user.username,
        reg_date=datetime.datetime.now()
    ))
    session.commit()


async def check_admin(from_user_id):
    q = session.query(User).filter(User.tg_id == from_user_id).first()
    if q.is_admin:
        print(True, from_user_id, 'is admin')
        return True
    return False


async def check_not_free(qid):
    q = session.query(QuestsInfo).filter(QuestsInfo.qid == qid).first()
    if q.price is None:
        return False
    return True


async def check_payment(tg_id, qid):
    uid = session.query(User).filter(User.tg_id == tg_id).first().id
    payed = session.query(Orders).filter(Orders.user_id == uid, Orders.quest_id == qid).first()
    if payed is None:
        return False
    return True


