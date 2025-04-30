from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.connection import get_db
from backend.models.produto import ProdutoBase, Produto, ProdutoUpdate
from backend.models.auth import LoginRequest  # Certifique-se de que o caminho está correto
from backend.services.produto_service import (
    get_produtos as get_produtos_service,
    get_produto as get_produto_service,
    criar_produto as criar_produto_service,
    atualizar_produto as atualizar_produto_service,
    deletar_produto as deletar_produto_service,
    atualizar_produto_parcial as atualizar_produto_parcial_service,
    get_produtos_id as get_produto_por_cadastro,
    atualizar_produto_admin as atualizar_produto_parcial_service_admin
)

router = APIRouter()

@router.get("/", response_model=list[ProdutoBase])
def get_produtos(db: Session = Depends(get_db)):
    return get_produtos_service(db)

@router.get("/{produto_id}", response_model=ProdutoBase)
def get_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = get_produto_service(db, produto_id)
    if not produto:
        return {"message": "produto não encontrado"}
    return produto

@router.post("/", response_model=ProdutoBase)
def criar_produto(produto: ProdutoBase, db: Session = Depends(get_db)):
    return criar_produto_service(db, produto)

@router.put("/{produto_id}", response_model=ProdutoBase)
def atualizar_produto(produto_id: int, produto: ProdutoBase, db: Session = Depends(get_db)):
    produto_atualizado = atualizar_produto_service(db, produto_id, produto)
    if not produto_atualizado:
        return {"message": "produto não encontrado"}
    return produto_atualizado

@router.delete("/{produto_id}")
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    sucesso = deletar_produto_service(db, produto_id)
    if not sucesso:
        return {"message": "produto não encontrado"}
    return {"message": "produto deletado com sucesso"}



@router.patch("/{codigo}", response_model=ProdutoBase)
def atualizar_produto_parcial(codigo: str, produto: ProdutoBase, db: Session = Depends(get_db)):
    produto_atualizado = atualizar_produto_parcial_service(db, codigo, produto)
    
    if not produto_atualizado:
        raise HTTPException(status_code=404, detail="produto não encontrado")

    return produto_atualizado


@router.get("/emitentes/{emitente_id}", response_model=list[ProdutoBase])
def get_produtos_id(emitente_id: int, db: Session = Depends(get_db)):
    """ Retorna os produtos filtrados pelo emintente_id. """
    return get_produto_por_cadastro(db, emitente_id)



@router.patch("/produto_admin/{id}", response_model=ProdutoBase)
def atualizar_produto_parcial(id: int, produto: ProdutoBase, db: Session = Depends(get_db)):
    produto_atualizado = atualizar_produto_parcial_service_admin(db, id, produto)
    
    if not produto_atualizado:
        raise HTTPException(status_code=404, detail="produto não encontrado")

    return produto_atualizado