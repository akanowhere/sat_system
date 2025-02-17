from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel
from backend.db.connection import Base

# Modelo SQLAlchemy para o banco de dados
class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    metodo_pagamento = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    data_pagamento = Column(DateTime, default=datetime.utcnow)

    pedido = relationship("Pedido", back_populates="pagamentos")

# Modelo Pydantic para resposta e criação
class PagamentoBase(BaseModel):
    pedido_id: int
    metodo_pagamento: str
    valor: float
    data_pagamento: datetime = datetime.utcnow()

    class Config:
        from_attributes = True
