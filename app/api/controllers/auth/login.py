"""登录接口 Controller。

这里保持轻量：接收已经校验的请求模型，委托 AuthService 生成令牌，
不在此处实现真实用户查询或密码校验。
"""

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.auth.LoginSchema import LoginSchema

from services.AuthService import AuthService

router = APIRouter(
    # main.py 会在这个前缀外再统一加上 /api/v1。
    tags=["Login Api"],
    prefix='/login'
    )


@router.post("/", response_model=dict)
async def loginUser(body : LoginSchema):
    """接收登录请求并返回访问令牌与刷新令牌。

    FastAPI 会先根据 LoginSchema 解析 body；当前项目的 userId 固定为演示值，
    因此该接口只能用于学习调用链，不能视为完整认证实现。
    """
    print(body)
    # 固定 ID 仅用于当前教学示例；真实认证应由用户查询和密码校验替代。
    userId = 1
    jwtData =await AuthService.generateTokens(userId)
    return jwtData
