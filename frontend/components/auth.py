import streamlit as st
import requests

# API de autenticação no backend
#API_URL = "http://localhost:8000/cadastros/auth"  # Certifique-se de que está correto
#API_URL = "https://satsystem-production.up.railway.app/cadastros/auth"
API_URL = "https://satsystem-production-2931.up.railway.app/cadastros/auth"

def autenticar():
    st.title("Sistema de Pedidos SAT")

    if st.session_state.get("authenticated"):
        return st.session_state["cnpj"], True, st.session_state.get("cadastro_id")

    cnpj = st.text_input("CNPJ")
    password = st.text_input("Senha", type="password")

    if st.button("Login"):
        response = requests.post(API_URL, json={"cnpj": cnpj, "password": password})

        if response.status_code == 200 and response.json().get("authenticated"):
            st.session_state["authenticated"] = True
            st.session_state["cnpj"] = cnpj
            st.session_state["cadastro_id"] = response.json().get("id")
            st.rerun()
        else:
            st.error("CNPJ ou senha incorretos")

    return None, None, False
