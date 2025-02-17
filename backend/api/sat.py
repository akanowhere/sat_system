from fastapi import APIRouter
import ctypes
from unittest import mock


router = APIRouter()

# Carregar a DLL do SAT (ajuste o caminho conforme necessário)
#sat_dll = ctypes.CDLL("C:\\caminho_para\\SAT.dll")

@router.get("/consultar-sat")
def consultar_sat():
    resposta = sat_dll.ConsultarStatusOperacional()
    return {"status_sat": resposta.decode("utf-8")}

@router.post("/enviar-venda/")
def enviar_venda(xml_cupom: str):
    resposta = sat_dll.EnviarDadosVenda(xml_cupom.encode("utf-8"))
    return {"resposta": resposta.decode("utf-8")}




# Mock da DLL
def mock_CDLL(path):
    print(f"Mockando o carregamento da DLL: {path}")
    # Aqui você pode simular qualquer comportamento da DLL se necessário
    return mock.MagicMock()

# Substituindo o `ctypes.CDLL` pela versão mockada
with mock.patch("ctypes.CDLL", side_effect=mock_CDLL):
    sat_dll = ctypes.CDLL("C:\\caminho_para\\SAT.dll")
    # Aqui o código segue como se a DLL fosse carregada normalmente, mas usando o mock
    print(sat_dll)