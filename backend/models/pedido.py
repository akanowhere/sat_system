from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from backend.models.cadastro import Cadastro
from backend.models.emitente import Emitente
import streamlit as st
import pytz


from backend.db.connection import Base

# Modelo SQLAlchemy para o banco de dados
class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    status = Column(String, default="pendente")
    valor_total = Column(Float, nullable=False)
    #data_criacao = Column(DateTime, default=datetime.utcnow)
    data_criacao = Column(DateTime, default=lambda: datetime.now(pytz.timezone('America/Sao_Paulo')))
    quantidade = Column(Float, nullable=False)
    chave_acesso = Column(String, nullable=True)
    protocolo = Column(String, nullable=True)
    status_sefaz = Column(String, nullable=True)
    motivo = Column(String, nullable=True)
    data_recebimento = Column(String, nullable=True)


    # Chave estrangeira
    emitente_id = Column(Integer, ForeignKey('emitente.id', ondelete='CASCADE'))

    #pagamentos = relationship("Pagamento", back_populates="pedido", cascade="all, delete-orphan")
    emitente = relationship("Emitente", back_populates="pedidos")


# Modelo Pydantic para resposta
# Modelo Pydantic para resposta
class PedidoBase(BaseModel):
    #descricao: str
    descricao: str = Field(..., min_length=1, max_length=255, description="Descrição do pedido")
    status: str = "pendente"
    valor_total: float
    data_criacao: Optional[datetime] = None  # Opcional, será automaticamente atribuído ao criar
    emitente_id: Optional[int] = None
    quantidade: Optional[float] = None
    chave_acesso: Optional[str] = None
    protocolo: Optional[str] = None
    status_sefaz: Optional[str] = None
    motivo: Optional[str] = None
    data_recebimento: Optional[str] = None

    class Config:
        from_attributes = True


#cadastro_id = st.session_state.get("cadastro_id")  # Pega o cadastro_id da sessão