from rest_framework import authentication
import jwt
from rest_framework.exceptions import AuthenticationFailed

from s2i.settings import SECRET_KEY

class MyJwtAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if request.method == 'POST':
            # 从请求头中获取token
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                raise AuthenticationFailed('未找到授权信息')
            
            try:
                # 处理Bearer格式的token
                auth_parts = auth_header.split()
                if len(auth_parts) != 2 or auth_parts[0].lower() != 'bearer':
                    raise AuthenticationFailed('无效的授权格式')
                
                token = auth_parts[1]
                payload = jwt.decode(token, algorithms=['HS256'], key=SECRET_KEY)
                return (payload, token)
            except jwt.DecodeError:
                raise AuthenticationFailed('无效的令牌')
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('令牌已过期')
            except Exception:
                raise AuthenticationFailed('认证失败')