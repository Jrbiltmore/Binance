import jwt
import datetime
from typing import Dict

class Auth:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def encode_token(self, user_id: str) -> str:
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(payload, self.secret_key, algorithm='HS256')
        except Exception as e:
            return str(e)

    def decode_token(self, token: str) -> Dict[str, str]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return {'user_id': payload['sub']}
        except jwt.ExpiredSignatureError:
            return {'error': 'Token expired. Please log in again.'}
        except jwt.InvalidTokenError:
            return {'error': 'Invalid token. Please log in again.'}
