import streamlit as st
from frontend.components.auth import autenticar  # Importa a autenticação
from frontend.screens.pedidos import exibir_pedidos, adicionar_pedido

def main():
    name, authenticated = autenticar()  # Obtém os dados da autenticação

    if authenticated and name == "admin":
        st.sidebar.write(f"Bem-vindo, {name}!")

        menu = ["Home", "Pedidos", "Pagamentos", "Cadastro"]
        escolha = st.sidebar.selectbox("Escolha a Tela", menu)

        if escolha == "Home":
            st.subheader("Sistema Autenticador e Transmissor de Cupons Fiscais Eletrônicos")
        elif escolha == "Pedidos":
            st.subheader("Tela de Pedidos")
            exibir_pedidos()
            adicionar_pedido()
        elif escolha == "Pagamentos":
            st.subheader("Tela de Pagamento (em construção)")
        elif escolha == "Cadastro":
            st.subheader("Tela de Cadastro (em construção)")

        # Lógica de logout
        if st.sidebar.button("Logout"):
            del st.session_state["authenticated"]
            del st.session_state["username"]
            st.rerun()

    elif authenticated:
        menu = ["Home", "Pedidos", "Pagamentos"]
        escolha = st.sidebar.selectbox("Escolha a Tela", menu)

        if escolha == "Home":
            st.subheader("Sistema Autenticador e Transmissor de Cupons Fiscais Eletrônicos")
        elif escolha == "Pedidos":
            st.subheader("Tela de Pedidos")
            exibir_pedidos()
            adicionar_pedido()
        elif escolha == "Pagamentos":
            st.subheader("Tela de Pagamento (em construção)")
        
        if st.sidebar.button("Logout"):
            del st.session_state["authenticated"]
            del st.session_state["username"]
            st.rerun()


    else:
        st.warning("Por favor, faça login para acessar o sistema.")

if __name__ == "__main__":
    main()
