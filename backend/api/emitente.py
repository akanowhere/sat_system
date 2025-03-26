from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.connection import get_db
from backend.models.emitente import EmitenteBase, Emitente, EmitenteUpdate
from backend.models.auth import LoginRequest  # Certifique-se de que o caminho está correto
from backend.services.emitente_service import (
    get_emitentes as get_emitentes_service,
    get_emitente as get_emitente_service,
    criar_emitente as criar_emitente_service,
    atualizar_emitente as atualizar_emitente_service,
    deletar_emitente as deletar_emitente_service,
    atualizar_emitente_parcial as atualizar_emitente_parcial_service
)

router = APIRouter()

@router.get("/", response_model=list[EmitenteBase])
def get_emitentes(db: Session = Depends(get_db)):
    return get_emitentes_service(db)

@router.get("/{emitente_id}", response_model=EmitenteBase)
def get_emitente(emitente_id: int, db: Session = Depends(get_db)):
    emitente = get_emitente_service(db, emitente_id)
    if not emitente:
        return {"message": "emitente não encontrado"}
    return emitente

@router.post("/", response_model=EmitenteBase)
def criar_emitente(emitente: EmitenteBase, db: Session = Depends(get_db)):
    return criar_emitente_service(db, emitente)

@router.put("/{emitente_id}", response_model=EmitenteBase)
def atualizar_emitente(emitente_id: int, emitente: EmitenteBase, db: Session = Depends(get_db)):
    emitente_atualizado = atualizar_emitente_service(db, emitente_id, emitente)
    if not emitente_atualizado:
        return {"message": "emitente não encontrado"}
    return emitente_atualizado

@router.delete("/{emitente_id}")
def deletar_emitente(emitente_id: int, db: Session = Depends(get_db)):
    sucesso = deletar_emitente_service(db, emitente_id)
    if not sucesso:
        return {"message": "emitente não encontrado"}
    return {"message": "emitente deletado com sucesso"}


@router.post("/auth")
def autenticar(login_data: LoginRequest, db: Session = Depends(get_db)):
    emitente = db.query(Emitente).filter(Emitente.cnpj == login_data.cnpj).first()
    
    if not emitente or emitente.password != login_data.password:
        raise HTTPException(status_code=401, detail="CNPJ ou senha incorretos")
    
    if emitente.status is False:  # Verifica se o status é False
        raise HTTPException(status_code=403, detail="Usuário inativo. Entre em contato com o suporte.")
    
    return {"authenticated": True, "id": emitente.id, "licenca": emitente.licenca, "cert": emitente.cert, "senha_cert": emitente.senha_cert}



@router.patch("/{emitente_id}", response_model=EmitenteBase)
def atualizar_emitente_parcial(emitente_id: int, emitente: EmitenteUpdate, db: Session = Depends(get_db)):
    emitente_atualizado = atualizar_emitente_parcial_service(db, emitente_id, emitente)
    
    if not emitente_atualizado:
        raise HTTPException(status_code=404, detail="emitente não encontrado")

    return emitente_atualizado
