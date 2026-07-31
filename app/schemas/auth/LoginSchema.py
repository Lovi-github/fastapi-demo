"""登录接口的请求体模型。"""

from typing import List, Optional

from pydantic import BaseModel


    
class LoginSchema(BaseModel):
    """声明登录接口当前接受的两个必填字符串字段。

    本模型会保证字段存在并进行基础类型解析；当前没有邮箱格式、密码长度
    或真实账号校验规则，学习时不要把它误认为生产级登录 DTO。
    """
    email: str
    password: str
