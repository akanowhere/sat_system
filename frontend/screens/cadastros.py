import streamlit as st
import requests

#API_URL = "http://localhost:8000/cadastros/"
API_URL = "https://satsystem-production.up.railway.app/cadastros/"


def exibir_cadastro():
    # Input para inserir o ID do Cadastro
    id_cadastro = st.text_input("Número do Cadastro", "")

    # Botão para buscar o cadastro na API
    if st.button("Buscar Cadastro"):
        if not id_cadastro.strip():
            st.warning("Por favor, insira um ID de cadastro.")
            return
        
        try:
            response = requests.get(f"{API_URL}{id_cadastro}")  # Chama a API com o ID inserido
            response.raise_for_status()
            cadastros = response.json()

            # Verifica se há dados antes de exibir a tabela
            if isinstance(cadastros, dict) and cadastros:
                st.table([cadastros])  # Exibe os dados formatados como uma tabela
            else:
                st.warning("Nenhum cadastro encontrado para esse ID.")
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao buscar cadastro: {e}")
        

def criar_cadastro():
    descricao = st.text_input("Descrição do Cadastro")
    status = st.selectbox("Status", ["true", "false"])
    nome = st.text_input("Nome Estabelecimento")
    cnpj = st.text_input("CNPJ Estabelecimento")
    ie = st.text_input("IE Estabelecimento")
    endereco = st.text_input("Endereço Estabelecimento")
    mail = st.text_input("Mail Estabelecimento")
    password = st.text_input("Senha")


    if st.button("Criar Cadastro"):
        if not descricao or cnpj <= 0:
            st.warning("Descrição e CNPJ são obrigatórios!")
            return
        
        data = {"descricao": descricao, "status": status, "nome": nome, "cnpj": cnpj, "ie": ie}

        try:
            response = requests.post(API_URL, json=data)
            response.raise_for_status()
            st.success("Cadastro Adicionado!")
            st.rerun()  # Atualiza a página automaticamente
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao adicionar cadastro: {e}")
