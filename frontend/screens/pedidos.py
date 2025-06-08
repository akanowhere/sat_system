import streamlit as st
import requests
import time
import pandas as pd
from frontend.components.NFeAutorizacao4 import call_pedido, call_pedido_sem_cpf

#API_URL = "http://localhost:8000/pedidos/"
# API_URL = "https://humble-yodel-57qvr7v97fvg4r-8000.app.github.dev/pedidos/"
# API_URL = "https://satsystem.streamlit.app/pedidos/"
#API_URL = "https://satsystem-production.up.railway.app/pedidos/"
API_URL = "https://satsystem-production-2931.up.railway.app/pedidos/"

# Adicionar CSS para reduzir o tamanho da fonte da tabela

API_URL_EMITENTE = "https://satsystem-production-2931.up.railway.app/emitentes/"
API_URL_PRODUTO = "https://satsystem-production-2931.up.railway.app/produtos/"
#API_URL = "http://localhost:8000/emitentes/auth"
# API_URL = "https://humble-yodel-57qvr7v97fvg4r-8000.app.github.dev/pedidos/"
# API_URL = "https://satsystem.streamlit.app/pedidos/"
#API_URL = "https://satsystem-production.up.railway.app/pedidos/"

# Adicionar CSS para reduzir o tamanho da fonte da tabela


def exibir_pedidos(emitente_id):
    try:
        response = requests.get(f"{API_URL}emitentes/{emitente_id}")
        response.raise_for_status()
        pedidos = response.json()

        if isinstance(pedidos, list) and len(pedidos) > 0 and isinstance(pedidos[0], dict):
            df = pd.DataFrame(pedidos)
            st.dataframe(df.tail(10), use_container_width=True, hide_index=True)
        else:
            st.error("Sem pedidos gerados no Sistema.")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao carregar pedidos: {e}")

# Verifica se a tela deve ficar bloqueada

def adicionar_pedido(cadastro_id, chave, certificado):
    #st.write("VERSÃO DO STREAMLIT:", st.__version__)

    key_descricao = "descricao_" + str(time.time())
    
    with st.form(key="pedido_form", clear_on_submit=True):

        #############################################
        try:
            response = requests.get(f"{API_URL_PRODUTO}emitentes/{cadastro_id}")
            #response = requests.get(f"{API_URL_PRODUTO}emitentes/{cadastro_id}/{codigo}") # a implantar.
            response.raise_for_status()
            produtos_response = response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao carregar produtos: {e}")
        

        produtos = [(produto["descricao"], produto["id"]) for produto in produtos_response]
        

# Exibindo a estrutura final
        print(produtos)
        print(produtos_response)



            
        # Definir o produto padrão pela descrição
        default_produtos = 'MARMITEX - COMIDA CASEIRA UNIDADE'

        # Selecionar o produto usando a descrição, ao invés de tentar acessar o código
        # produtos_nome = st.selectbox(
        #     "Descrição do Pedido:",
        #     [nome for nome, codigo in produtos],  # Mostra apenas o nome
        #     index=[i for i, v in enumerate(produtos) if v[0] == default_produtos][0]  # Definindo o índice corretamente
        # )
        # produtos_nome = st.selectbox(
        #     "Descrição do Pedido:",
        #     [nome for nome, _ in produtos]  # Mostra apenas a descrição dos produtos
        # )
        produtos_nome = st.selectbox(
            "Descrição do Pedido:",
            [nome for nome, _ in sorted(produtos, key=lambda x: x[1])]  # Ordena por ID (código)
        )

        # Obter o código do produto selecionado
        #produto_codigo = next(codigo for nome, codigo in produtos if nome == produtos_nome)
        produto_id = next(codigo for nome, codigo in produtos if nome == produtos_nome)
        print('PRDUTO__________________________ID',produto_id)
        produto_selecionado = next(
           (produto for produto in produtos_response if produto["id"] == produto_id),
            None  # Se não encontrar, retorna None
            )
        if produto_selecionado:
            print("Produto completo selecionado:", produto_selecionado)
        else:
            print("Produto não encontrado.")

        #st.write("Produto selecionado:", produtos_nome)
        #st.write("Código do produto selecionado:", produto_codigo)
        #default_produtos = "1"
       
        #st.write(f"Forma de pagamento selecionada: {forma_pagamento_nome} (Código: {forma_pagamento_codigo})")
        # for produto in produtos_response:
        #     descricao = produto.get("descricao")
        #     print(descricao) 
        #produtos = []

        # for produto in produtos_response:
        #     descricao = produto.get("descricao", "Sem descrição")
        #     produtos.append(descricao)
  
        #########################################################


        quantidade = st.number_input("Quantidade:", min_value=0.0, format="%.2f")
        
        if quantidade:
            try:
                quantidade = float(quantidade)  # Tenta converter para float
            except ValueError:
                st.error("Por favor, insira um número válido.")
                quantidade = None  # Evita processamento se a conversão falhar
                
        #status = st.selectbox("Status:", ["pendente", "concluído", "cancelado"])

        # Criar o carrinho na sessão, se não existir
        if "carrinho" not in st.session_state:
            st.session_state.carrinho = []

        # Botão para adicionar o produto ao carrinho
        if st.form_submit_button("Adicionar produto ao carrinho"):
            if not produtos_nome or quantidade is None or quantidade <= 0:
                st.warning("Descrição e quantidade válidos são obrigatórios!")
            else:
                item =produto_selecionado.copy()
                if item["unidade_comercial"] == "KG":
                    if "quantidade" in item:
                        print(type(item["quantidade"]))
                    else:
                        print("Chave 'quantidade' ainda não foi definida.")
                    print("unidade_comercial_______________________________KG")
                    print(quantidade)
                    #type(item["quantidade"])
                    item["quantidade"] = float(quantidade) 
                    print(quantidade)
                    print("TIPAGEMM___________________", type(quantidade))
                elif item["unidade_comercial"] == "UN":
                    if "quantidade" in item:
                        print(type(item["quantidade"]))
                    else:
                        print("Chave 'quantidade' ainda não foi definida.")
                    print("unidade_comercial_______________________________UN")
                    print(quantidade)
                    print("TIPAGEMM___________________", type(quantidade))
                    if isinstance(quantidade, float) and not quantidade.is_integer():
                        st.error("Este produto é vendido por unidade e não pode ter quantidade fracionada.")
                        time.sleep(2)
                        st.rerun() 
                        return  # Interrompe a execução da função atual
                    item["quantidade"] = int(quantidade)
                    print(item["quantidade"])
                st.session_state.carrinho.append(item)
                print("PRODUTOS NO CARRINHO__________________",st.session_state.carrinho)
                #st.success("Produto adicionado ao carrinho!")


        # Exibir o carrinho atual
        if st.session_state.carrinho:
            st.write("### Carrinho de Produtos:")
            df_carrinho = pd.DataFrame(st.session_state.carrinho)
            st.dataframe(df_carrinho, use_container_width=True, hide_index=True)

            # Checkbox para excluir produtos
            indices_remover = st.multiselect("Selecione produtos para remover:", df_carrinho.index)
            if st.form_submit_button("Remover Selecionados"):
                for idx in sorted(indices_remover, reverse=True):
                    st.session_state.carrinho.pop(idx)

                print("PRODUTOS NO CARRINHO__________________",st.session_state.carrinho)    
                st.success("Produtos removidos!")
                st.rerun()  # Atualiza a página

      
        status = "Concluído"
        valor_total = 0
        #valor_total = sum(item['quantidade'] * item['preco_unitario'] for item in carrinho)
        print('________________TIPO VAR',type(valor_total))
        print(valor_total)
        emitente_id = cadastro_id

        default_status = st.session_state.get("CPF", "Não")  # Se None, assume False
        #st.session_state["status"] = st.selectbox("CPF na nota:", ["Sim", "Não"], index=[True, False].index(default_status))
        cpf_na_nota = st.selectbox("CPF na nota:", ["Sim", "Não"], index=["Sim", "Não"].index(default_status))
        cpf = st.text_input("Número de CPF:", max_chars=11,value=st.session_state.get("cpf", ""))
        cpf_valido = cpf.isdigit() and len(cpf) == 11
        # if not cpf:
        #     st.warning("Digite o CPF.")
        # elif not cpf.isdigit():
        #     st.error("O CPF deve conter apenas números.")
        # elif len(cpf) != 11:
        #     st.error("O CPF deve conter exatamente 11 dígitos.")
        # else:
        #     #st.success("CPF válido!")
        #     st.session_state["cpf"] = cpf  # Atualiza session_state
        formas_pagamento = [
            ("Dinheiro", "1"),
            ("Cheque", "2"),
            ("Cartão de Crédito", "3"),
            ("Cartão de Débito", "4"),
            ("Crédito Loja", "5"),
            ("Vale Alimentação", "10"),
            ("Vale Refeição", "11"),
            ("Vale Presente", "12"),
            ("Vale Combustível", "13"),
            ("Boleto Bancário", "14"),
            ("Depósito Bancário", "15"),
            ("Outros", "90")
             ]
        default_forma_pagamento = "1"
        forma_pagamento_nome = st.selectbox(
            "Forma de Pagamento:", 
            [nome for nome, codigo in formas_pagamento],  # Mostra apenas o nome
            index=[i for i, v in enumerate(formas_pagamento) if v[1] == default_forma_pagamento][0]
                )
        forma_pagamento_codigo = next(codigo for nome, codigo in formas_pagamento if nome == forma_pagamento_nome)
        #st.write(f"Forma de pagamento selecionada: {forma_pagamento_nome} (Código: {forma_pagamento_codigo})")
        st.session_state["CPF"] = cpf_na_nota
        #descricao = st.text_input("Descrição do Pedido:")


        ############################################################################

        
        ########################################################################
        if st.form_submit_button("Adicionar Pedido"):
            
            if cpf_na_nota == "Sim":
                cpf_valido = cpf.isdigit() and len(cpf) == 11
                if not cpf:
                    st.warning("Digite o CPF.")
                    time.sleep(1)
                    return
                elif not cpf.isdigit():
                    st.error("O CPF deve conter apenas números.")
                    time.sleep(1)
                    return
                elif len(cpf) != 11:
                    st.error("O CPF deve conter exatamente 11 dígitos.")
                    time.sleep(1)
                    return
                else:
                    #st.success("CPF válido!")
                    st.session_state["cpf"] = cpf  # Atualiza session_state

            carrinho = st.session_state.get("carrinho", [])  # <-- ESTA LINHA FALTANDO

            valor_total = sum(item['quantidade'] * item['preco_unitario'] for item in carrinho)

            for item in carrinho:
                nome = item['descricao']
                quantidade = item['quantidade']
                preco_unitario = item['preco_unitario']
                subtotal = quantidade * preco_unitario
                st.write(f"- **{nome}** | Quantidade: {quantidade} | Preço unitário: {preco_unitario:.2f} | Subtotal: {subtotal:.2f}")
            st.session_state["confirmar_pedido"] = True
            st.write("### Resumo do Pedido")
            st.write(f"**Total de itens:** {len(carrinho)}")
            st.write(f"**Valor total:** R$ {valor_total:.2f}")
            st.write(f"**Forma de pagamento:** {forma_pagamento_nome}")
            st.write(f"**CPF na nota:** {cpf_na_nota}")
            if cpf_na_nota == "Sim":
                st.write(f"**CPF:** {cpf}")



    if st.session_state.get("confirmar_pedido"):
        placeholder = st.empty()
        with placeholder.container():
            st.warning("Tem certeza que deseja adicionar este pedido?")
            col1, col2 = st.columns(2)

            with col1:
                if st.button("✅ Confirmar Pedido"):
                    carrinho = st.session_state.carrinho
                    if not carrinho:
                        st.warning("Carrinho sem itens adicionados!")
                        st.session_state["confirmar_pedido"] = False
                        time.sleep(2)
                        #placeholder.empty()
                        st.rerun()
                        #st.session_state["cpf"] = ""
                        return

                    with st.spinner("Adicionando pedido..."):
                        try:
                            response_emitente = requests.get(f"{API_URL_EMITENTE}{cadastro_id}")
                            response_emitente.raise_for_status()

                            valor_total = 0  # Você pode recalcular aqui se quiser

                            resposta = None
                            if cpf_na_nota == "Sim" and carrinho:
                                resposta = call_pedido(
                                    chave, certificado, response_emitente, quantidade,
                                    valor_total, forma_pagamento_codigo, cpf,
                                    produtos_nome, produto_selecionado, carrinho
                                )
                            elif carrinho:
                                resposta = call_pedido_sem_cpf(
                                    chave, certificado, response_emitente, quantidade,
                                    valor_total, forma_pagamento_codigo,
                                    produtos_nome, produto_selecionado, carrinho
                                )

                            if resposta and resposta.get("status") == "sucesso":
                                data = {
                                    "descricao": carrinho[0]["descricao"],
                                    "status": "Concluído",
                                    "valor_total": valor_total,
                                    "emitente_id": cadastro_id,
                                    "quantidade": quantidade,
                                    "chave_acesso": resposta["chave_acesso"],
                                    "protocolo": resposta["n_prot"],
                                    "data_recebimento": resposta["data_recebimento"],
                                    "motivo": resposta["x_motivo"],
                                    "status_sefaz": resposta["Status_sefaz"]
                                }
                                requests.post(API_URL, json=data)
                                print('RESPOSTA______________NOTA_____',resposta)
                                novo_id_nota = {"id_nota": response_emitente.json().get("id_nota") + 1}
                                requests.patch(f"{API_URL_EMITENTE}{cadastro_id}", json=novo_id_nota)

                                st.success("Pedido adicionado com sucesso!")

                                st.session_state.carrinho = []
                                st.session_state["cpf"] = ""

                            else:
                                st.error("Ocorreu um erro na autorização!")

                        except requests.exceptions.RequestException as e:
                            st.error(f"Erro ao adicionar pedido: {e}")

                        st.session_state["confirmar_pedido"] = False
                        #placeholder.empty()
                        time.sleep(1)
                        st.rerun()

            with col2:
                if st.button("❌ Cancelar"):
                    st.session_state["confirmar_pedido"] = False
                    st.rerun()
                    #placeholder.empty()
                    st.session_state["cpf"] = ""