from sqlalchemy.orm import Session
from backend.models.cadastro import Cadastro, CadastroBase

def get_cadastros(db: Session):
    """ Retorna todos os cadastros do banco de dados. """
    return db.query(Cadastro).all()

def get_cadastro(db: Session, cadastro_id: int):
    """ Retorna um cadastros específico pelo ID. """
    return db.query(Cadastro).filter(Cadastro.id == cadastro_id).first()

def criar_cadastro(db: Session, cadastro_data: CadastroBase):
    """ Cria um novo cadastros no banco de dados. """
    novo_cadastro = Cadastro(**cadastro_data.dict())
    db.add(novo_cadastro)
    db.commit()
    db.refresh(novo_cadastro)
    return novo_cadastro

def atualizar_cadastro(db: Session, cadastro_id: int, cadastro_data: CadastroBase):
    """ Atualiza um cadastros existente. """
    cadastro = db.query(Cadastro).filter(Cadastro.id == cadastro_id).first()
    if not cadastro:
        return None
    
    cadastro.descricao = cadastro_data.descricao
    cadastro.status = cadastro_data.status
    cadastro.nome = cadastro_data.nome
    cadastro.cnpj = cadastro_data.cnpj
    cadastro.ie = cadastro_data.ie
    cadastro.data_criacao = cadastro_data.data_criacao
    cadastro.licenca = cadastro_data.licenca
    cadastro.endereco = cadastro_data.endereco
    cadastro.mail = cadastro_data.mail
    cadastro.telefone = cadastro_data.telefone
    cadastro.password = cadastro_data.password

    db.commit()
    db.refresh(cadastro)
    return cadastro

def deletar_cadastro(db: Session, cadastro_id: int):
    """ Remove um cadastros pelo ID. """
    cadastro = db.query(Cadastro).filter(Cadastro.id == cadastro_id).first()
    if not cadastro:
        return None
    
    db.delete(cadastro)
    db.commit()
    return True
