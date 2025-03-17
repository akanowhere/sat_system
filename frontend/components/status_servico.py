import requests
import tempfile
import os
from contextlib import ExitStack
import re
import requests
import streamlit as st






def call_cadastro(certificado, chave):


    cert_temp_file_path = None
    key_temp_file_path = None


    try:
        if not certificado or not isinstance(certificado, str):
            raise ValueError("A variável 'certificado' está vazia ou não é uma string válida.")

        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as temp_cert_file:
            # Escrever o conteúdo do certificado no arquivo temporário
            temp_cert_file.write(certificado.encode('utf-8'))
            
            # Obter o caminho do arquivo temporário
            cert_temp_file_path = temp_cert_file.name
            
            print(f"Caminho do arquivo temporário: {cert_temp_file_path}")

    except ValueError as ve:
        #print(f"Erro: {ve}")
        st.write(f"Erro: {ve}")

    except Exception as e:
        #print(f"Ocorreu um erro inesperado: {e}")
        st.write(f"Ocorreu um erro inesperado: {e}")




    try:
        if not chave or not isinstance(chave, str):
            raise ValueError("A variável 'chave' está vazia ou não é uma string válida.")

        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_key_file:
            # Escrever o conteúdo da chave no arquivo temporário
            temp_key_file.write(chave)
            
            # Obter o caminho do arquivo temporário
            key_temp_file_path = temp_key_file.name

        print("Chave temporária gerada em:", key_temp_file_path)

    except ValueError as ve:
        #print(f"Erro: {ve}")
        st.write(f"Erro: {ve}")

    except Exception as e:
        #print(f"Ocorreu um erro inesperado: {e}")
        st.write(f"Ocorreu um erro inesperado: {e}")


    # with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_key_file:
    #     # Escrever o conteúdo do certificado no arquivo temporário
    #     temp_key_file.write(chave)
        
    #     # Obter o caminho do arquivo temporário
    #     key_temp_file_path = temp_key_file.name

    # print("Chave temporário gerado em:", key_temp_file_path)




    # URL da SEFAZ para consulta de status da NFC-e
    url = "https://homologacao.nfce.fazenda.sp.gov.br/ws/NFeStatusServico4.asmx"

    # Cabeçalhos da requisição (SOAP 1.2)
    headers = {
        "Content-Type": "application/soap+xml; charset=utf-8",
        "User-Agent": "Mozilla/5.0"
    }

    # Corpo da requisição SOAP (versão 4.00) - Removidos espaços extras
    soap_request = """<?xml version="1.0" encoding="utf-8"?><soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"><soap12:Body><nfeDadosMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/NFeStatusServico4"><consStatServ versao="4.00" xmlns="http://www.portalfiscal.inf.br/nfe"><tpAmb>2</tpAmb><cUF>35</cUF><xServ>STATUS</xServ></consStatServ></nfeDadosMsg></soap12:Body></soap12:Envelope>"""

    # Certificado SSL
    cacert_path = "/etc/ssl/certs"
    os.environ['REQUESTS_CA_BUNDLE'] = cacert_path

    # Fazer a requisição à SEFAZ com o certificado digital
    try:
        response = requests.post(
            url,
            data=soap_request.strip(),  # Remove espaços extras
            headers=headers,
            cert=(cert_temp_file_path, key_temp_file_path), # PEGA DO CORPO DO CODIGO E GERA O ARQUIVO TEMP .PEM FUNCIONA FORA DA FUNÇÃO MAS NÃO FUNCIONA DENTRAO DA FUNÇÂO
            verify=cacert_path,
            timeout=30
        )

        print("Status Code:", response.status_code)
        print("Resposta da SEFAZ:\n", response.text)

        status = response.status_code
        sefaz = response.text

    except ValueError as ve:
        print(f"Erro nos parâmetros: {ve}")
        return None, str(ve)
    except requests.exceptions.SSLError as ssl_err:
        print("Erro SSL:", ssl_err)
    except requests.exceptions.RequestException as e:
        print("Erro na requisição:", e)
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None, f"Erro inesperado: {e}"

 

    finally:
    # Remover arquivos temporários **apenas se eles forem criados**
        if cert_temp_file_path and os.path.exists(cert_temp_file_path):
            try:
                os.remove(cert_temp_file_path)
                print(f"Arquivo temporário {cert_temp_file_path} removido.")
            except Exception as e:
                print(f"Erro ao remover {cert_temp_file_path}: {e}")

        if key_temp_file_path and os.path.exists(key_temp_file_path):
            try:
                os.remove(key_temp_file_path)
                print(f"Arquivo temporário {key_temp_file_path} removido.")
            except Exception as e:
                print(f"Erro ao remover {key_temp_file_path}: {e}")


    return status, sefaz
