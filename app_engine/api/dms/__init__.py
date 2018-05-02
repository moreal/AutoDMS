# -*-coding:utf8
# so simple and so dirty code

import requests
import json

from api.dms.exceptions import *

def login(id, pw):
    resp = requests.post("http://dms.istruly.sexy/auth", data={"id": id, "pw": pw})

    status_code = resp.status_code
    content = resp.text
    
    if not status_code is 200:
        raise BadLogin()
    
    data = json.loads(content)

    return data['refresh_token'], data['access_token']

def isRightPlace(class_num, seat_num):
    if 1 <= class_num <= 4:
        return 1 <= seat_num <= 20
    elif class_num == 5 or class_num == 6:
        return 1 <= seat_num <= 44
    elif class_num == 7:
        return 1 <= seat_num <= 49
    else:
        return False

def isRightTime(time):
    return time is 11 or time is 12

def getExtensionMaps(class_num, time):
    if isRightTime(time):
        content = requests.get(f"http://dms.istruly.sexy/extension/map/{time}?class_num={class_num}").text
        datas = json.loads(content) 
        maps = list(filter(lambda x: x != 0, datas))
        return maps
    else:
        raise BadTime()

def canAssign(class_num, seat_num, time):
    return seat_num in getExtensionMaps(class_num, time)

# 연장을 신청하는 메소드. class_num, seat_num 값을 필요로 합니다.
def applyExtension(id, pw, class_num, seat_num, time):
    try:
        refresh_token, access_token = login(id, pw)
    except BadLogin as e:
        raise e

    if not canAssign(class_num, seat_num, time):
        raise BadPlace()

    resp = requests.post(f"http://dms.istruly.sexy/extension/{time}", 
                         headers={"Authorization": "JWT "+access_token},
                         data={"seat_num": str(seat_num), "class_num": str(class_num)})

    status_code = resp.status_code

    return 200 <= status_code < 300

def getExtensionPlaceByName(name, time=12):
    for class_num in range(1,8):
        maps = getExtensionMaps(class_num, time)
        for seat_num, _name in enumerate(maps):
            if _name == name:
                return class_num, seat_num
    return -1, False