import streamlit as st
import requests
import time
import pandas as pd

# API_URL = "http://localhost:8000/pedidos/"
# API_URL = "https://humble-yodel-57qvr7v97fvg4r-8000.app.github.dev/pedidos/"
# API_URL = "https://satsystem.streamlit.app/pedidos/"
#API_URL = "https://satsystem-production.up.railway.app/pedidos/"
API_URL = "https://satsystem-production-2931.up.railway.app/pedidos/"

# Adicionar CSS para reduzir o tamanho da fonte da tabela

def exibir_pedidos(cadastro_id):
    try:
        response = requests.get(f"{API_URL}cadastro/{cadastro_id}")
        response.raise_for_status()
        pedidos = response.json()

        if isinstance(pedidos, list) and len(pedidos) > 0 and isinstance(pedidos[0], dict):
            df = pd.DataFrame(pedidos)
            st.dataframe(df.tail(10), use_container_width=True, hide_index=True)
        else:
            st.error("Sem pedidos gerados no Sistema.")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao carregar pedidos: {e}")


def adicionar_pedido(cadastro_id):
    key_descricao = "descricao_" + str(time.time())
    
    with st.form(key="pedido_form", clear_on_submit=True):
        descricao = st.text_input("Descrição do Pedido")
        quantidade = st.number_input("Quantidade", min_value=0.0, format="%.2f")
        
        if quantidade:
            try:
                quantidade = float(quantidade)  # Tenta converter para float
            except ValueError:
                st.error("Por favor, insira um número válido.")
                quantidade = None  # Evita processamento se a conversão falhar
                
        status = st.selectbox("Status", ["pendente", "concluído", "cancelado"])
        valor_total = st.number_input("Valor Total", min_value=0.0, format="%.2f")
        cadastro_id = cadastro_id
      
        if st.form_submit_button("Adicionar Pedido"):
            if not descricao or valor_total is None or quantidade is None or valor_total <= 0 or quantidade <= 0:
                st.warning("Descrição, valor total e quantidade são obrigatórios e precisam ser maiores que 0!")
                return
                
            data = {"descricao": descricao, "status": status, "valor_total": valor_total, "cadastro_id": cadastro_id, "quantidade": quantidade}

            try:
                response = requests.post(API_URL, json=data)
                response.raise_for_status()
                
                st.success("Pedido Adicionado com Sucesso!")
                
                time.sleep(1)
                st.rerun()  # Atualiza a página automaticamente
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao adicionar pedido: {e}")

