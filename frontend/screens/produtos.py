import streamlit as st
import requests
import time
import pandas as pd


API_URL = "https://satsystem-production-2931.up.railway.app/produtos/"
API_URL_EMITENTE = "https://satsystem-production-2931.up.railway.app/emitentes/"
API_URL_PRODUTO_ADMIN = "https://satsystem-production-2931.up.railway.app/produtos/admin/"

#API_URL = "http://localhost:8000/emitentes/auth"
# API_URL = "https://humble-yodel-57qvr7v97fvg4r-8000.app.github.dev/pedidos/"
# API_URL = "https://satsystem.streamlit.app/pedidos/"
#API_URL = "https://satsystem-production.up.railway.app/pedidos/"

# Adicionar CSS para reduzir o tamanho da fonte da tabela


def exibir_produtos(emitente_id):
    try:
        response = requests.get(f"{API_URL}emitentes/{emitente_id}")
        response.raise_for_status()
        produtos = response.json()

        if isinstance(produtos, list) and len(produtos) > 0 and isinstance(produtos[0], dict):
            df = pd.DataFrame(produtos)
            st.dataframe(df.tail(10), use_container_width=True, hide_index=True)
        else:
            st.error("Sem produtos gerados no Sistema.")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao carregar produtos: {e}")



def exibir_produtos_admin():
    try:
        response = requests.get(f"{API_URL}")
        response.raise_for_status()
        produtos = response.json()

        if isinstance(produtos, list) and len(produtos) > 0 and isinstance(produtos[0], dict):
            df = pd.DataFrame(produtos)
            st.dataframe(df.tail(10), use_container_width=True, hide_index=True)
        else:
            st.error("Sem produtos gerados no Sistema.")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao carregar produtos: {e}")



def atualizar_produtos(emitente_id):
    """Formulário para atualizar um campo do emitente (semelhante ao Swagger)."""
    with st.form(key="update_form_produto", clear_on_submit=True):
        # 🔹 Entrada do ID do emitente
        id_produto = st.text_input("ID do produto a ser atualizado:", "")

        # 🔹 Seleção do campo a ser atualizado
        if emitente_id == 0:
            opcao = st.selectbox(
                "Escolha o campo para atualização:",
                ["id", "codigo", "descricao", "ncm", "cest", "cfop", "unidade_comercial", "unidade_tributavel", "ean", "ean_tributavel", "preco_unitario", "origem_icms", "csosn", "pis_modalidade", "cofins_modalidade", "valor_tributos_aprox", "emitente_id"]
            )
        else:
            opcao = st.selectbox(
                "Escolha o campo para atualização:",
                ["preco_unitario"]
            )

        # 🔹 Novo valor para o campo escolhido
        novo_valor = st.text_input(f"Novo valor:")

        # 🔹 Botão para atualizar o emitente
        if st.form_submit_button("Atualizar produto"):
            if not id_produto.strip():
                st.warning("Por favor, insira um Código válido para atualização.")
                return
            if not novo_valor.strip():
                st.warning("Por favor, insira um valor para atualização.")
                return

            try:
                # 🔹 Converte os tipos de dados corretamente
                if opcao == "preco_unitario":
                    try:
                        novo_valor = float(novo_valor)
                    except ValueError:
                        st.error("O campo 'preco_unitario' deve ser um número inteiro.")
                        return
                
                # 🔹 Monta o JSON para enviar na requisição
                update_data = {opcao: novo_valor}

                # 🔹 Envia a requisição PATCH para atualizar o emitente
                #response = requests.patch(f"{API_URL}{id_produto}", json=update_data)
                response = requests.patch(f"{API_URL_PRODUTO_ADMIN}produto_admin/{id_produto}", json=update_data)
                response.raise_for_status()

                st.success("Produto atualizado com sucesso!")
                time.sleep(2)
                st.rerun()
                exibir_produtos()
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao atualizar produto: {e}")
                time.sleep(2)
                st.rerun()
                exibir_produtos()



def atualizar_produtos_admin():
    """Formulário para atualizar um campo do emitente (semelhante ao Swagger)."""
    with st.form(key="update_form_produto_admin", clear_on_submit=True):
        # 🔹 Entrada do ID do emitente
        id_produto = st.text_input("ID do produto a ser atualizado:", "")

        # 🔹 Seleção do campo a ser atualizado
        opcao = st.selectbox(
            "Escolha o campo para atualização:",
            ["id", "codigo", "descricao", "ncm", "cest", "cfop", "unidade_comercial", "unidade_tributavel", "ean", "ean_tributavel", "preco_unitario", "origem_icms", "csosn", "pis_modalidade", "cofins_modalidade", "valor_tributos_aprox", "emitente_id"]
        )

        # 🔹 Novo valor para o campo escolhido
        novo_valor = st.text_input(f"Novo valor:")

        # 🔹 Botão para atualizar o emitente
        if st.form_submit_button("Atualizar produto"):
            if not id_produto.strip():
                st.warning("Por favor, insira um Código válido para atualização.")
                return
            if not novo_valor.strip():
                st.warning("Por favor, insira um valor para atualização.")
                return

            try:
                # 🔹 Converte os tipos de dados corretamente
                if opcao == "preco_unitario":
                    try:
                        novo_valor = float(novo_valor)
                    except ValueError:
                        st.error("O campo 'preco_unitario' deve ser um número inteiro.")
                        return
                
                # 🔹 Monta o JSON para enviar na requisição
                update_data = {opcao: novo_valor}

                # 🔹 Envia a requisição PATCH para atualizar o emitente
                #response = requests.patch(f"{API_URL}{id}", json=update_data)
                response = requests.patch(f"{API_URL_PRODUTO_ADMIN}produto_admin/{id_produto}", json=update_data)

                response.raise_for_status()

                st.success("Produto atualizado com sucesso!")
                time.sleep(2)
                st.rerun()
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao atualizar produto: {e}")
                time.sleep(2)
                st.rerun()




def criar_produto():
    with st.form(key="produto_form", clear_on_submit=False):
        if "ativo" not in st.session_state:
            st.session_state["ativo"] = True
        codigo = st.text_input("Código Produto:")
        #descricao = st.text_input("Descrição do Cadastro")
        #st.session_state["status"] = st.selectbox("Status", [True, False], index=[True, False].index(st.session_state["status"]))
        default_ativo = st.session_state.get("ativo", False)  # Se None, assume False
        #default_codigo_regime = st.session_state.get("codigo_de_regime_tributario", "1")  # Assumindo 1 como default válido
        st.session_state["ativo"] = st.selectbox("ativo:", [True, False], index=[True, False].index(default_ativo))
        
        #cnpj = st.text_input("CNPJ Estabelecimento",  key="cnpj")
        descricao = st.text_input("Descrição:")
        ncm = st.text_input("Código NCM")
        cest = st.text_input("CEST:")
        cfop = st.text_input("CFOP:", key="cfop")
        unidades = [
                        
                    ("UN", "Unidade"),
                    ("KG", "Quilograma"),
                    ("G", "Grama"),
                    ("L", "Litro"),
                    ("M", "Metro"),
                    ("M2", "Metro quadrado"),
                    ("M3", "Metro cúbico"),
                    ("CX", "Caixa"),
                    ("PCT", "Pacote"),
                    ("PC", "Peça"),
                    ("DZ", "Dúzia"),
                    ("PAR", "Par"),
                    ("FD", "Fardo"),
                    ("SC", "Saco"),
                    ("RL", "Rolo")
             ]
        #unidade_comercial = st.selectbox("Status:", ["pendente", "concluído", "cancelado"])
        default_unidade_produto = "Unidade"
        unidade_comercial = st.selectbox(
            "Unidade Comercial:",
            [codigo for codigo, nome  in unidades],
            index=[i for i, v in enumerate(unidades) if v[1] == default_unidade_produto][0]
        )
        unidade_tributavel = unidade_comercial
        ean = st.text_input("Código EAN")
        ean_tributavel = ean #código de barras
        preco_unitario = st.number_input("Preço Unitário:", min_value=0.0, format="%.2f")
        origem_icms = 0
        csosn = '400'
        pis_modalidade ='07'
        cofins_modalidade ='07'
        valor_tributos_aprox = st.number_input("Percentual Tributo do Produto:", min_value=0.0, format="%.2f")
        #emitente_id = preco_unitario = st.number_input("ID do EMITENTE:", min_value=0.0, format="%.2f")
        emitente_id = st.number_input("ID do EMITENTE:", min_value=0, max_value=99, step=1, format="%d")
        # if st.button("Verificar ID"):
        #     if emitente_id in ids_validos:
        #         st.success(f"ID {emitente_id} encontrado!")
        #     else:
        #         st.error("ID não existe.")
        if st.form_submit_button("Criar Produto"):
            if not codigo or not ncm:
                st.warning("Código e NCM são obrigatórios!")
                return

            data = {
                        "ativo": st.session_state["ativo"],
                        "codigo": codigo,
                        "descricao": descricao,
                        "ncm": ncm,
                        "cest": cest,
                        "cfop": cfop,
                        "unidade_comercial": unidade_comercial,
                        "unidade_tributavel": unidade_tributavel,  # Converte string para booleano
                        "ean": ean,
                        "ean_tributavel": ean_tributavel,
                        "preco_unitario": preco_unitario,
                        "origem_icms": origem_icms,
                        "csosn": csosn,
                        "pis_modalidade": pis_modalidade,
                        "cofins_modalidade": cofins_modalidade,
                        "valor_tributos_aprox": valor_tributos_aprox,
                        "emitente_id": emitente_id
                    }

            print(f"Enviando o seguinte JSON: {data}")

            try:
                response = requests.post(API_URL, json=data)
                response.raise_for_status()
                st.success("Produto Adicionado com Sucesso!")
                time.sleep(2)
                st.rerun()  # Atualiza a página automaticamente
            except requests.exceptions.RequestException as e:
                #e = ("Mail Estabelecimento, Senha, Telefone Responsável, Mail Estabelecimento, Licença, Bairro Estabelecimento, Número Estabelecimento, Endereço Estabelecimento, Telefone Estabelecimento, IE Estabelecimento, CNPJ Estabelecimento e Razão Social são obrigatórios.")
                st.error(f"Erro ao adicionar Produto: {e}")