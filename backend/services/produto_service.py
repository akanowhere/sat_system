from sqlalchemy.orm import Session
from backend.models.produto import Produto, ProdutoBase, ProdutoUpdate




def get_produtos(db: Session):
    """ Retorna todos os emitentes do banco de dados. """
    return db.query(Produto).all()

def get_produto(db: Session, produto_id: int):
    """ Retorna um emitentes específico pelo ID. """
    return db.query(Produto).filter(Produto.id == produto_id).first()


def criar_produto(db: Session, produto_data: ProdutoBase):
    """ Cria um novo emitentes no banco de dados. """
    novo_produto = Produto(**produto_data.dict())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

def atualizar_produto(db: Session, produto_id: int, produto_data: ProdutoBase):
    """ Atualiza um emitentes existente. """
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        return None
    
    produto.codigo = produto_data.codigo
    produto.descricao = produto_data.descricao
    produto.ncm = produto_data.ncm
    produto.cfop = produto_data.cfop
    produto.unidade_comercial = produto_data.unidade_comercial
    produto.unidade_tributavel = produto_data.unidade_tributavel
    produto.ean = produto_data.ean
    produto.ean_tributavel = produto_data.ean_tributavel
    produto.preco_unitario = produto_data.preco_unitario
    produto.origem_icms = produto_data.origem_icms
    produto.csosn = produto_data.csosn
    produto.cofins_modalidade = produto_data.cofins_modalidade
    produto.valor_tributos_aprox = produto_data.valor_tributos_aprox
    produto.ativo = produto_data.ativo

    
    db.commit()
    db.refresh(produto)
    return produto

def deletar_produto(db: Session, produto_id: int):
    """ Remove um emitentes pelo ID. """
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        return None
    
    db.delete(produto)
    db.commit()
    return True



def atualizar_produto_parcial(db: Session, codigo: str, produto_data: ProdutoUpdate):
    """ Atualiza um emitente parcialmente. """
    produto = db.query(Produto).filter(Produto.id == id).first()
    
    if not produto:
        return None
    
    # Atualiza apenas os campos fornecidos pelo usuário
    for key, value in produto_data.dict(exclude_unset=True).items():
        setattr(produto, key, value)

    db.commit()
    db.refresh(produto)
    return produto


def get_produtos_id(db: Session, emitente_id: int):
    """ Retorna todos os pedidos de um determinado cadastro. """
    return db.query(Produto).filter(Produto.emitente_id == emitente_id).all()



def atualizar_produto_admin(db: Session, id: int, produto_data: ProdutoUpdate):
    """ Atualiza um produto existente. """
    produto = db.query(Produto).filter(Produto.id == id).first()
    if not produto:
        return None
      
    for key, value in produto_data.dict(exclude_unset=True).items():
            setattr(produto, key, value)

    db.commit()
    db.refresh(produto)
    return produto
