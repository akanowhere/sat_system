from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import Query
from backend.db.connection import get_db
from backend.models.pedido import PedidoBase
from backend.services.pedido_service import (
    get_pedidos as get_pedidos_service,
    get_pedido as get_pedido_service,
    criar_pedido as criar_pedido_service,
    atualizar_pedido as atualizar_pedido_service,
    deletar_pedido as deletar_pedido_service,
    get_pedidos_id as get_pedidos_por_cadastro
)

router = APIRouter()

@router.get("/", response_model=list[PedidoBase])
def get_pedidos(db: Session = Depends(get_db)):
    return get_pedidos_service(db)

@router.get("/{pedido_id}", response_model=PedidoBase)
def get_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = get_pedido_service(db, pedido_id)
    if not pedido:
        return {"message": "Pedido não encontrado"}
    return pedido

@router.post("/", response_model=PedidoBase)
def criar_pedido(pedido: PedidoBase, db: Session = Depends(get_db)):
    return criar_pedido_service(db, pedido)

@router.put("/{pedido_id}", response_model=PedidoBase)
def atualizar_pedido(pedido_id: int, pedido: PedidoBase, db: Session = Depends(get_db)):
    pedido_atualizado = atualizar_pedido_service(db, pedido_id, pedido)
    if not pedido_atualizado:
        return {"message": "Pedido não encontrado"}
    return pedido_atualizado

@router.delete("/{pedido_id}")
def deletar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    sucesso = deletar_pedido_service(db, pedido_id)
    if not sucesso:
        return {"message": "Pedido não encontrado"}
    return {"message": "Pedido deletado com sucesso"}

# @router.get("/cadastro/{cadastro_id}", response_model=list[PedidoBase])
# def get_pedidos_id(cadastro_id: int, db: Session = Depends(get_db)):
#     """ Retorna os pedidos filtrados pelo cadastro_id. """
#     return get_pedidos_por_cadastro(db, cadastro_id)

@router.get("/emitentes/{emitente_id}", response_model=list[PedidoBase])
def get_pedidos_id(emitente_id: int, db: Session = Depends(get_db)):
    """ Retorna os pedidos filtrados pelo cadastro_id. """
    return get_pedidos_por_cadastro(db, emitente_id)