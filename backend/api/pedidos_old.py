from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db.connection import get_db
from backend.models.pedido import Pedido, PedidoBase  # Importando o modelo SQLAlchemy e Pydantic

router = APIRouter()

@router.get("/", response_model=list[PedidoBase])
def get_pedidos(db: Session = Depends(get_db)):
    """
    Obtém todos os pedidos do banco de dados.
    """
    pedidos = db.query(Pedido).all()
    return pedidos

@router.get("/{pedido_id}", response_model=PedidoBase)
def get_pedido(pedido_id: int, db: Session = Depends(get_db)):
    """
    Obtém um pedido específico pelo seu ID.
    """
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if pedido is None:
        return {"message": "Pedido não encontrado"}
    return pedido

@router.post("/", response_model=PedidoBase)
def criar_pedido(pedido: PedidoBase, db: Session = Depends(get_db)):
    """
    Cria um novo pedido.
    """
    db_pedido = Pedido(**pedido.dict())
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

@router.put("/{pedido_id}", response_model=PedidoBase)
def atualizar_pedido(pedido_id: int, pedido: PedidoBase, db: Session = Depends(get_db)):
    """
    Atualiza os dados de um pedido existente.
    """
    db_pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if db_pedido is None:
        return {"message": "Pedido não encontrado"}
    
    db_pedido.descricao = pedido.descricao
    db_pedido.status = pedido.status
    db_pedido.valor_total = pedido.valor_total
    db_pedido.data_criacao = pedido.data_criacao
    
    db.commit()
    db.refresh(db_pedido)
    
    return db_pedido

@router.delete("/{pedido_id}")
def deletar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    """
    Deleta um pedido pelo seu ID.
    """
    db_pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if db_pedido is None:
        return {"message": "Pedido não encontrado"}
    
    db.delete(db_pedido)
    db.commit()
    
    return {"message": "Pedido deletado com sucesso"}
