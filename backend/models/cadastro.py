from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.sql import func

from backend.db.connection import Base

# Modelo SQLAlchemy para o banco de dados
class Cadastro(Base):
    __tablename__ = "cadastro"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String(255), nullable=False)  # Limite de tamanho definido
    status = Column(Boolean, default=True)  # Agora é um booleano (True = ativo, False = inativo)
    nome = Column(String, nullable=False)  
    cnpj = Column(String, nullable=False)  
    ie = Column(String, nullable=False)  
    data_criacao = Column(DateTime, default=func.now())  
    licenca = Column(Integer, nullable=False)
    endereco = Column(String, nullable=False)
    mail = Column(String, nullable=False)
    telefone = Column(String, nullable=False)  
    password = Column(String, nullable=False)  
    cert = Column(String, nullable=False)
    key = Column(String, nullable=False)

    #pedidos = relationship("Pedido", back_populates="cadastro", cascade="all, delete-orphan") 
    pedidos = relationship("Pedido", back_populates="cadastro")

# Modelo Pydantic para resposta
class CadastroBase(BaseModel):
    descricao: str = Field(..., min_length=1, max_length=255, description="Descrição do pedido")
    status: bool  # Agora é um booleano
    nome: str
    cnpj: str  
    ie: str  
    data_criacao: Optional[datetime] = None  
    licenca: int
    endereco: str
    mail: str
    telefone: str 
    password: str 
    cert: Optional[str]
    key: Optional[str]

    class Config:
        from_attributes = True


class CadastroUpdate(BaseModel):
    descricao: Optional[str] = None
    status: Optional[bool] = None
    nome: Optional[str] = None
    cnpj: Optional[str] = None
    ie: Optional[str] = None
    licenca: Optional[int] = None
    endereco: Optional[str] = None
    mail: Optional[str] = None
    telefone: Optional[str] = None
    password: Optional[str] = None

    class Config:
        from_attributes = True