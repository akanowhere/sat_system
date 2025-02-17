from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.connection import get_db
from backend.models.pagamento import Pagamento, PagamentoBase
from backend.models.pedido import Pedido  # Importa para validar se o pedido existe

router = APIRouter()

@router.get("/", response_model=list[PagamentoBase])
def get_pagamentos(db: Session = Depends(get_db)):
    """
    Obtém todos os pagamentos cadastrados.
    """
    pagamentos = db.query(Pagamento).all()
    return pagamentos

@router.get("/{pagamento_id}", response_model=PagamentoBase)
def get_pagamento(pagamento_id: int, db: Session = Depends(get_db)):
    """
    Obtém um pagamento pelo ID.
    """
    pagamento = db.query(Pagamento).filter(Pagamento.id == pagamento_id).first()
    if not pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    return pagamento

@router.post("/", response_model=PagamentoBase)
def criar_pagamento(pagamento: PagamentoBase, db: Session = Depends(get_db)):
    """
    Registra um novo pagamento para um pedido.
    """
    pedido = db.query(Pedido).filter(Pedido.id == pagamento.pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    db_pagamento = Pagamento(**pagamento.dict())
    db.add(db_pagamento)
    db.commit()
    db.refresh(db_pagamento)

    return db_pagamento

@router.delete("/{pagamento_id}")
def deletar_pagamento(pagamento_id: int, db: Session = Depends(get_db)):
    """
    Remove um pagamento pelo ID.
    """
    pagamento = db.query(Pagamento).filter(Pagamento.id == pagamento_id).first()
    if not pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")

    db.delete(pagamento)
    db.commit()

    return {"message": "Pagamento deletado com sucesso"}
