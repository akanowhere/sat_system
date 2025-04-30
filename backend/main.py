from fastapi import FastAPI
from backend.api.sat import router as sat_router
from backend.api.pedidos import router as pedidos_router
from backend.api.pagamentos import router as pagamentos_router
from backend.api.cadastros import router as cadastros_router
from backend.api.emitente import router as emitentes_router
from backend.api.emitente import router as emitentes_router
from backend.api.produtos import router as produtos_router

# Criação da instância FastAPI
app = FastAPI()

# Incluir as rotas na aplicação
app.include_router(sat_router, prefix="/sat", tags=["sat"])
app.include_router(pedidos_router, prefix="/pedidos", tags=["pedidos"])
app.include_router(pagamentos_router, prefix="/pagamentos", tags=["pagamentos"])
app.include_router(cadastros_router, prefix="/cadastros", tags=["cadastros"])
app.include_router(cadastros_router, prefix="/auth", tags=["auth"])
app.include_router(emitentes_router, prefix="/emitentes", tags=["emitentes"])
app.include_router(produtos_router, prefix="/produtos", tags=["produtos"])
app.include_router(produtos_router, prefix="/produtos/admin", tags=["produtos/admin"])


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do Restaurante SAT"}

if __name__ == "__main__":
     uvicorn.run(app, host="0.0.0.0", port=8501)