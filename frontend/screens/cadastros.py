import streamlit as st
import requests
import time

# Garantir que as variáveis de estado sejam inicializadas
# if "status" not in st.session_state:
#     st.session_state["status"] = True

# if "cadastro_data" not in st.session_state:
#     st.session_state["cadastro_data"] = None  # Armazena os dados da API

#API_URL = "http://localhost:8000/cadastros/"





st.session_state.clear()

#API_URL = "https://satsystem-production.up.railway.app/cadastros/"
API_URL = "https://satsystem-production-2931.up.railway.app/cadastros/"


if "status" not in st.session_state:
    st.session_state["status"] = True

if "cadastro_data" not in st.session_state:
    st.session_state["cadastro_data"] = None  # Armazena os dados da API


def exibir_cadastro():
    with st.form(key="cadastro_view_form", clear_on_submit=True):
        if "cadastro_data" not in st.session_state:
            st.session_state["cadastro_data"] = None  # Armazena os dados da API
        id_cadastro = st.text_input("Número do Cadastro", "")

        if st.form_submit_button("Buscar Cadastro"):
            if not id_cadastro.strip():
                st.warning("Por favor, insira um ID de cadastro.")
                return

            try:
                response = requests.get(f"{API_URL}{id_cadastro}")
                response.raise_for_status()
                cadastros = response.json()

                if isinstance(cadastros, dict) and cadastros:
                    st.session_state["cadastro_data"] = [cadastros]  # Salva os dados
                else:
                    st.session_state["cadastro_data"] = None
                    st.warning("Nenhum cadastro encontrado para esse ID.")
                    time.sleep(2)
                    st.rerun()  # Atualiza a página automaticamente
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao buscar cadastro: {e}")
                time.sleep(2)
                st.rerun()  # Atualiza a página automaticamente
                st.session_state["cadastro_data"] = None

        # Exibir a tabela se houver dados salvos
        if st.session_state["cadastro_data"]:
            st.table(st.session_state["cadastro_data"])


def criar_cadastro():
    with st.form(key="cadastro_form", clear_on_submit=True):
        if "status" not in st.session_state:
            st.session_state["status"] = True
        descricao = st.text_input("Descrição do Cadastro")
        st.session_state["status"] = st.selectbox("Status", [True, False], index=[True, False].index(st.session_state["status"]))
        nome = st.text_input("Nome Estabelecimento")
        cnpj = st.text_input("CNPJ Estabelecimento")
        ie = st.text_input("IE Estabelecimento")
        endereco = st.text_input("Endereço Estabelecimento")
        mail = st.text_input("Mail Estabelecimento")
        telefone = st.text_input("Telefone Estabelecimento")
        password = st.text_input("Senha")
        licenca = st.text_input("Licença")

        if st.form_submit_button("Criar Cadastro"):
            if not descricao or not cnpj:
                st.warning("Descrição e CNPJ são obrigatórios!")
                return

            data = {"descricao": descricao, "status": st.session_state["status"], "nome": nome, "cnpj": cnpj, "ie": ie, "endereco": endereco, "mail": mail, "telefone": telefone, "password": password, "licenca" : licenca}


            print(f"Enviando o seguinte JSON: {data}")

            try:
                response = requests.post(API_URL, json=data)
                response.raise_for_status()
                st.success("Cadastro Adicionado com Sucesso!")
                time.sleep(2)
                st.rerun()  # Atualiza a página automaticamente
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao adicionar cadastro: {e}")