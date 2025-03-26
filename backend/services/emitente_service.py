from sqlalchemy.orm import Session
from backend.models.emitente import Emitente, EmitenteBase, EmitenteUpdate

def get_emitentes(db: Session):
    """ Retorna todos os emitentes do banco de dados. """
    return db.query(Emitente).all()

def get_emitente(db: Session, emitente_id: int):
    """ Retorna um emitentes específico pelo ID. """
    return db.query(Emitente).filter(Emitente.id == emitente_id).first()

def criar_emitente(db: Session, emitente_data: EmitenteBase):
    """ Cria um novo emitentes no banco de dados. """
    novo_emitente = Emitente(**emitente_data.dict())
    db.add(novo_emitente)
    db.commit()
    db.refresh(novo_emitente)
    return novo_emitente

def atualizar_emitente(db: Session, emitente_id: int, emitente_data: EmitenteBase):
    """ Atualiza um emitentes existente. """
    emitente = db.query(Emitente).filter(Emitente.id == emitente_id).first()
    if not emitente:
        return None
    
    emitente.descricao = emitente_data.descricao
    emitente.status = emitente_data.status
    emitente.nome = emitente_data.nome
    emitente.cnpj = emitente_data.cnpj
    emitente.ie = emitente_data.ie
    emitente.data_criacao = emitente_data.data_criacao
    emitente.licenca = emitente_data.licenca
    emitente.endereco = emitente_data.endereco
    emitente.mail = emitente_data.mail
    emitente.telefone = emitente_data.telefone
    emitente.password = emitente_data.password

    db.commit()
    db.refresh(emitente)
    return emitente

def deletar_emitente(db: Session, emitente_id: int):
    """ Remove um emitentes pelo ID. """
    emitente = db.query(Emitente).filter(Emitente.id == emitente_id).first()
    if not emitente:
        return None
    
    db.delete(emitente)
    db.commit()
    return True



def atualizar_emitente_parcial(db: Session, emitente_id: int, emitente_data: EmitenteUpdate):
    """ Atualiza um emitente parcialmente. """
    emitente = db.query(Emitente).filter(Emitente.id == emitente_id).first()
    
    if not emitente:
        return None
    
    # Atualiza apenas os campos fornecidos pelo usuário
    for key, value in emitente_data.dict(exclude_unset=True).items():
        setattr(emitente, key, value)

    db.commit()
    db.refresh(emitente)
    return emitente
