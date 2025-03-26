from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.utils.flags import NAMESPACE_NFE
from lxml import etree
import streamlit as st

import os

script_dir = os.path.dirname(os.path.abspath(__file__))


def call_cadastro(chave, certificado):

#https://homologacao.nfce.fazenda.sp.gov.br/ws/NFeStatusServico4

    # Defina se o ambiente é de homologação (True) ou produção (False)
    homologacao = True  # Altere para False se for produção

    #certificado = "/mnt/d/pythonDSA/sat/sat_system/certificados_digitais/JP_E_SOUZA_SOLUCOES_2024.pfx"
    #certificado = "/mnt/d/pythonDSA/sat/sat_system/certificados_digitais/JP_E_SOUZA_SOLUCOES_2024.pfx"

    #certificado = "/mnt/d/pythonDSA/sat/sat_system/frontend/certificados_digitais/JP_E_SOUZA_SOLUCOES_2024.pfx"

    #certificado = os.path.abspath(os.path.join(script_dir, "..", "certificados_digitais", "JP_E_SOUZA_SOLUCOES_2024.pfx"))
    #print(certificado)

    print("CERTIFICADO________________",certificado)
    print("sENHA________________",chave)
    certificado = os.path.abspath(os.path.join(script_dir, "..", "..", "certificados_digitais_emitentes", f"{certificado}.pfx"))
    


    if os.path.exists(certificado):
        print("Arquivo encontrado!")
    else:
        print("Arquivo não encontrado!")




    #certificado = "/certificados_digitais/JP_E_SOUZA_SOLUCOES_2024.pfx"
    #senha = 'tlaush2020'
    uf = 'sp'
    #D:\pythonDSA\sat\sat_system\certificados_digitais\JP_E_SOUZA_SOLUCOES_2024.pfx

    # certificado = "/mnt/d/pythonDSA/sat/sat_system/certificados_digitais/SEIS_IRMAOS.pfx"
    #senha = 'tlaush'
    senha = chave
    # uf = 'sp'


    con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
    xml = con.status_servico('nfce')     # nfe ou nfce
    print(xml.text)

    # Exemplo de leitura da resposta
    ns = {'ns': NAMESPACE_NFE}
    # Algumas UF podem ser xml.text ou xml.content
    resposta = etree.fromstring(xml.content)[0][0]

    status = resposta.xpath('ns:retConsStatServ/ns:cStat', namespaces=ns)[0].text
    motivo = resposta.xpath('ns:retConsStatServ/ns:xMotivo', namespaces=ns)[0].text

    print(status)
    print(motivo)

    return status, motivo




######main
#call_cadastro()