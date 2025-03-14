import requests
import tempfile
import os
from contextlib import ExitStack
import re



#cert_file_path = "/mnt/d/pythonDSA/sat/sat_system/certificado_teste_teste.pem"
#key_file_path = "/mnt/d/pythonDSA/sat/sat_system/key_teste_teste.pem"


# Caminhos dos arquivos de certificado e chave
#certificado_pem = "/mnt/d/pythonDSA/sat/sat_system/certificado.pem"
#chave_pem = "/mnt/d/pythonDSA/sat/sat_system/chave.pem"

certificado_pem_string = """Bag Attributes
    localKeyID: EF FA 6C 00 92 4E EE 54 D4 4F AE 63 F8 1E 6A BB 43 C7 F1 BA 
subject=C = BR, ST = SP, L = SAO PAULO, O = ICP-Brasil, OU = Secretaria da Receita Federal do Brasil - RFB, OU = RFB e-CNPJ A1, OU = AR A DIGIFORTE, OU = Videoconferencia, OU = 16464755000187, CN = JP E SOUZA SOLUCOES EM CIENCIA DE DADOS LTDA:46780934000194
issuer=C = BR, O = ICP-Brasil, OU = Secretaria da Receita Federal do Brasil - RFB, CN = AC A DIGIFORTE RFB
-----BEGIN CERTIFICATE-----
MIIIIzCCBgugAwIBAgIIcTNXUWHNbhUwDQYJKoZIhvcNAQELBQAwdzELMAkGA1UE
BhMCQlIxEzARBgNVBAoTCklDUC1CcmFzaWwxNjA0BgNVBAsTLVNlY3JldGFyaWEg
ZGEgUmVjZWl0YSBGZWRlcmFsIGRvIEJyYXNpbCAtIFJGQjEbMBkGA1UEAxMSQUMg
QSBESUdJRk9SVEUgUkZCMB4XDTI0MDYxNzE4MzE1OVoXDTI1MDYxNzE4MzE1OVow
ggEmMQswCQYDVQQGEwJCUjELMAkGA1UECBMCU1AxEjAQBgNVBAcTCVNBTyBQQVVM
TzETMBEGA1UEChMKSUNQLUJyYXNpbDE2MDQGA1UECxMtU2VjcmV0YXJpYSBkYSBS
ZWNlaXRhIEZlZGVyYWwgZG8gQnJhc2lsIC0gUkZCMRYwFAYDVQQLEw1SRkIgZS1D
TlBKIEExMRcwFQYDVQQLEw5BUiBBIERJR0lGT1JURTEZMBcGA1UECxMQVmlkZW9j
b25mZXJlbmNpYTEXMBUGA1UECxMOMTY0NjQ3NTUwMDAxODcxRDBCBgNVBAMTO0pQ
IEUgU09VWkEgU09MVUNPRVMgRU0gQ0lFTkNJQSBERSBEQURPUyBMVERBOjQ2Nzgw
OTM0MDAwMTk0MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtzAAb4ab
bomf7v96/7QSuM/cidCB8jbn31hBya1vJeYM0iGJJaaw8eFTobqHqxyd2IKx0hRx
ZeGz2/QDf7Y+uuNlrZRwBmfD4AvTKtFu1oeDE8qlr5m/0o1qxenzYWvSON6029nS
b5NS1segB1xjirVraRIN+LuTrZf8twQam71aK78PDsAicbuFaH3vhf8oAJjHaDT8
sXMcot4HDCSPfYYiFGg3mKbgwL6uHlvbtwGSAeSW1CPTNaz4/h3udFz/zWGwCZtU
HfLpvQWC7CMC3Qp5Jz/9bgdci6qjs/GFFNR5M0nJ0QRaXnVVebP7c6LoNZTgmIfD
3scpv1XLb/pE3wIDAQABo4IDADCCAvwwgaYGCCsGAQUFBwEBBIGZMIGWMF8GCCsG
AQUFBzAChlNodHRwOi8vaWNwLWJyYXNpbC52YWxpZGNlcnRpZmljYWRvcmEuY29t
LmJyL2FjLWFkaWdpZm9ydGVyZmIvYWMtYWRpZ2lmb3J0ZXJmYnY1LnA3YjAzBggr
BgEFBQcwAYYnaHR0cDovL29jc3B2NS52YWxpZGNlcnRpZmljYWRvcmEuY29tLmJy
MAkGA1UdEwQCMAAwHwYDVR0jBBgwFoAUxPe0WwbvO5J8MB9l9Po/ukAZOPcwegYD
VR0gBHMwcTBvBgZgTAECAUIwZTBjBggrBgEFBQcCARZXaHR0cDovL2ljcC1icmFz
aWwudmFsaWRjZXJ0aWZpY2Fkb3JhLmNvbS5ici9hYy1hZGlnaWZvcnRlcmZiL2Rw
Yy1hYy1hZGlnaWZvcnRlcmZidjUucGRmMIHKBgNVHR8EgcIwgb8wXaBboFmGV2h0
dHA6Ly9pY3AtYnJhc2lsLnZhbGlkY2VydGlmaWNhZG9yYS5jb20uYnIvYWMtYWRp
Z2lmb3J0ZXJmYi9sY3ItYWMtYWRpZ2lmb3J0ZXJmYnY1LmNybDBeoFygWoZYaHR0
cDovL2ljcC1icmFzaWwyLnZhbGlkY2VydGlmaWNhZG9yYS5jb20uYnIvYWMtYWRp
Z2lmb3J0ZXJmYi9sY3ItYWMtYWRpZ2lmb3J0ZXJmYnY1LmNybDAOBgNVHQ8BAf8E
BAMCBeAwHQYDVR0lBBYwFAYIKwYBBQUHAwIGCCsGAQUFBwMEMIGsBgNVHREEgaQw
gaGBFGpwbHNvdXphNzlAZ21haWwuY29toDgGBWBMAQMEoC8ELTE2MDQxOTc5MDA0
MDM5MTQwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMKAbBgVgTAEDAqASBBBK
T0FPIFBBVUxPIFNPVVpBoBkGBWBMAQMDoBAEDjQ2NzgwOTM0MDAwMTk0oBcGBWBM
AQMHoA4EDDAwMDAwMDAwMDAwMDANBgkqhkiG9w0BAQsFAAOCAgEAGbMro5DPL8QO
vXRNTfg/S/V88pcbjaQSBhiUXPG1oEZZyLnRenOxKdJ3Dw0g2sy62xFw7Kqp0U6O
Tw7rmX2MNH/p6LD1mATTYiNSUZCfWkjTA/lhngLbfOTUPgK9q+UQTD7Ue9W30PFW
80egkO7MmI/TKTxV76jugoiLBEEP/BIHel3PcXv5VCRJo+zXvfQSOM4npOSkr/mP
vSAXxlV14rRMOVtfsNAev4Aj+H1duVCqnRfwlesnajBbM8kC8vluKpAo72Y9hJTE
mtP4QmBYUuTuDmZUTfl8J0AXLhJjDcQlqDXIFf53j8VQ6bmrL/FppsR5pGRLhNDn
akrHgnc2+Yz6le6fGyHOwva+MHkFqvYGkEALvzgtQ+WdjpfBT/qT6Gfo3Z5uMUXH
3MWet5TGl/3E7EKcyyRzGfjiv3GIgSDAfTN33jxSARZbHvba+nG0McepVHJNsGTP
ZS9cheJO1bwMY2gYAfchFE4SCJeQqAGOUc+WA3i6NmXSYG095Fz8jF6WheLiBD0Y
i3wfxYAWHhHfIGXajDglU6eCRUCmW9JpPow+glJwzesltzcXrPkFxJ0B8zajmaoR
YAqkY6jBdJXmVCMYcbsVbLZixfpQtu3jTkP5X41HgpL218FU6oHU10kRuTEcZ5Sx
yDUUmWwGCADdzJhk7MmVFnBrlLc7hHE=
-----END CERTIFICATE-----"""


key_pem_string = """Bag Attributes
    localKeyID: EF FA 6C 00 92 4E EE 54 D4 4F AE 63 F8 1E 6A BB 43 C7 F1 BA 
Key Attributes: <No Attributes>
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC3MABvhptuiZ/u
/3r/tBK4z9yJ0IHyNuffWEHJrW8l5gzSIYklprDx4VOhuoerHJ3YgrHSFHFl4bPb
9AN/tj6642WtlHAGZ8PgC9Mq0W7Wh4MTyqWvmb/SjWrF6fNha9I43rTb2dJvk1LW
x6AHXGOKtWtpEg34u5Otl/y3BBqbvVorvw8OwCJxu4Vofe+F/ygAmMdoNPyxcxyi
3gcMJI99hiIUaDeYpuDAvq4eW9u3AZIB5JbUI9M1rPj+He50XP/NYbAJm1Qd8um9
BYLsIwLdCnknP/1uB1yLqqOz8YUU1HkzScnRBFpedVV5s/tzoug1lOCYh8Pexym/
Vctv+kTfAgMBAAECggEAR22OHe5smNNM61Hu0dmTG0Dhi1Mj+B/0lZ/CNzNLDYoA
Icc1xNqUUBw+Eee7krrbyVpcn7+c38775J3m51tWZmTYdrBUZgr701aJBj8Xasr4
DzWLGUdoBl9h7L3mSmxSUh50gu0SIrNdL6Yy/evGXIWU1ilWDVCGqr+CqJIPFf47
SQRRK9nwp44iS2VFxQI/GyiSrYO1o4Oxc+VMWQIgykXFc85IOc3UiOS2IQfZXrzQ
6Y5hMHxwTj2/5U9PmE8YIMbUx6WhWIFmlAtjALquQHswsJuD+J5dgzqOFlyc/74r
Cfxs2/bZMKLDk59BfNCOnP1FdIKFjRQjyZZxk9QtkQKBgQDx+KbfhSuO8VTay74G
A1Rfg6UVcfNUrD4ioNUzgLLDs4w+bpI+DnWz/4oRPhzAB93Z7OAud2qGMRS8t46T
cYXRyWUKL8b4qSV+4wjnPsu9cMVOo0FTTUmgtlo/+mUCUliIl1YBlhwz/oa4mrTr
zDY+C2Wn2ZoecJjBSyuh/oPd5QKBgQDBzuDdSbbprnS2lBkzcME46oMTDjc0va9j
CnEr4V/JI+Rfkx/3p9MkePu4aHOUExjnM/rc8WorthfSxoSRLBZ4FwgSpD/HxP/B
yxSPiL0BEYhgCKauQQQJ6umC86VxJP1N9JOuVvXNik8GHcfkEzKbKZCDFOILdS1M
ICbDnhXLcwKBgB372unNvbUL0KEAKD7kgLsJPBapNSbj5RszZNfp9bzsbc96siKA
djNk0f4K/VMKZoJPqQP5Bjk0scYk1MUOhy+UzjFx9CzyANR1W7AUBvkllT2GW1zw
MdR5ZDuTUpr0C0Z5wk2WBU6oFpefjBXAC2Sq0uD2xPNKrpMdNn3vZPXFAoGAAmzI
O3yUoU/hffdUaWRbxo6InVBsOGi3LRIQYHAtdqLQVLHOkJa0+ZvZ6nDEIXIruZjY
5rLOlUVt/uEk/3wBu/btzu3nLmS0noQf+bvIQZ8qiakSDNQbbNRXn5/UzhmcYcFR
p7jG0o+MdZMh0SS8WVynxjwYp/QLYQx177SmqSkCgYEAgrvqvq84aQf1A8DImM64
sY/gjq2TN1itmmw4Ws6DJZaNz0LYE3tEn28J8kEwqoFfUkdu3IE0XjDHsDVOTaBY
Z03UBj6WR14n2C9ZPgukVcjZ6lwACAzIIQGsWIOmD3WjLKdCI4ANMe/CeCZYQuo/
K6O/IENSQgVSPhk8EsY4RUY=
-----END PRIVATE KEY-----"""


# Limpar caracteres extras e garantir formatação correta
#certificado_limpo = "\n".join(re.findall(r"-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----", certificado_pem_string, re.DOTALL))


# with open(cert_file_path, "w", newline="") as cert_file:
#     cert_file.write(certificado_pem_string.strip() + "\n")



# Salvar corretamente o certificado no arquivo
#with open(key_file_path, "w", encoding="utf-8") as cert_file:
#   cert_file.write(key_pem_string + "\n")



with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_cert_file:
    # Escrever o conteúdo do certificado no arquivo temporário
    temp_cert_file.write(certificado_pem_string)
    
    # Obter o caminho do arquivo temporário
    cert_temp_file_path = temp_cert_file.name

print("Certificado temporário gerado em:", cert_temp_file_path)


with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_key_file:
    # Escrever o conteúdo do certificado no arquivo temporário
    temp_key_file.write(key_pem_string)
    
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

# Fazer a requisição à SEFAZ com o certificado digital
try:
    response = requests.post(
        url,
        data=soap_request.strip(),  # Remove espaços extras
        headers=headers,
        #cert=(certificado_pem, chave_pem),
        #cert=(cert_file_path, chave_pem),
        cert=(cert_temp_file_path, key_temp_file_path),
        #cert=(cert_temp_file_path, key_file_path),
        verify=cacert_path,
        timeout=30
    )
    
    print("🔹 Status Code:", response.status_code)
    print("🔹 Resposta da SEFAZ:\n", response.text)

except requests.exceptions.SSLError as ssl_err:
    print("❌ Erro SSL:", ssl_err)
except requests.exceptions.RequestException as e:
    print("❌ Erro na requisição:", e)



os.remove(cert_temp_file_path)
os.remove(key_temp_file_path)

