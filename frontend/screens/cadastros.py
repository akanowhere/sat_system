import streamlit as st
import requests
import time
import pandas as pd

# Garantir que as variáveis de estado sejam inicializadas
# if "status" not in st.session_state:
#     st.session_state["status"] = True

# if "cadastro_data" not in st.session_state:
#     st.session_state["cadastro_data"] = None  # Armazena os dados da API

API_URL = "http://localhost:8000/cadastros/"





st.session_state.clear()

#API_URL = "https://satsystem-production.up.railway.app/cadastros/"
#API_URL = "https://satsystem-production-2931.up.railway.app/cadastros/"



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

        # Exibir a tabela se houver dados salvos e retirar opções suspensas df
        if st.session_state["cadastro_data"]:
            st.markdown(
                            """
                            <style>
                            [data-testid="stElementToolbar"] {
                                display: none;
                            }
                            </style>
                            """,
                            unsafe_allow_html=True
                        )
                
            #st.table(st.session_state["cadastro_data"])
            df = pd.DataFrame(st.session_state["cadastro_data"])

              # 🔹 **Selecionar colunas específicas**
            colunas_desejadas = ["id", "nome", "email", "data_cadastro"]  # Altere conforme necessário
            df = df[colunas_desejadas] if all(col in df.columns for col in colunas_desejadas) else df

            # 🔹 **Melhor opção para exibição**
            st.dataframe(df, use_container_width=True, hide_index=True)

            # 🔹 **Opção alternativa: Tabela Estática**
            # st.table(df)


def atualizar_cadastro():
    """Formulário para atualizar um campo do cadastro (semelhante ao Swagger)."""
    with st.form(key="update_form", clear_on_submit=True):
        # 🔹 Entrada do ID do cadastro
        cadastro_id = st.text_input("ID do Cadastro a ser atualizado:", "")

        # 🔹 Seleção do campo a ser atualizado
        opcao = st.selectbox(
            "Escolha o campo para atualização:",
            ["descricao", "status", "nome", "cnpj", "ie", "licenca", "endereco", "mail", "telefone", "password"]
        )

        # 🔹 Novo valor para o campo escolhido
        novo_valor = st.text_input(f"Novo valor:")

        # 🔹 Botão para atualizar o cadastro
        if st.form_submit_button("Atualizar Cadastro"):
            if not cadastro_id.strip():
                st.warning("Por favor, insira um ID válido para atualização.")
                return
            if not novo_valor.strip():
                st.warning("Por favor, insira um valor para atualização.")
                return

            try:
                # 🔹 Converte os tipos de dados corretamente
                if opcao == "status":
                    novo_valor = novo_valor.lower() in ["true", "1", "yes", "sim"]
                elif opcao == "licenca":
                    try:
                        novo_valor = int(novo_valor)
                    except ValueError:
                        st.error("O campo 'licenca' deve ser um número inteiro.")
                        return

                # 🔹 Monta o JSON para enviar na requisição
                update_data = {opcao: novo_valor}

                # 🔹 Envia a requisição PATCH para atualizar o cadastro
                response = requests.patch(f"{API_URL}{cadastro_id}", json=update_data)
                response.raise_for_status()

                st.success("Cadastro atualizado com sucesso!")
                time.sleep(2)
                st.rerun()
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao atualizar cadastro: {e}")
                time.sleep(2)
                st.rerun()



def criar_cadastro():
    with st.form(key="cadastro_form", clear_on_submit=True):
        if "status" not in st.session_state:
            st.session_state["status"] = True
        descricao = st.text_input("Descrição do Cadastro")
        #st.session_state["status"] = st.selectbox("Status", [True, False], index=[True, False].index(st.session_state["status"]))
        default_status = st.session_state.get("status", False)  # Se None, assume False
        st.session_state["status"] = st.selectbox("Status", [True, False], index=[True, False].index(default_status))
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