from sqlalchemy.orm import Session
from backend.models.pagamento import Pagamento
from backend.models.pedido import Pedido

def realizar_pagamento(db: Session, pedido_id: int, valor: float, metodo: str):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        return {"error": "Pedido não encontrado"}
    
    pagamento = Pagamento(pedido_id=pedido_id, valor=valor, metodo=metodo)
    db.add(pagamento)
    db.commit()
    db.refresh(pagamento)

    return pagamento

def listar_pagamentos(db: Session):
    return db.query(Pagamento).all()
