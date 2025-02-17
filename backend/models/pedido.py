from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

from backend.db.connection import Base

# Modelo SQLAlchemy para o banco de dados
class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    status = Column(String, default="pendente")
    valor_total = Column(Float, nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)

    pagamentos = relationship("Pagamento", back_populates="pedido", cascade="all, delete-orphan")


# Modelo Pydantic para resposta
# Modelo Pydantic para resposta
class PedidoBase(BaseModel):
    #descricao: str
    descricao: str = Field(..., min_length=1, max_length=255, description="Descrição do pedido")
    status: str = "pendente"
    valor_total: float
    data_criacao: Optional[datetime] = None  # Opcional, será automaticamente atribuído ao criar
    #data_criacao: datetime

    class Config:
        from_attributes = True

