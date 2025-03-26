import streamlit as st
import requests
import time
import pandas as pd

# Garantir que as variáveis de estado sejam inicializadas
# if "status" not in st.session_state:
#     st.session_state["status"] = True

# if "emitente_data" not in st.session_state:
#     st.session_state["emitente_data"] = None  # Armazena os dados da API


#API_URL = "http://localhost:8000/emitentes/"


st.session_state.clear()

API_URL = "https://satsystem-production.up.railway.app/emitentes/"



if "status" not in st.session_state:
    st.session_state["status"] = True

if "emitente_data" not in st.session_state:
    st.session_state["emitente_data"] = None  # Armazena os dados da API


def exibir_emitente():
    with st.form(key="emitente_view_form", clear_on_submit=True):
        if "emitente_data" not in st.session_state:
            st.session_state["emitente_data"] = None  # Armazena os dados da API
        id_emitente = st.text_input("Número do emitente:", "")

        if st.form_submit_button("Buscar emitente"):
            if not id_emitente.strip():
                st.warning("Por favor, insira um ID de emitente.")
                return

            try:
                response = requests.get(f"{API_URL}{id_emitente}")
                response.raise_for_status()
                emitentes = response.json()

                if isinstance(emitentes, dict) and emitentes:
                    st.session_state["emitente_data"] = [emitentes]  # Salva os dados
                else:
                    st.session_state["emitente_data"] = None
                    st.warning("Nenhum emitente encontrado para esse ID.")
                    time.sleep(2)
                    st.rerun()  # Atualiza a página automaticamente
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao buscar emitente: {e}")
                time.sleep(2)
                st.rerun()  # Atualiza a página automaticamente
                st.session_state["emitente_data"] = None

        # Exibir a tabela se houver dados salvos e retirar opções suspensas df
        if st.session_state["emitente_data"]:
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
                
            #st.table(st.session_state["emitente_data"])
            df = pd.DataFrame(st.session_state["emitente_data"])

              # 🔹 **Selecionar colunas específicas**
            colunas_desejadas = ["id", "nome", "email", "data_criacao"]  # Altere conforme necessário
            df = df[colunas_desejadas] if all(col in df.columns for col in colunas_desejadas) else df

            # 🔹 **Melhor opção para exibição**
            st.dataframe(df, use_container_width=True, hide_index=True)

            # 🔹 **Opção alternativa: Tabela Estática**
            # st.table(df)


def atualizar_emitente():
    """Formulário para atualizar um campo do emitente (semelhante ao Swagger)."""
    with st.form(key="update_form", clear_on_submit=True):
        # 🔹 Entrada do ID do emitente
        emitente_id = st.text_input("ID do emitente a ser atualizado:", "")

        # 🔹 Seleção do campo a ser atualizado
        opcao = st.selectbox(
            "Escolha o campo para atualização:",
            ["razao_social", "nome_fantasia", "cnpj", "inscricao_estadual", "cnae_fiscal", "inscricao_municipal", "inscricao_estadual_subst_tributaria", "codigo_de_regime_tributario", "endereco_logradouro", "endereco_numero", "endereco_complemento", "endereco_bairro", "endereco_cep", "endereco_pais", "endereco_uf", "endereco_municipio", "endereco_cod_municipio", "endereco_telefone", "status", "licenca", "mail", "telefone", "password", "cert", "senha_cert", "cod_seguranca"]
        )

        # 🔹 Novo valor para o campo escolhido
        novo_valor = st.text_input(f"Novo valor:")

        # 🔹 Botão para atualizar o emitente
        if st.form_submit_button("Atualizar emitente"):
            if not emitente_id.strip():
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

                # 🔹 Envia a requisição PATCH para atualizar o emitente
                response = requests.patch(f"{API_URL}{emitente_id}", json=update_data)
                response.raise_for_status()

                st.success("emitente atualizado com sucesso!")
                time.sleep(2)
                st.rerun()
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao atualizar emitente: {e}")
                time.sleep(2)
                st.rerun()



def criar_emitente():
    with st.form(key="cadastro_form", clear_on_submit=True):
        if "status" not in st.session_state:
            st.session_state["status"] = True
        cnpj = st.text_input("CNPJ Estabelecimento:")
        #descricao = st.text_input("Descrição do Cadastro")
        #st.session_state["status"] = st.selectbox("Status", [True, False], index=[True, False].index(st.session_state["status"]))
        default_status = st.session_state.get("status", False)  # Se None, assume False
        st.session_state["status"] = st.selectbox("Status:", [True, False], index=[True, False].index(default_status))
        
        #cnpj = st.text_input("CNPJ Estabelecimento",  key="cnpj")
        password = st.text_input("Senha:")
        cod_seguranca = st.text_input("Código Segurança:")
        licenca = st.text_input("Licença:")
        razao_social = st.text_input("Razão Social:", key="razao_social")
        nome_fantasia = st.text_input("Nome Estabelecimento:", key="nome_fantasia")
        inscricao_estadual = st.text_input("IE Estabelecimento:", key="inscricao_estadual")
        cnae_fiscal = st.text_input("CNAE:", key="cnae_fiscal:")
        inscricao_municipal = st.text_input("Mail Estabelecimento:", key="inscricao_municipal")
        #codigo_de_regime_tributario = st.text_input("Telefone Estabelecimento:", key="codigo_de_regime_tributario")
        endereco_logradouro = st.text_input("Endereço Estabelecimento:", key="endereco_logradouro")
        endereco_numero = st.text_input("Número Estabelecimento:", key="endereco_numero")
        endereco_complemento = st.text_input("Complemento Estabelecimento:", key="endereco_complemento")
        endereco_bairro = st.text_input("Bairro Estabelecimento:", key="endereco_bairro")
        endereco_cep = st.text_input("Cep Estabelecimento:", key="endereco_cep")
        endereco_pais = st.text_input("País Estabelecimento:", key="endereco_pais")
        endereco_uf = st.text_input("Estado Estabelecimento:", key="endereco_uf")
        endereco_municipio = st.text_input("Município Estabelecimento:", key="endereco_municipio")
        mail = st.text_input("Mail Estabelecimento:")
        telefone = st.text_input("Telefone Responsável:")
        cert = st.text_input("Nome Certificado Estabelecimento:")
        senha_cert = st.text_input("Senha Certificado Estabelecimento:")

        if st.form_submit_button("Criar Cadastro"):
            if not password or not cnpj:
                st.warning("Senha e CNPJ são obrigatórios!")
                return

            #data = {"status": st.session_state["status"], "cnpj": cnpj, "mail": mail, "telefone": telefone, "password": password, "licenca" : licenca}
            data = {
                        "status": st.session_state["status"],
                        "cnpj": cnpj,
                        "mail": mail,
                        "telefone": telefone,
                        "password": password,
                        "cod_seguranca": cod_seguranca,
                        "licenca": licenca,  # Converte string para booleano
                        "razao_social": razao_social,
                        "nome_fantasia": nome_fantasia,
                        "inscricao_estadual": inscricao_estadual,
                        "cnae_fiscal": cnae_fiscal,
                        "inscricao_municipal": inscricao_municipal,
                        #"codigo_de_regime_tributario": codigo_de_regime_tributario,
                        "endereco_logradouro": endereco_logradouro,
                        "endereco_numero": endereco_numero,
                        "endereco_complemento": endereco_complemento,
                        "endereco_bairro": endereco_bairro,
                        "endereco_cep": endereco_cep,
                        "endereco_pais": endereco_pais,
                        "endereco_uf": endereco_uf,
                        "endereco_municipio": endereco_municipio,
                        "cert": cert,
                        "senha_cert": senha_cert
                    }

            print(f"Enviando o seguinte JSON: {data}")

            try:
                response = requests.post(API_URL, json=data)
                response.raise_for_status()
                st.success("Cadastro Adicionado com Sucesso!")
                time.sleep(2)
                st.rerun()  # Atualiza a página automaticamente
            except requests.exceptions.RequestException as e:
                e = ("Mail Estabelecimento, Senha, Telefone Responsável, Mail Estabelecimento, Licença, Bairro Estabelecimento, Número Estabelecimento, Endereço Estabelecimento, Telefone Estabelecimento, IE Estabelecimento, CNPJ Estabelecimento e Razão Social são obrigatórios.")
                st.error(f"Erro ao adicionar cadastro: {e}")