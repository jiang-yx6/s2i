import jwt
from s2i import settings

def create_token(user):
    jwt_sk = settings.SECRET_KEY
    headers = {
        'type': 'jwt',
        'alg': 'HS256',
    }
    payload = {
        'user_id': user.id,
        'username': user.username,
    }
    user_token = jwt.encode(headers=headers, payload=payload, algorithm='HS256', key=jwt_sk)
    return user_token