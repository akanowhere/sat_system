import streamlit as st
import requests

print("sys.path:", sys.path)

#API_URL = "http://localhost:8000/pedidos/"
API_URL = "https://humble-yodel-57qvr7v97fvg4r-8000.app.github.dev/pedidos/"

def exibir_pedidos():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        pedidos = response.json()
        
        # Debug: Verificar estrutura dos pedidos
        #st.write("Dados recebidos:", pedidos)
        
        if isinstance(pedidos, list) and len(pedidos) > 0 and isinstance(pedidos[0], dict):
            st.table(pedidos)
        else:
            st.error("Formato inesperado de resposta da API!")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao carregar pedidos: {e}")
        

def adicionar_pedido():
    descricao = st.text_input("Descrição do Pedido")
    status = st.selectbox("Status", ["pendente", "concluído", "cancelado"])
    valor_total = st.number_input("Valor Total", min_value=0.0, format="%.2f")

    if st.button("Adicionar_Pedido"):
        if not descricao or valor_total <= 0:
            st.warning("Descrição e valor total são obrigatórios!")
            return
        
        data = {"descricao": descricao, "status": status, "valor_total": valor_total}

        try:
            response = requests.post(API_URL, json=data)
            response.raise_for_status()
            st.success("Pedido Adicionado!")
            st.rerun()  # Atualiza a página automaticamente
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao adicionar pedido: {e}")
