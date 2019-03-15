#author py chen
import datetime
import os

FALL_IN_LOVE=(2019,2,24)
# print(type(FALL_IN_LOVE))


MAIL_SERVER = os.environ.get("MAIL_SERVER")
USER_MAIL = os.environ.get("USER_MAIL")
PASS_MAIL = os.environ.get("PASS_MAIL")
SEND_MAIL = os.environ.get("SEND_MAIL")
TO_MAIL = os.environ.get("TO_MAIL")

def get_loving_days():

    today=datetime.datetime.today()
    anniversary_day=datetime.datetime(*FALL_IN_LOVE)

    return (today-anniversary_day).days

# print(datetime.datetime(*FALL_IN_LOVE))
#
# print(get_loving_days())
