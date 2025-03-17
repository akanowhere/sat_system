import requests
import tempfile
import os
from contextlib import ExitStack
import re
import requests





def call_cadastro(certificado, chave):



    with tempfile.NamedTemporaryFile(delete=False, mode='wb') as temp_cert_file:
        # Escrever o conteúdo do certificado no arquivo temporário
        temp_cert_file.write(certificado.encode('utf-8'))
        
        
        # Obter o caminho do arquivo temporário
        cert_temp_file_path = temp_cert_file.name
        
        print(f"Caminho do arquivo temporário: {cert_temp_file_path}")





    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_key_file:
        # Escrever o conteúdo do certificado no arquivo temporário
        temp_key_file.write(chave)
        
        # Obter o caminho do arquivo temporário
        key_temp_file_path = temp_key_file.name

    print("Chave temporário gerado em:", key_temp_file_path)




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

    except requests.exceptions.SSLError as ssl_err:
        print("Erro SSL:", ssl_err)
    except requests.exceptions.RequestException as e:
        print("Erro na requisição:", e)

 

    os.remove(cert_temp_file_path)
    os.remove(key_temp_file_path)


    return status, sefaz
