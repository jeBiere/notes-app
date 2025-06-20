from fastapi.security import APIKeyCookie
from fastapi import Security

access_token_cookie = APIKeyCookie(name="access_token", auto_error=False)

def get_token_from_cookie(token: str = Security(access_token_cookie)):
    return token
