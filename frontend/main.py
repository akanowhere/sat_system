import sys
import os


# não apagar o cabeçalho em prod pois aqui inicializa o dir em prod
#sys.path.append('/mount/src/sat_system')

#sys.path.append(os.path.join(os.path.dirname(__file__), 'frontend'))

sys.path.append('/app')



from frontend.components.auth import autenticar  # Importa a autenticação
from frontend.screens.pedidos import exibir_pedidos, adicionar_pedido
from frontend.screens.cadastros import exibir_cadastro, criar_cadastro, atualizar_cadastro



#sys.path.append('/mount/src/sat_system/frontend')

# Adicionando o diretório raiz do projeto ao sys.path
#sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'frontend'))

# Verifique o sys.path
#print("sys.path:", sys.path)

# Código CSS para esconder o ícone do GitHub

# hide_github_icon = """
# <style>
# /* Esconder o link do GitHub */
# .css-1jc7ptx, 
# .e1ewe7hr3, 
# .viewerBadge_container__1QSob, 
# .styles_viewerBadge__1yB5_, 
# .viewerBadge_link__1S137, 
# .viewerBadge_text__1JaDK { 
#     display: none; 
# }

# /* Esconder menu principal, rodapé e cabeçalho */
# #MainMenu { visibility: hidden; }
# footer { visibility: hidden; }
# header { visibility: hidden; }

# /* Esconder o avatar do criador do app */
# img[src*="avatars.githubusercontent.com"] {
#     display: none !important;
# }

# /* Esconder o link do perfil */
# a[href*="share.streamlit.io/user/"] {
#     display: none !important;
# }
# </style>

# <script>
# setTimeout(function() {
#     let avatar = document.querySelector('img[data-testid="appCreatorAvatar"]');
#     if (avatar) avatar.style.display = 'none';

#     let profileLink = document.querySelector('a[href*="share.streamlit.io/user/"]');
#     if (profileLink) profileLink.style.display = 'none';
# }, 3000); // Aguarda 3 segundos
# </script>
# """

import streamlit as st

# Aplicar o CSS no Streamlit
#st.markdown(hide_github_icon, unsafe_allow_html=True)




st.set_page_config(page_title="Main age", page_icon="📝", layout="centered")


def main():
    #name, authenticated = autenticar()  # Obtém os dados da autenticação
    cnpj, authenticated, cadastro_id = autenticar()  # Obtém os dados da autenticação

    #st.write(f"Authenticated: {authenticated}, CNPJ: {cnpj}, Cadastro ID: {cadastro_id}")

    if authenticated and cnpj == "admin":
        #st.sidebar.write("Debug Session State:", st.session_state)
        #st.sidebar.write(f"Bem-vindo, {cadastro_id}!")
        st.sidebar.markdown(f"Bem-vindo, **{cnpj}**!")
        #st.sidebar.markdown(f"Bem-vindo, **{status}**!")
        menu = ["Home", "Pedidos", "Pagamentos", "Cadastro"]
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
            exibir_pedidos(cadastro_id)
            adicionar_pedido(cadastro_id)
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
            

        # Lógica de logout
        if st.sidebar.button("Logout"):
            del st.session_state["authenticated"]
            del st.session_state["cnpj"]
            st.rerun()

    elif authenticated:
        #st.sidebar.write(f"Bem-vindo, {cnpj}!")
        st.sidebar.markdown(f"Bem-vindo, **{cnpj}**!")
        menu = ["Home", "Pedidos", "Pagamentos"]
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
            exibir_pedidos(cadastro_id)
            adicionar_pedido(cadastro_id)
        elif escolha == "Pagamentos":
            st.markdown(
                "<div style='text-align: center; font-size: 30px; font-weight: bold; color: black;'>"
                "Tela de Pagamento (em construção)"
                "</div>",
                unsafe_allow_html=True
            )
            #st.subheader("Tela de Pagamento (em construção)")
        
        if st.sidebar.button("Logout"):
            del st.session_state["authenticated"]
            del st.session_state["cnpj"]
            st.rerun()


    else:
        st.warning("Por favor, faça login para acessar o sistema.")


if __name__ == "__main__":
    main()