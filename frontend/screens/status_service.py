import streamlit as st
import subprocess


def status_service():




    if st.button("Verificar Status"):
        st.write("Verificando status do serviço...")

        with st.spinner("Processando..."):
            process = subprocess.Popen(
                ["python", "/workspaces/sat_system/frontend/components/teste_requisicao.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            output, error = process.communicate()

        st.write("Status:")
        st.code(output)

        if error:
            st.write("Status Erros:")
            st.code(error)
