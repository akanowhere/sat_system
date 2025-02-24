import streamlit as st

# Credenciais fixas para teste
#USERNAME = "admin"
USERNAME = "65650764000178"
PASSWORD = "1234"

def autenticar():
    st.title("Sistema de Pedidos SAT")
    # Se o usuário já estiver autenticado, retorna os dados
    if st.session_state.get("authenticated"):
        return st.session_state["username"], True

    # Exibe formulário de login
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.rerun()  # Recarrega a página para mostrar a tela principal
        else:
            st.error("Usuário ou senha incorretos")

    return None, False  # Se não autenticado, retorna falso
