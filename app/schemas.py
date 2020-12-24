from typing import List

from pydantic import BaseModel


class Kurs(BaseModel):
    bank: str
    jual: float
    beli: float


class Kebasa(BaseModel):

    nama: str
    jenis: str
    harga: str