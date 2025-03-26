from sqlalchemy.orm import Session
from backend.models.pedido import Pedido, PedidoBase

def get_pedidos(db: Session):
    """ Retorna todos os pedidos do banco de dados. """
    return db.query(Pedido).all()

def get_pedido(db: Session, pedido_id: int):
    """ Retorna um pedido específico pelo ID. """
    return db.query(Pedido).filter(Pedido.id == pedido_id).first()

def criar_pedido(db: Session, pedido_data: PedidoBase):
    """ Cria um novo pedido no banco de dados. """
    novo_pedido = Pedido(**pedido_data.dict())
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    return novo_pedido

def atualizar_pedido(db: Session, pedido_id: int, pedido_data: PedidoBase):
    """ Atualiza um pedido existente. """
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        return None
    
    pedido.descricao = pedido_data.descricao
    pedido.status = pedido_data.status
    pedido.valor_total = pedido_data.valor_total
    pedido.data_criacao = pedido_data.data_criacao

    db.commit()
    db.refresh(pedido)
    return pedido

def deletar_pedido(db: Session, pedido_id: int):
    """ Remove um pedido pelo ID. """
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        return None
    
    db.delete(pedido)
    db.commit()
    return True

def get_pedidos_id(db: Session, emitente_id: int):
    """ Retorna todos os pedidos de um determinado cadastro. """
    return db.query(Pedido).filter(Pedido.emitente_id == emitente_id).all()
