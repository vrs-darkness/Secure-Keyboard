from pydantic import BaseModel


class Input(BaseModel):
    Input: str


class Train(BaseModel):
    global_grad: dict
