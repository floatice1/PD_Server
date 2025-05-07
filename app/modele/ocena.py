from pydantic import BaseModel, Field
import datetime

class OcenaBazowa(BaseModel):
    studentId: str
    grupaId: str
    wystawionePrzez: str
    wartoscOceny: str

class OcenaTworzenie(OcenaBazowa):
    pass

class Ocena(OcenaBazowa):
    ocenaId: str
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)