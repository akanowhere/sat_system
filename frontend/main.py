import sys
import os


sys.path.append('/mount/src/sat_system')

#print("sys.path:", sys.path)



import streamlit as st
from frontend.screens.pedidos import exibir_pedidos, adicionar_pedido

def main():
    st.title("Sistema de Pedidos SAT")

    menu = ["Home", "Pedidos", "Pagamentos"]
    escolha = st.sidebar.selectbox("Escolha a Tela", menu)

    if escolha == "Home":
        st.subheader("Sistema Autenticador e Transmissor de Cupons Fiscais Eletrônicos")
    elif escolha == "Pedidos":
        exibir_pedidos()
        adicionar_pedido()
    elif escolha == "Pagamentos":
        st.subheader("Tela de Pagamento (em construção)")

if __name__ == "__main__":
    main()
