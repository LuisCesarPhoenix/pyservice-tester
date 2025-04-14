from pydantic import BaseModel, Field
from typing import Optional

class DataSchema(BaseModel):
    cpf: str = Field(..., regex=r"^\d{11}$")  # CPF deve ter 11 dígitos
    nome: Optional[str]
    telefone: Optional[str]
    email: Optional[str]
    endereco: Optional[str]

    class Config:
        anystr_strip_whitespace = True  # Remove espaços extras
        validate_assignment = True  # Valida ao atribuir valores
