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
    key_descricao = "descricao_" + str(time.time())
    
    with st.form(key="pedido_form", clear_on_submit=True):
        default_status = st.session_state.get("CPF", "Não")  # Se None, assume False
        #st.session_state["status"] = st.selectbox("CPF na nota:", ["Sim", "Não"], index=[True, False].index(default_status))
        cpf_na_nota = st.selectbox("CPF na nota:", ["Sim", "Não"], index=["Sim", "Não"].index(default_status))
        formas_pagamento = [
            ("Dinheiro", "01"),
            ("Cheque", "02"),
            ("Cartão de Crédito", "03"),
            ("Cartão de Débito", "04"),
            ("Crédito Loja", "05"),
            ("Vale Alimentação", "10"),
            ("Vale Refeição", "11"),
            ("Vale Presente", "12"),
            ("Vale Combustível", "13"),
            ("Boleto Bancário", "14"),
            ("Depósito Bancário", "15"),
            ("Outros", "90")
             ]
        default_forma_pagamento = "01"
        forma_pagamento_nome = st.selectbox(
            "Forma de Pagamento:", 
            [nome for nome, codigo in formas_pagamento],  # Mostra apenas o nome
            index=[i for i, v in enumerate(formas_pagamento) if v[1] == default_forma_pagamento][0]
                )
        forma_pagamento_codigo = next(codigo for nome, codigo in formas_pagamento if nome == forma_pagamento_nome)
        st.write(f"Forma de pagamento selecionada: {forma_pagamento_nome} (Código: {forma_pagamento_codigo})")
        st.session_state["CPF"] = cpf_na_nota
        descricao = st.text_input("Descrição do Pedido:")
        quantidade = st.number_input("Quantidade:", min_value=0.0, format="%.2f")
        
        if quantidade:
            try:
                quantidade = float(quantidade)  # Tenta converter para float
            except ValueError:
                st.error("Por favor, insira um número válido.")
                quantidade = None  # Evita processamento se a conversão falhar
                
        status = st.selectbox("Status:", ["pendente", "concluído", "cancelado"])
        valor_total = st.number_input("Valor Total:", min_value=0.0, format="%.2f")
        print('________________TIPO VAR',type(valor_total))
        print(valor_total)
        emitente_id = cadastro_id
        
        
      
        if st.form_submit_button("Adicionar Pedido"):
            if not descricao or valor_total is None or quantidade is None or valor_total <= 0 or quantidade <= 0:
                st.warning("Descrição, valor total e quantidade são obrigatórios e precisam ser maiores que 0!")
                return
                
            #data = {"descricao": descricao, "status": status, "valor_total": valor_total, "emitente_id": emitente_id, "quantidade": quantidade}

            with st.spinner("Adicionando pedido..."):
                try:
                    response_emitente =  response = requests.get(f"{API_URL_EMITENTE}{cadastro_id}")
                    response_emitente.raise_for_status()
                    #emitentes = response_emitente.json()
                    #print("Response JSON:", response_emitente.json())
                    #response = requests.post(API_URL, json=data)
                    response.raise_for_status()
                    print('PRITN TESTEEEE')
                    # chamada NFAUT (emitente, cliente)
                    if cpf_na_nota == "Sim":
                        st.write("O pedido terá CPF na nota.")
                        resposta = call_pedido(chave, certificado, response_emitente, quantidade, valor_total)

                    else:
                        resposta = call_pedido_sem_cpf(chave, certificado, response_emitente, quantidade, valor_total)
                        st.write("O pedido NÃO terá CPF na nota.")   

                    #call_pedido_sem_cpf(chave, certificado)
                    #data = {"descricao": descricao, "status": status, "valor_total": valor_total, "emitente_id": emitente_id, "quantidade": quantidade}
                    if resposta["status"] == "sucesso":
                        data = {"descricao": descricao, "status": status, "valor_total": valor_total, "emitente_id": emitente_id, "quantidade": quantidade, "chave_acesso": resposta["chave_acesso"], "protocolo": resposta["n_prot"], "data_recebimento": resposta["data_recebimento"],"motivo":resposta["x_motivo"], "status_sefaz": resposta["Status_sefaz"]}
                        print('_________________Json_______________PEDIDOS_____________INSERT____________',data)
                        response = requests.post(API_URL, json=data)
                        print('RESPOSTA______________NOTA_____',resposta)
                        print("Nota autorizada com sucesso!")
                        data_id_nota = {"id_nota": response_emitente.json().get("id_nota") + 1}
                        print('________________PRINT_id_nota',data_id_nota)
                        response_emitente = requests.patch(f"{API_URL_EMITENTE}{cadastro_id}", json=data_id_nota)
                        response.raise_for_status()
                    else:
                        print(f"Ocorreu um erro na autorização: resposta")
                        #print(resposta["xml_enviado"])
                    #response_emitente = requests.post(API_URL, json=data_id_nota)
                    #reponse_id_nota = requests.post(API_URL, json=data_id_nota)
                    st.success("Pedido Adicionado com Sucesso!")
                    
                    time.sleep(1)
                    st.rerun()  # Atualiza a página automaticamente
                except requests.exceptions.RequestException as e:
                    st.error(f"Erro ao adicionar pedido: {e}")