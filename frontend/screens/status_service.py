import streamlit as st
import subprocess
import os
#from frontend.components.status_servico import call_cadastro
from frontend.components.NFeStatusServico4 import call_cadastro


def status_service(chave, certificado, env):
    print("PRINT_STATUS_SERVICE",certificado, chave, env)
    #call_cadastro(certificado)
    with st.form(key="status_service_view_form"):
        submitted = st.form_submit_button("Verificar Status")

    if submitted:
        st.write("Verificando status do serviço...")

        with st.spinner("Processando..."):
            output, error = call_cadastro(chave, certificado, env)  # Chama a função diretamente

        st.write("Status:")
        st.code(output, error)

        if error:
            st.write("Status:")
            st.code(error)

# Para rodar no Streamlit, chame `status_service()` dentro de um script Streamlit
