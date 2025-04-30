from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.sql import func

from backend.db.connection import Base

# Modelo SQLAlchemy para o banco de dados
class Produto(Base):
    __tablename__ = "produto"

    id = Column(Integer, primary_key=True, index=True)  # ID para a chave primária
    codigo = Column(String(255), nullable=False)  # Razão Social
    descricao = Column(String(255))  # Nome Fantasia
    ncm = Column(String(10)) 
    cfop = Column(String(10)) 
    unidade_comercial = Column(String(10)) 
    unidade_tributavel = Column(String(10)) 
    ean = Column(String, default='SEM GTIN')
    ean_tributavel = Column(String, default='SEM GTIN')
    preco_unitario = Column(Float, nullable=False)
    origem_icms = Column(Integer, nullable=False)
    csosn = Column(String(3)) 
    pis_modalidade = Column(String(2)) 
    cofins_modalidade = Column(String(2)) 
    valor_tributos_aprox = Column(Float, nullable=False)
    ativo = Column(Boolean, default=True)
    emitente_id = Column(Integer, nullable=False)
    

     # Chave estrangeira
    emitente_id = Column(Integer, ForeignKey('emitente.id', ondelete='CASCADE'))
    #emitente = relationship("Emitente", back_populates="produto")


# Modelo Pydantic para resposta
class ProdutoBase(BaseModel):
     
    id: Optional[int] = None
    codigo: Optional[str] = None
    descricao: Optional[str] = None
    ncm: Optional[str] = None
    cfop: Optional[str] = None
    unidade_comercial: Optional[str] = None
    unidade_tributavel: Optional[str] = None
    ean: Optional[str] = None
    ean_tributavel: Optional[str] = None
    preco_unitario: Optional[float] = None
    origem_icms: Optional[int] = None
    csosn: Optional[str] = None
    pis_modalidade: Optional[str] = None
    cofins_modalidade: Optional[str] = None
    valor_tributos_aprox: Optional[float] = None
    ativo: Optional[bool] = True
    emitente_id: Optional[int] = None


    class Config:
        from_attributes = True



class ProdutoUpdate(BaseModel):
    codigo: Optional[str] = None
    descricao: Optional[str] = None
    ncm: Optional[str] = None
    cfop: Optional[str] = None
    unidade_comercial: Optional[str] = None
    unidade_tributavel: Optional[str] = None
    ean: Optional[str] = None
    ean_tributavel: Optional[str] = None
    preco_unitario: Optional[float] = None
    origem_icms: Optional[int] = None
    csosn: Optional[str] = None
    pis_modalidade: Optional[str] = None
    cofins_modalidade: Optional[str] = None
    valor_tributos_aprox: Optional[float] = None
    ativo: Optional[bool] = True
    emitente_id: Optional[int] = None
    
    class Config:
        from_attributes = True

