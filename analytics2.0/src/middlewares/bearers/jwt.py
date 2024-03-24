from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.utils import tokenizator


class JWTErrors:
  INCORRECT_AUTH_SCHEME = "Неверная схема авторизации"
  INCORRECT_AUTH_TOKEN = "Неверный токен авторизации"


class JWTBearer(HTTPBearer):
  def __init__(self, auto_error: bool = True):
      super(JWTBearer, self).__init__(auto_error=auto_error)

  async def __call__(self, request: Request):
      CREDENTIAL_SCHEME = "Bearer"
      credentials: HTTPAuthorizationCredentials = await super(
          JWTBearer, self
      ).__call__(request=request)
      if credentials:
          if not credentials.scheme == CREDENTIAL_SCHEME:
              raise HTTPException(
                  status_code=status.HTTP_403_FORBIDDEN,
                  detail=JWTErrors.INCORRECT_AUTH_SCHEME,
              )
          payload = await self.verify_jwt(credentials.credentials)
          if payload is None:
              raise HTTPException(
                  status_code=status.HTTP_403_FORBIDDEN,
                  detail=JWTErrors.INCORRECT_AUTH_TOKEN,
              )   
          return payload
      else:
          raise HTTPException(
              status_code=status.HTTP_403_FORBIDDEN,
              detail=JWTErrors.INCORRECT_AUTH_SCHEME,
          )

  async def verify_jwt(self, jwt_token: str) -> bool:
    payload = None
    try:
        payload = tokenizator.decode(jwt_token)
    except Exception as ex:
        payload = None
    return payload
