from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.sql import func

from backend.db.connection import Base

# Modelo SQLAlchemy para o banco de dados
class Emitente(Base):
    __tablename__ = "emitente"

    id = Column(Integer, primary_key=True, index=True)  # ID para a chave primária
    razao_social = Column(String(255), nullable=False)  # Razão Social
    nome_fantasia = Column(String(255))  # Nome Fantasia
    cnpj = Column(String(18), nullable=False)  # CNPJ
    inscricao_estadual = Column(String(20), nullable=False)  # Inscrição Estadual
    cnae_fiscal = Column(String(20))  # CNAE Fiscal
    inscricao_municipal = Column(String(20))  # Inscrição Municipal
    inscricao_estadual_subst_tributaria = Column(String(20))  # Inscrição Estadual Subst. Tributário
    codigo_de_regime_tributario = Column(String(10), nullable=False)  # Código de Regime Tributário
    endereco_logradouro = Column(String(255), nullable=False)  # Logradouro
    endereco_numero = Column(String(10), nullable=False)  # Número
    endereco_complemento = Column(String(255))  # Complemento
    endereco_bairro = Column(String(100), nullable=False)  # Bairro
    endereco_cep = Column(String(10))  # CEP
    endereco_pais = Column(String(50), nullable=False, default="Brasil")  # País (somente Brasil)
    endereco_uf = Column(String(2), nullable=False)  # UF
    endereco_municipio = Column(String(100), nullable=False)  # Município
    endereco_cod_municipio = Column(String(20))  # Código Município
    endereco_telefone = Column(String(15))  # Telefone
    status = Column(Boolean, default=True)  # Status
    licenca = Column(Integer, nullable=False)  # Licença
    mail = Column(Text, nullable=False)  # E-mail
    telefone = Column(Text, nullable=False)  # Telefone
    password = Column(Text)  # Senha
    data_criacao = Column(DateTime, default=func.now())  # Data de Criação
    cert = Column(String, nullable=False)
    senha_cert = Column(String, nullable=False)
    cod_seguranca = Column(String)

    #pedidos = relationship("Pedido", back_populates="cadastro", cascade="all, delete-orphan") 
    pedidos = relationship("Pedido", back_populates="emitente")

# Modelo Pydantic para resposta
class EmitenteBase(BaseModel):
    #id: int
    razao_social: str = Field(..., min_length=1, max_length=255, description="Razão Social do Emitente")
    nome_fantasia: Optional[str] = None
    cnpj: str
    inscricao_estadual: str
    cnae_fiscal: Optional[str] = None
    inscricao_municipal: Optional[str] = None
    inscricao_estadual_subst_tributaria: Optional[str] = None
    codigo_de_regime_tributario: Optional[str] = None
    endereco_logradouro: str
    endereco_numero: str
    endereco_complemento: Optional[str] = None
    endereco_bairro: str
    endereco_cep: Optional[str] = None
    endereco_pais: str = "Brasil"
    endereco_uf: str = "SP"
    endereco_municipio: Optional[str] = None
    endereco_cod_municipio: Optional[str] = None
    endereco_telefone: Optional[str] = None
    status: bool = True
    licenca: int
    mail: str
    telefone: str
    password: str
    data_criacao: Optional[datetime] = None
    cert: Optional[str] 
    senha_cert: Optional[str]
    cod_seguranca: Optional[str]
    

    class Config:
        from_attributes = True



class EmitenteUpdate(BaseModel):
    razao_social: Optional[str] = None
    nome_fantasia: Optional[str] = None
    cnpj: Optional[str] = None
    inscricao_estadual: Optional[str] = None
    cnae_fiscal: Optional[str] = None
    inscricao_municipal: Optional[str] = None
    inscricao_estadual_subst_tributaria: Optional[str] = None
    codigo_de_regime_tributario: Optional[str] = None
    endereco_logradouro: Optional[str] = None
    endereco_numero: Optional[str] = None
    endereco_complemento: Optional[str] = None
    endereco_bairro: Optional[str] = None
    endereco_cep: Optional[str] = None
    endereco_pais: Optional[str] = None
    endereco_uf: Optional[str] = None
    endereco_municipio: Optional[str] = None
    endereco_cod_municipio: Optional[str] = None
    endereco_telefone: Optional[str] = None
    status: Optional[bool] = None
    licenca: Optional[bool] = None
    mail: Optional[str] = None
    telefone: Optional[str] = None
    password: Optional[str] = None
    cert: Optional[str] = None
    senha_cert: Optional[str] = None
    cod_seguranca: Optional[str] = None

    class Config:
        from_attributes = True
