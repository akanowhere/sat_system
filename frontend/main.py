import sys
import os


# não apagar o cabeçalho em prod pois aqui inicializa o dir em prod
sys.path.append('/mount/src/sat_system')


import streamlit as st
from frontend.components.auth import autenticar  # Importa a autenticação
from frontend.screens.pedidos import exibir_pedidos, adicionar_pedido
from frontend.screens.cadastros import exibir_cadastro, criar_cadastro



#sys.path.append('/mount/src/sat_system/frontend')

# Adicionando o diretório raiz do projeto ao sys.path
#sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'frontend'))

# Verifique o sys.path
#print("sys.path:", sys.path)

# Código CSS para esconder o ícone do GitHub

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
</style>
"""

# Aplicar o CSS no Streamlit
st.markdown(hide_github_icon, unsafe_allow_html=True)



def main():
    cnpj, authenticated, cadastro_id  = autenticar()  # Obtém os dados da autenticação

    if authenticated and cnpj == "admin":
        st.sidebar.write(f"Bem-vindo, {cnpj}!")

        menu = ["Home", "Pedidos", "Pagamentos", "Cadastro"]
        escolha = st.sidebar.selectbox("Escolha a Tela", menu)

        if escolha == "Home":
            st.subheader("Sistema Autenticador e Transmissor de Cupons Fiscais Eletrônicos")
        elif escolha == "Pedidos":
            st.subheader("Tela de Pedidos")
            exibir_pedidos(cadastro_id)
            adicionar_pedido(cadastro_id)
        elif escolha == "Pagamentos":
            st.subheader("Tela de Pagamento (em construção)")
        elif escolha == "Cadastro":
            st.subheader("Atualizar Cadastro")
            exibir_cadastro()
            st.subheader("Criar Cadastro")
            criar_cadastro()

        # Lógica de logout
        if st.sidebar.button("Logout"):
            del st.session_state["authenticated"]
            del st.session_state["cnpj"]
            st.rerun()

    elif authenticated:
        st.sidebar.write(f"Bem-vindo, {cnpj}!")
        menu = ["Home", "Pedidos", "Pagamentos"]
        escolha = st.sidebar.selectbox("Escolha a Tela", menu)

        if escolha == "Home":
            st.subheader("Sistema Autenticador e Transmissor de Cupons Fiscais Eletrônicos")
        elif escolha == "Pedidos":
            st.subheader("Tela de Pedidos")
            exibir_pedidos(cadastro_id)
            adicionar_pedido(cadastro_id)
        elif escolha == "Pagamentos":
            st.subheader("Tela de Pagamento (em construção)")
        
        if st.sidebar.button("Logout"):
            del st.session_state["authenticated"]
            del st.session_state["cnpj"]
            st.rerun()


    else:
        st.warning("Por favor, faça login para acessar o sistema.")

if __name__ == "__main__":
    main()
