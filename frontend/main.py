import sys
import os


# não apagar o cabeçalho em prod pois aqui inicializa o dir em prod
#sys.path.append('/mount/src/sat_system')

#sys.path.append(os.path.join(os.path.dirname(__file__), 'frontend'))

sys.path.append('/app')



from frontend.components.auth import autenticar  # Importa a autenticação
from frontend.screens.pedidos import exibir_pedidos, adicionar_pedido
from frontend.screens.produtos import exibir_produtos, atualizar_produtos, criar_produto, exibir_produtos_admin, atualizar_produtos_admin
from frontend.screens.status_service import status_service
from frontend.screens.emitentes import exibir_emitente, criar_emitente, atualizar_emitente
import streamlit as st

# Aplicar o CSS no Streamlit

hide_github_icon = """
<style>
/* Esconder o link do GitHub */
.css-1jc7ptx, 
.e1ewe7hr3, 
.viewerBadge_container__1QSob, 
.styles_viewerBadge__1yB5_, 
.viewerBadge_link__1S137, 
.viewerBadge_text__1JaDK { 
    display: none; 
}

/* Esconder menu principal, rodapé e cabeçalho */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

 </style>"""

st.set_page_config(page_title="Pedidos NFC-e", page_icon="📝", layout="centered")
st.markdown(hide_github_icon, unsafe_allow_html=True)



def main():
    #name, authenticated = autenticar()  # Obtém os dados da autenticação
    cnpj, authenticated, emitente_id, licenca, certificado, chave, env = autenticar()  # Obtém os dados da autenticação
    print("SENHA__MAIN", cnpj, authenticated, emitente_id, licenca, certificado, chave, env)
    
    #print("Response na função MAIN:", response.json() if response else "Nenhuma resposta")  # Verificando a resposta
    

    #st.write(f"Authenticated: {authenticated}, CNPJ: {cnpj}, Cadastro ID: {cadastro_id}")

    if authenticated and cnpj == "admin":
        print("CHAVE_ENV",cnpj, authenticated, emitente_id, licenca, certificado, chave, env)
        #st.sidebar.write("Debug Session State:", st.session_state)
        #st.sidebar.write(f"Bem-vindo, {cadastro_id}!")
        st.sidebar.markdown(f"Bem-vindo, **{cnpj}** sua licença em uso é **{licenca}**!")
        #st.sidebar.markdown(f"Bem-vindo, **{cadastro_id}**!")
        menu = ["Home", "Pedidos", "Pagamentos", "Produtos", "Status Serviço", "Emitente"]
        escolha = st.sidebar.selectbox("Escolha a Tela", menu)

        if escolha == "Pedidos":
            if "pedidos_reset" not in st.session_state:
                st.session_state["pedidos_reset"] = True  # Inicializa como True na primeira vez
            
            # Se for a primeira vez na tela "Pedidos", reinicia os componentes
            if st.session_state["pedidos_reset"]:
                # Realiza o reset de informações da tela de Pedidos
                st.session_state["pedidos_reset"] = False  # Marca como False após o primeiro reset
                # Resetar ou redefinir qualquer dado ou visualização da tela "Pedidos" aqui
                st.session_state.carrinho = []
                st.rerun()



        # Página Home
        if escolha == "Home":
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Sistema Autenticador e Transmissor de Cupons Fiscais Eletrônicos"
                "</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<div style='text-align: center; font-size: 18px; color: black; margin-top: 20px;'>"
                "Imprima ou transforme em PDF suas NF's no link abaixo:<br>"
                "<a href='https://www.homologacao.nfce.fazenda.sp.gov.br/NFCeConsultaPublica/Paginas/ConsultaPublica.aspx' "
                "target='_blank' style='color: #1a73e8; text-decoration: none;'>"
                "https://www.homologacao.nfce.fazenda.sp.gov.br/NFCeConsultaPublica/Paginas/ConsultaPublica.aspx"
                "</a>"
                "</div>",
                unsafe_allow_html=True
            )
            #st.subheader("Sistema Autenticador e Transmissor de Cupons Fiscais Eletrônicos")
        elif escolha == "Pedidos":
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Pedidos"
                "</div>",
                unsafe_allow_html=True
            )
            #st.subheader("Tela de Pedidos")
            exibir_pedidos(emitente_id)
            adicionar_pedido(emitente_id, chave, certificado)
        elif escolha == "Pagamentos":
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Tela de Pagamento (em construção)"
                "</div>",
                unsafe_allow_html=True
            )
            #st.subheader("Tela de Pagamento (em construção)")
        elif escolha == "Produtos":
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Produtos"
                "</div>",
                unsafe_allow_html=True
            )
            #st.subheader("Tela de Pedidos")
            #exibir_produtos(emitente_id)
            exibir_produtos_admin()
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Atualizar Produtos"
                "</div>",
                unsafe_allow_html=True
            )
            #st.subheader("Atualizar Emitente")
            atualizar_produtos(emitente_id)
            #atualizar_produtos_admin()
            #adicionar_pedido(emitente_id, chave, certificado)
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Criar Produto"
                "</div>",
                unsafe_allow_html=True
            )
            criar_produto()
        elif escolha == "Status Serviço":
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Verificar Status do Serviço"
                "</div>",
                unsafe_allow_html=True
            )
            #status_service()
            status_service(chave, certificado, env)
        elif escolha == "Emitente":
            #st.subheader("Visualizar Emitente")
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Visualizar Emitente"
                "</div>",
                unsafe_allow_html=True
            )
            exibir_emitente()
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Atualizar Emitente"
                "</div>",
                unsafe_allow_html=True
            )
            #st.subheader("Atualizar Emitente")
            atualizar_emitente()
            #st.subheader("Criar Emitente")
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Criar Emitente"
                "</div>",
                unsafe_allow_html=True
            )
            criar_emitente()


        # Lógica de logout
        if st.sidebar.button("Logout"):
            del st.session_state["authenticated"]
            del st.session_state["cnpj"]
            st.rerun()



    elif authenticated:
        #st.sidebar.write(f"Bem-vindo, {cnpj}!")
        #st.sidebar.markdown(f"Bem-vindo, **{cnpj}**!")
        st.sidebar.markdown(f"Bem-vindo, **{cnpj}** sua licença em uso é **{licenca}**!")
        menu = ["Home", "Pedidos", "Pagamentos", "Produtos", "Status Serviço"]
        escolha = st.sidebar.selectbox("Escolha a Tela", menu)

        if "ultima_tela" not in st.session_state:
            st.session_state.ultima_tela = escolha

        # Detectar troca de tela e resetar carrinho ao sair de "Pedidos"
        if st.session_state.ultima_tela != escolha:
            if st.session_state.ultima_tela == "Pedidos":
                st.session_state.carrinho = []  # ou .clear(), se já existir
            st.session_state.ultima_tela = escolha


        if escolha == "Pedidos":
            if "pedidos_reset" not in st.session_state:
                st.session_state["pedidos_reset"] = True  # Inicializa como True na primeira vez
            
            # Se for a primeira vez na tela "Pedidos", reinicia os componentes
            if st.session_state["pedidos_reset"]:
                # Realiza o reset de informações da tela de Pedidos
                st.session_state["pedidos_reset"] = False  # Marca como False após o primeiro reset
                # Resetar ou redefinir qualquer dado ou visualização da tela "Pedidos" aqui
                st.rerun()


        if escolha == "Home":
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Sistema Autenticador e Transmissor de Cupons Fiscais Eletrônicos"
                "</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<div style='text-align: center; font-size: 18px; color: black; margin-top: 20px;'>"
                "Imprima ou transforme em PDF suas NF´s no link abaixo:<br>"
                "<a href='https://www.nfce.fazenda.sp.gov.br/NFCeConsultaPublica/Paginas/ConsultaPublica.aspx' "
                "target='_blank' style='color: #1a73e8; text-decoration: none;'>"
                "https://www.nfce.fazenda.sp.gov.br/NFCeConsultaPublica/Paginas/ConsultaPublica.aspx"
                "</a>"
                "</div>",
                unsafe_allow_html=True
            )
            #st.subheader("Sistema Autenticador e Transmissor de Cupons Fiscais Eletrônicos")
        elif escolha == "Pedidos":
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Pedidos"
                "</div>",
                unsafe_allow_html=True
            )
            #st.subheader("Tela de Pedidos")
            exibir_pedidos(emitente_id)
            adicionar_pedido(emitente_id, chave, certificado)
        elif escolha == "Pagamentos":
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Tela de Pagamento (em construção)"
                "</div>",
                unsafe_allow_html=True
            )
            #st.subheader("Tela de Pagamento (em construção)")
        elif escolha == "Produtos":
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Produtos"
                "</div>",
                unsafe_allow_html=True
            )
            #st.subheader("Tela de Pedidos")
            exibir_produtos(emitente_id)
            #adicionar_pedido(emitente_id, chave, certificado)
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Atualizar Produtos"
                "</div>",
                unsafe_allow_html=True
            )
            #st.subheader("Atualizar Emitente")
            atualizar_produtos(emitente_id)
            #adicionar_pedido(emitente_id, chave, certificado)
        elif escolha == "Status Serviço":
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Verificar Status do Serviço"
                "</div>",
                unsafe_allow_html=True
            )
            status_service(chave, certificado, env)
           
        
        if st.sidebar.button("Logout"):
            del st.session_state["authenticated"]
            del st.session_state["cnpj"]
            st.rerun()


    else:
        st.warning("Por favor, faça login para acessar o sistema.")


if __name__ == "__main__":
    main()