import hashlib
import datetime
import time
from django.conf import settings

import jwt
from jwt import exceptions

from public.status_code import TOKEN_Invalid_Token, TOKEN_DecodeError, TOKEN_Expired_Signature_Error

# 行是必须的
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devops_zwy.settings")

SALT = settings.SECRET_KEY


def crate_token(uuid: str, username: str, nickname: str, role: int) -> str:
    # 构造header
    # headers = {
    #     'typ': 'jwt',
    #     'alg': 'HS256'
    # }
    # # 构造payload
    # payload = {
    #     'user_id': id,  # 自定义用户ID
    #     'username': username,  # 自定义用户名
    #     'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=m)  # 超时时间

    # }
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    # 构造payload
    payload = {
        'uuid': uuid,  # 自定义用户ID
        'username': username,  # 自定义用户名
        'nickname': nickname,  # 自定义用户名
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=settings.JWT_TIME_OUT)  # 超时时间
    }
    result = jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers)
    return result


def check_token(token: str) -> tuple[dict, bool]:
    try:
        # 从token中获取payload【不校验合法性】
        # unverified_payload = jwt.decode(token, None, False)
        # 从token中获取payload【校验合法性】
        result = jwt.decode(jwt=token, key=SALT, algorithms=["HS256"])
        return result, True
    except exceptions.ExpiredSignatureError:
        return TOKEN_Expired_Signature_Error, False
    except jwt.DecodeError:
        return TOKEN_DecodeError, False
    except jwt.InvalidTokenError:
        return TOKEN_Invalid_Token, False


def md5(password: str) -> str:
    """密码加密"""
    obj = hashlib.md5(SALT.encode("utf-8"))
    obj.update(password.encode("utf-8"))
    return obj.hexdigest()


if __name__ == '__main__':
    # start: float = time.time()
    # token: str = crate_token(1, "zhang", "zhang", 1)
    # print(token)
    # res, _ = check_token(
    #     "eyJhbGciOiJIUzI1NiIsInR5cCI6Imp3dCJ9.eyJ1dWlkIjoxLCJ1c2VybmFtZSI6InpoYW5nIiwibmlja25hbWUiOiJ6aGFuZyIsInJvbGUiOjEsImV4cCI6MTcwMzE2NjEyOH0.GxTLmgwGYXEr8vJ1ySOyFcBuCLczXUQrtX1yxtYS7cU")
    # print(res)
    # print(time.time() - start)
    pass
