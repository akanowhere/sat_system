# pagamento.py
import streamlit as st
import requests

# Exibe os pagamentos existentes
def exibir_pagamentos():
    response = requests.get("http://localhost:8000/pagamentos/")
    if response.status_code == 200:
        pagamentos = response.json()
        if pagamentos:
            st.subheader("Lista de Pagamentos")
            for pagamento in pagamentos:
                st.write(f"**ID:** {pagamento['id']} | **Pedido ID:** {pagamento['pedido_id']} | **Valor Pago:** {pagamento['valor_pago']}")
        else:
            st.write("Nenhum pagamento encontrado.")
    else:
        st.error("Erro ao carregar os pagamentos.")

# Adicionar novo pagamento
def adicionar_pagamento():
    st.subheader("Adicionar Pagamento")

    pedido_id = st.number_input("ID do Pedido", min_value=1)
    valor_pago = st.number_input("Valor Pago", min_value=0.0)

    if st.button("Adicionar Pagamento"):
        data = {"pedido_id": pedido_id, "valor_pago": valor_pago}
        response = requests.post("http://localhost:8000/pagamentos/", json=data)
        if response.status_code == 201:
            st.success("Pagamento Adicionado com Sucesso!")
        else:
            st.error("Erro ao adicionar pagamento.")

# Atualizar pagamento
def atualizar_pagamento():
    pagamento_id = st.number_input("ID do Pagamento a ser Atualizado", min_value=1)
    valor_pago = st.number_input("Novo Valor Pago", min_value=0.0)

    if st.button("Atualizar Pagamento"):
        data = {"valor_pago": valor_pago}
        response = requests.put(f"http://localhost:8000/pagamentos/{pagamento_id}", json=data)
        if response.status_code == 200:
            st.success("Pagamento Atualizado com Sucesso!")
        else:
            st.error("Erro ao atualizar pagamento.")

# Deletar pagamento
def deletar_pagamento():
    pagamento_id = st.number_input("ID do Pagamento a ser Deletado", min_value=1)
    
    if st.button("Deletar Pagamento"):
        response = requests.delete(f"http://localhost:8000/pagamentos/{pagamento_id}")
        if response.status_code == 200:
            st.success("Pagamento Deletado com Sucesso!")
        else:
            st.error("Erro ao deletar pagamento.")

def exibir_pagamento_screen():
    st.sidebar.title("Gestão de Pagamentos")
    menu = ["Ver Pagamentos", "Adicionar Pagamento", "Atualizar Pagamento", "Deletar Pagamento"]
    escolha = st.sidebar.selectbox("Escolha uma ação", menu)

    if escolha == "Ver Pagamentos":
        exibir_pagamentos()
    elif escolha == "Adicionar Pagamento":
        adicionar_pagamento()
    elif escolha == "Atualizar Pagamento":
        atualizar_pagamento()
    elif escolha == "Deletar Pagamento":
        deletar_pagamento()

if __name__ == "__main__":
    exibir_pagamento_screen()
