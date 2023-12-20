from fastapi import Response

def set_access_token(resp: Response, token: str) -> None:
    resp.set_cookie(
        key="access", 
        value=token,
        httponly=True,
        samesite="strict",
        max_age=1800,
    )