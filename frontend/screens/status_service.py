import streamlit as st
import subprocess
import os
#from frontend.components.status_servico import call_cadastro
from frontend.components.NFeStatusServico4 import call_cadastro


def status_service(certificado, chave):
    with st.form(key="status_service_view_form"):
        submitted = st.form_submit_button("Verificar Status")

    if submitted:
        st.write("Verificando status do serviço...")

        with st.spinner("Processando..."):
            output, error = call_cadastro(certificado, chave)  # Chama a função diretamente

        st.write("Status:")
        st.code(output, error)

        if error:
            st.write("Status:")
            st.code(error)

# Para rodar no Streamlit, chame `status_service()` dentro de um script Streamlit
