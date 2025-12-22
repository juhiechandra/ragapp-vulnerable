
from fastapi import HTTPException, status
from jwt import InvalidTokenError
import logging
import jwt


JWT_COOKIE_NAME = "Authorization"  # The name of the cookie that stores the JWT token


class JWT:
    _token: str
    data: dict

    def __init__(self, cookie: str):
        self._token = self._get_jwt_token(cookie)
        self.data = self._parse_jwt(self._token)

    @staticmethod
    def _get_jwt_token(cookie: str) -> str:
        token = cookie.get(JWT_COOKIE_NAME)
        if not cookie:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )
        # Remove Bearer prefix
        jwt_token = token.split(" ")[1]
        if not jwt_token or jwt_token == "":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid JWT token",
            )
        logging.info(f" user JWT token: {jwt_token}")
        return jwt_token
        

    @staticmethod
    def _parse_jwt(jwt_token: str) -> dict:
        try:
            # Decode without verifying the signature
            token_unmasked = jwt_token
            data = jwt.decode(token_unmasked, options={"verify_signature": False})
            return data
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid JWT token",
            )
