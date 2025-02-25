from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.connection import get_db
from backend.models.cadastro import CadastroBase, Cadastro
from backend.models.auth import LoginRequest  # Certifique-se de que o caminho está correto
from backend.services.cadastro_service import (
    get_cadastros as get_cadastros_service,
    get_cadastro as get_cadastro_service,
    criar_cadastro as criar_cadastro_service,
    atualizar_cadastro as atualizar_cadastro_service,
    deletar_cadastro as deletar_cadastro_service
)

router = APIRouter()

@router.get("/", response_model=list[CadastroBase])
def get_cadastros(db: Session = Depends(get_db)):
    return get_cadastros_service(db)

@router.get("/{cadastro_id}", response_model=CadastroBase)
def get_cadastro(cadastro_id: int, db: Session = Depends(get_db)):
    cadastro = get_cadastro_service(db, cadastro_id)
    if not cadastro:
        return {"message": "Cadastro não encontrado"}
    return cadastro

@router.post("/", response_model=CadastroBase)
def criar_cadastro(cadastro: CadastroBase, db: Session = Depends(get_db)):
    return criar_cadastro_service(db, cadastro)

@router.put("/{cadastro_id}", response_model=CadastroBase)
def atualizar_cadastro(cadastro_id: int, cadastro: CadastroBase, db: Session = Depends(get_db)):
    cadastro_atualizado = atualizar_cadastro_service(db, cadastro_id, cadastro)
    if not cadastro_atualizado:
        return {"message": "Cadastro não encontrado"}
    return cadastro_atualizado

@router.delete("/{cadastro_id}")
def deletar_cadastro(cadastro_id: int, db: Session = Depends(get_db)):
    sucesso = deletar_cadastro_service(db, cadastro_id)
    if not sucesso:
        return {"message": "Cadastro não encontrado"}
    return {"message": "Cadastro deletado com sucesso"}


@router.post("/auth")
def autenticar(login_data: LoginRequest, db: Session = Depends(get_db)):
    cadastro = db.query(Cadastro).filter(Cadastro.cnpj == login_data.cnpj).first()
    
    if not cadastro or cadastro.password != login_data.password:
        raise HTTPException(status_code=401, detail="CNPJ ou senha incorretos")
    
    return {"authenticated": True}