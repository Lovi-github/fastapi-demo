"""FastAPI Depends 可使用的前置校验示例。

当前任何 Router 都没有引用这些函数；它们不会影响登录接口，阅读时把它们当作
“如何把通用校验从 Controller 抽出”的参考。
"""

from typing import Annotated

from fastapi import Header, HTTPException


async def get_token_header(x_token: Annotated[str, Header()]):
    """校验请求头中的演示令牌。"""
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    """校验查询参数中的演示令牌。"""
    if token != "vahid":
        raise HTTPException(status_code=400, detail="No Vahid token provided")
