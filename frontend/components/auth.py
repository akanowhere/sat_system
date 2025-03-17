import streamlit as st
import requests

# API de autenticação no backend
#API_URL = "http://localhost:8000/cadastros/auth"  # Certifique-se de que está correto
#API_URL = "https://satsystem-production.up.railway.app/cadastros/auth"
API_URL = "https://satsystem-production-2931.up.railway.app/cadastros/auth"

def autenticar():
    # st.markdown(
    # "<h1 style='text-align: center; font-size: 50px; color: black'>Sistema de Pedidos NFC-e</h1>",
    # unsafe_allow_html=True
    #     )
    
    st.markdown(
    "<div style='text-align: center; font-size: 50px; font-weight: bold; color: black'>Sistema de Pedidos NFC-e</div>",
    unsafe_allow_html=True
        )

    #st.title("Sistema de Pedidos SAT")

    if st.session_state.get("authenticated"):
        return st.session_state["cnpj"], True, st.session_state.get("cadastro_id"), st.session_state.get("licenca"), st.session_state.get("cert"), st.session_state.get("key")#, st.session_state.get("status")

    cnpj = st.text_input("CNPJ")
    password = st.text_input("Senha", type="password")

    if st.button("Login"):
        response = requests.post(API_URL, json={"cnpj": cnpj, "password": password})

        #st.write("Response JSON:", response.json())
        #print("Response JSON:", response.json())

        if response.status_code == 200 and response.json().get("authenticated"):
            st.session_state["authenticated"] = True
            st.session_state["cnpj"] = cnpj
            st.session_state["cadastro_id"] = response.json().get("id")  # Busca o ID do cadastro
            st.session_state["licenca"] = response.json().get("licenca")
            st.session_state["cert"] = response.json().get("cert")
            st.session_state["key"] = response.json().get("key")
            #st.write(st.session_state)  # Debug
            st.rerun()
        elif response.status_code == 403:
            st.error("Usuário inativo. Entre em contato com o suporte.")
        else:
            st.error("CNPJ ou senha incorretos")

    return None, None, False, None, None, None