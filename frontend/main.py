import sys
import os


# não apagar o cabeçalho em prod pois aqui inicializa o dir em prod
#sys.path.append('/mount/src/sat_system')

#sys.path.append(os.path.join(os.path.dirname(__file__), 'frontend'))

sys.path.append('/app')



from frontend.components.auth import autenticar  # Importa a autenticação
from frontend.screens.pedidos import exibir_pedidos, adicionar_pedido
#from frontend.screens.cadastros import exibir_cadastro, criar_cadastro, atualizar_cadastro
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
    cnpj, authenticated, emitente_id, licenca, certificado, chave = autenticar()  # Obtém os dados da autenticação
    print("SENHA__MAIN", chave)

    #st.write(f"Authenticated: {authenticated}, CNPJ: {cnpj}, Cadastro ID: {cadastro_id}")

    if authenticated and cnpj == "admin":
        #st.sidebar.write("Debug Session State:", st.session_state)
        #st.sidebar.write(f"Bem-vindo, {cadastro_id}!")
        st.sidebar.markdown(f"Bem-vindo, **{cnpj}** sua licença em uso é **{licenca}**!")
        #st.sidebar.markdown(f"Bem-vindo, **{cadastro_id}**!")
        menu = ["Home", "Pedidos", "Pagamentos", "Cadastro", "Status Serviço", "Emitente"]
        escolha = st.sidebar.selectbox("Escolha a Tela", menu)

        if escolha == "Home":
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Sistema Autenticador e Transmissor de Cupons Fiscais Eletrônicos"
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
            adicionar_pedido(emitente_id)
        elif escolha == "Pagamentos":
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Tela de Pagamento (em construção)"
                "</div>",
                unsafe_allow_html=True
            )
            #st.subheader("Tela de Pagamento (em construção)")
        elif escolha == "Cadastro":
            #st.subheader("Visualizar Cadastro")
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Visualizar Cadastro"
                "</div>",
                unsafe_allow_html=True
            )
            exibir_cadastro()
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Atualizar Cadastro"
                "</div>",
                unsafe_allow_html=True
            )
            #st.subheader("Atualizar Cadastro")
            atualizar_cadastro()
            #st.subheader("Criar Cadastro")
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Criar Cadastro"
                "</div>",
                unsafe_allow_html=True
            )
            criar_cadastro()
        elif escolha == "Status Serviço":
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Verificar Status do Serviço"
                "</div>",
                unsafe_allow_html=True
            )
            #status_service()
            status_service(chave, certificado)
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
        menu = ["Home", "Pedidos", "Pagamentos", "Status Serviço"]
        escolha = st.sidebar.selectbox("Escolha a Tela", menu)

        if escolha == "Home":
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Sistema Autenticador e Transmissor de Cupons Fiscais Eletrônicos"
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
            adicionar_pedido(emitente_id)
        elif escolha == "Pagamentos":
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Tela de Pagamento (em construção)"
                "</div>",
                unsafe_allow_html=True
            )
            #st.subheader("Tela de Pagamento (em construção)")
        elif escolha == "Status Serviço":
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Verificar Status do Serviço"
                "</div>",
                unsafe_allow_html=True
            )
            status_service(chave, certificado)
           
        
        if st.sidebar.button("Logout"):
            del st.session_state["authenticated"]
            del st.session_state["cnpj"]
            st.rerun()


    else:
        st.warning("Por favor, faça login para acessar o sistema.")


if __name__ == "__main__":
    main()