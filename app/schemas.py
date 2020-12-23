from typing import List

from pydantic import BaseModel


class Kurs(BaseModel):
    bank: str
    jual: float
    beli: float