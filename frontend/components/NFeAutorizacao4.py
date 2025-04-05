from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.entidades.cliente import Cliente
from pynfe.entidades.emitente import Emitente
from pynfe.entidades.notafiscal import NotaFiscal
from pynfe.entidades.fonte_dados import _fonte_dados
from pynfe.processamento.serializacao import SerializacaoXML
from pynfe.processamento.serializacao import SerializacaoQrcode
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.utils.flags import CODIGO_BRASIL
from decimal import Decimal
import datetime
import os

#https://homologacao.nfce.fazenda.sp.gov.br/ws/NFeAutorizacao4.asmx       

script_dir = os.path.dirname(os.path.abspath(__file__))



#def call_pedido(senha, certificado, response_emitente, quantidade, forma_pagamento_codigo):
def call_pedido(senha, certificado, response_emitente, quantidade, valor_total):
#def call_pedido():

  valor_bruto = (quantidade*valor_total)
  print("Response JSON:", response_emitente.json())
  #certificado = "/mnt/d/pythonDSA/sat/sat_system/certificados_digitais/JP_E_SOUZA_SOLUCOES_2024.pfx"
  #senha = 'tlaush2020'
  uf = 'sp'

  certificado = os.path.abspath(os.path.join(script_dir, "..", "..", "certificados_digitais_emitentes", f"{certificado}.pfx"))

  homologacao = True


    # emitente
  emitente = Emitente(
      #razao_social = response_emitente.json().get("razao_social")
      razao_social=response_emitente.json().get("razao_social"),
      nome_fantasia=response_emitente.json().get("nome_fantasia"),
      cnpj=response_emitente.json().get("cnpj"),           # cnpj apenas números
      codigo_de_regime_tributario=response_emitente.json().get("codigo_de_regime_tributario"), # 1 para simples nacional ou 3 para normal
      inscricao_estadual=response_emitente.json().get("inscricao_estadual"), # numero de IE da empresa
      inscricao_municipal='',
      cnae_fiscal=response_emitente.json().get("cnae_fiscal"),           # cnae apenas números
      endereco_logradouro=response_emitente.json().get("endereco_logradouro"),
      endereco_numero=response_emitente.json().get("endereco_numero"),
      endereco_bairro=response_emitente.json().get("endereco_bairro"),
      endereco_municipio=response_emitente.json().get("endereco_municipio"),
      endereco_uf=response_emitente.json().get("endereco_uf"),
      endereco_cep=response_emitente.json().get("endereco_cep"),
      endereco_pais=CODIGO_BRASIL
  )


  # emitente
  # emitente = Emitente(
  #     #razao_social = response_emitente.json().get("razao_social")
  #     razao_social='NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL',
  #     nome_fantasia='Nome Fantasia da Empresa',
  #     cnpj='46780934000194',           # cnpj apenas números
  #     codigo_de_regime_tributario='1', # 1 para simples nacional ou 3 para normal
  #     inscricao_estadual='956224310481', # numero de IE da empresa
  #     inscricao_municipal='',
  #     cnae_fiscal='9999999',           # cnae apenas números
  #     endereco_logradouro='Rua da Paz',
  #     endereco_numero='666',
  #     endereco_bairro='Sossego',
  #     endereco_municipio='São Paulo',
  #     endereco_uf='SP',
  #     endereco_cep='01002000',
  #     endereco_pais=CODIGO_BRASIL
  # )

  # cliente
  cliente = Cliente(
      razao_social='NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL',
      tipo_documento='CPF',           #CPF ou CNPJ
      email='',
      numero_documento='00403914000', # numero do cpf ou cnpj
      indicador_ie=9,                 # 9=Não contribuinte 1	Contribuinte de ICMS (possui Inscrição Estadual) 2	Contribuinte isento de Inscrição Estadual
      endereco_logradouro='',
      endereco_numero='',
      endereco_complemento='',
      endereco_bairro='',
      endereco_municipio='',
      endereco_uf='SP',
      endereco_cep='',
      endereco_pais=CODIGO_BRASIL,
      endereco_telefone='',
  )

  # Nota Fiscal
  nota_fiscal = NotaFiscal(
    emitente=emitente,
    cliente=cliente,
    uf=uf.upper(),
    natureza_operacao='VENDA', # venda, compra, transferência, devolução, etc
    forma_pagamento=0,          # 0=Pagamento à vista; 1=Pagamento a prazo; 2=Outros
    tipo_pagamento=1,
    #tipo_pagamento=int(forma_pagamento_codigo),          #01 - Dinheiro     02 - Cheque      03 - Cartão de Crédito       04 - Cartão de Débito      10 - Vale Alimentação  11 - Vale Refeição
    modelo=65,                 # 55=NF-e; 65=NFC-e
    serie='1',
    numero_nf=response_emitente.json().get("id_nota"), 
    #numero_nf='144',         # Número do Documento Fiscal.          # Número do Documento Fiscal.
    data_emissao=datetime.datetime.now(),
    data_saida_entrada=datetime.datetime.now(),
    tipo_documento=1,          # 0=entrada; 1=saida
    municipio='3550308',       # Código IBGE do Município 
    tipo_impressao_danfe=4,    # 0=Sem geração de DANFE;1=DANFE normal, Retrato;2=DANFE normal Paisagem;3=DANFE Simplificado;4=DANFE NFC-e;
    forma_emissao='1',         # 1=Emissão normal (não em contingência); "9" → Contingência Off-line
    cliente_final=1,           # "0" → Não (exemplo: venda para empresa, revenda);1=Consumidor final;
    indicador_destino=1,       # "1" → Operação dentro do estado "2" → Operação interestadual "3" → Operação com exterior
    indicador_presencial=1,    #"0" → Não se aplica "1" → Operação presencial "2" → Operação não presencial (internet, telefone) "3" → Venda para entrega em domicílio "4" → NFC-e em operação com entrega futura "9" → Outras situações
    finalidade_emissao='1',    # 1=NF-e normal;2=NF-e complementar;3=NF-e de ajuste;4=Devolução de mercadoria.
    processo_emissao='0',      #0=Emissão de NF-e com aplicativo do contribuinte; "1" → Emissão pelo Fisco
    transporte_modalidade_frete=9, # "0"	Sem frete – O transporte não será cobrado separadamente. Geralmente usado na NFC-e (venda direta ao consumidor). "1"	Frete por conta do emitente – O vendedor (emitente da nota) assume os custos do frete. "2"	Frete por conta do destinatário/remetente – O comprador (destinatário) assume os custos do frete. "3"	Frete por conta de terceiros – O frete será pago por um terceiro, que não é o emitente nem o destinatário. "4"	Transporte próprio por conta do remetente – O próprio vendedor faz o transporte com frota própria. "5"	Transporte próprio por conta do destinatário – O próprio comprador retira ou transporta a mercadoria com frota própria. "9"	Sem ocorrência de transporte – Não há transporte envolvido na operação (exemplo: venda onde o cliente retira o produto na loja).
    informacoes_adicionais_interesse_fisco='Mensagem complementar',
    totais_tributos_aproximado=Decimal('21.06'),
  )

  # Produto
  nota_fiscal.adicionar_produto_servico(
      codigo='000328',                           # id do produto
      descricao='NOTA FISCAL EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL',
      ncm='21069090',
      #cest='0100100',                            # NT2015/003
      cfop='5102',
      unidade_comercial='UN',
      ean='SEM GTIN',
      ean_tributavel='SEM GTIN',
      quantidade_comercial=Decimal(quantidade),        # 12 unidades
      valor_unitario_comercial=Decimal(valor_total),
      #valor_unitario_comercial=Decimal('9.75'),  # preço unitário
      #valor_total_bruto=Decimal('117.00'),       # preço total
      valor_total_bruto = Decimal(valor_bruto),      # preço total,
      unidade_tributavel='UN',
      #quantidade_tributavel=Decimal('12'),
      #valor_unitario_tributavel=Decimal('9.75'),
      quantidade_tributavel=Decimal(quantidade),
      valor_unitario_tributavel=Decimal(valor_total),
      ind_total=1,
      # numero_pedido='12345',                   # xPed
      # numero_item='123456',                    # nItemPed
      icms_modalidade='102',
      icms_origem=0,
      icms_csosn='400',
      pis_modalidade='07',
      cofins_modalidade='07',
      valor_tributos_aprox='21.06'
      )

  # responsável técnico
  nota_fiscal.adicionar_responsavel_tecnico(
      cnpj='46780934000194',
      contato='jpsouzaengenhariadedados',
      email='jpsouzaengenhariadedados@gmail.com',
      fone='51985915924'
    )

  # exemplo de nota fiscal referenciada (devolução/garantia)
  # nfRef = NotaFiscalReferenciada(
  #     chave_acesso='99999999999999999999999999999999999999999999')
  # nota_fiscal.notas_fiscais_referenciadas.append(nfRef)

  # exemplo de grupo de pessoas autorizadas a baixar xml
  # autxml_lista = ['99999999000199', '00000000040']
  # for index, item in enumerate(autxml_lista, 1):
  #    nota_fiscal.adicionar_autorizados_baixar_xml(CPFCNPJ=item)

  # serialização
  # serialização
  serializador = SerializacaoXML(_fonte_dados, homologacao=homologacao)
  nfce = serializador.exportar()

  # assinatura
  a1 = AssinaturaA1(certificado, senha)
  xml = a1.assinar(nfce)

  # token de homologacao
  token = '000001'

  # csc de homologação
  csc = 'ad438d2a-dfbe-4187-a97d-80cfa2a044d9'

  # gera e adiciona o qrcode no xml NT2015/003
  xml_com_qrcode = SerializacaoQrcode().gerar_qrcode(token, csc, xml)

  # envio
  con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
  envio = con.autorizacao(modelo='nfce', nota_fiscal=xml_com_qrcode)

  # em caso de sucesso o retorno será o xml autorizado
  # Ps: no modo sincrono, o retorno será o xml completo (<nfeProc> = <NFe> + <protNFe>)
  # no modo async é preciso montar o nfeProc, juntando o retorno com a NFe  
  from lxml import etree
  if envio[0] == 0:
    print('Sucesso!')
    resposta_xml = etree.tostring(envio[1], pretty_print=True, encoding="unicode")
    tags= etree.fromstring(resposta_xml.encode('utf-8'))
    n_nf = tags.find('.//{*}nNF')  # {*} ignora o namespace
    if n_nf is not None:
      print("Número da NF:", n_nf.text)

# Exemplo: extrair a chave de acesso (tag <infNFe>, atributo Id)
    inf_nfe = tags.find('.//{*}infNFe')
    if inf_nfe is not None:
      chave_acesso = inf_nfe.attrib.get('Id', '')[-44:]  # os últimos 44 dígitos geralmente são a chave
      print("Chave de acesso:", chave_acesso)
    n_prot = tags.find('.//{*}nProt')
    if n_prot is not None:
      print("Número do protocolo:", n_prot.text)
    dh_recbto = tags.find('.//{*}dhRecbto')
    if dh_recbto is not None:
        print("Data de recebimento:", dh_recbto.text)
    c_stat = tags.find('.//{*}cStat')
    x_motivo = tags.find('.//{*}xMotivo')
    if c_stat is not None and x_motivo is not None:
      print("Status:", c_stat.text)
      print("Motivo:", x_motivo.text)

    
    print('📜 Resposta completa da SEFAZ:')
    print(resposta_xml)
    print(etree.tostring(envio[1], encoding="unicode").replace('\n','').replace('ns0:',''))
    return {
      "status": "sucesso",
      "chave_acesso": chave_acesso,
      "n_prot": n_prot.text,
      "x_motivo": x_motivo.text,
      "Status_sefaz": c_stat.text,
      "data_recebimento": dh_recbto.text
      }

  # em caso de erro o retorno será o xml de resposta da SEFAZ + NF-e enviada
  else:
    print('Erro:')
    print(envio[1].text) # resposta
    print('Nota:')
    print(etree.tostring(envio[2], encoding="unicode")) # nfe

    return {
        "status": "erro"
        }





#def call_pedido_sem_cpf(senha, certificado, response_emitente, forma_pagamento_codigo):
def call_pedido_sem_cpf(senha, certificado, response_emitente, quantidade, valor_total):

#def call_pedido():


  # valor_bruto = (quantidade*valor_total)
  # print(valor_bruto)
  # print("Response JSON:", response_emitente.json())
  # print('________________TIPO VAR',type(valor_bruto))
  # input("TESTE")
  #certificado = "/mnt/d/pythonDSA/sat/sat_system/certificados_digitais/JP_E_SOUZA_SOLUCOES_2024.pfx"
  #senha = 'tlaush2020'
  print("Response JSON:", response_emitente.json())
  valor_bruto = (quantidade*valor_total)
  uf = 'sp'

  certificado = os.path.abspath(os.path.join(script_dir, "..", "..", "certificados_digitais_emitentes", f"{certificado}.pfx"))

  homologacao = True


    # emitente
  emitente = Emitente(
      #razao_social = response_emitente.json().get("razao_social")
      razao_social=response_emitente.json().get("razao_social"),
      nome_fantasia=response_emitente.json().get("nome_fantasia"),
      cnpj=response_emitente.json().get("cnpj"),           # cnpj apenas números
      codigo_de_regime_tributario=response_emitente.json().get("codigo_de_regime_tributario"), # 1 para simples nacional ou 3 para normal
      inscricao_estadual=response_emitente.json().get("inscricao_estadual"), # numero de IE da empresa
      inscricao_municipal='',
      cnae_fiscal=response_emitente.json().get("cnae_fiscal"),           # cnae apenas números
      endereco_logradouro=response_emitente.json().get("endereco_logradouro"),
      endereco_numero=response_emitente.json().get("endereco_numero"),
      endereco_bairro=response_emitente.json().get("endereco_bairro"),
      endereco_municipio=response_emitente.json().get("endereco_municipio"),
      endereco_uf=response_emitente.json().get("endereco_uf"),
      endereco_cep=response_emitente.json().get("endereco_cep"),
      endereco_pais=CODIGO_BRASIL
  )


  # emitente
  # emitente = Emitente(
  #     #razao_social = response_emitente.json().get("razao_social")
  #     razao_social='NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL',
  #     nome_fantasia='Nome Fantasia da Empresa',
  #     cnpj='46780934000194',           # cnpj apenas números
  #     codigo_de_regime_tributario='1', # 1 para simples nacional ou 3 para normal
  #     inscricao_estadual='956224310481', # numero de IE da empresa
  #     inscricao_municipal='',
  #     cnae_fiscal='9999999',           # cnae apenas números
  #     endereco_logradouro='Rua da Paz',
  #     endereco_numero='666',
  #     endereco_bairro='Sossego',
  #     endereco_municipio='São Paulo',
  #     endereco_uf='SP',
  #     endereco_cep='01002000',
  #     endereco_pais=CODIGO_BRASIL
  # )

  # cliente
  cliente = Cliente(
      razao_social='NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL',
      tipo_documento='CPF',           #CPF ou CNPJ
      email='',
      numero_documento='00403914000', # numero do cpf ou cnpj
      indicador_ie=9,                 # 9=Não contribuinte 1	Contribuinte de ICMS (possui Inscrição Estadual) 2	Contribuinte isento de Inscrição Estadual
      endereco_logradouro='',
      endereco_numero='0',
      endereco_complemento='',
      endereco_bairro='',
      endereco_municipio='',
      endereco_uf='SP',
      endereco_cep='',
      endereco_pais=CODIGO_BRASIL,
      endereco_telefone='',
  )

  # Nota Fiscal
  nota_fiscal = NotaFiscal(
    emitente=emitente,
    #cliente=cliente,
    uf=uf.upper(),
    natureza_operacao='VENDA', # venda, compra, transferência, devolução, etc
    forma_pagamento=0,         # 0=Pagamento à vista; 1=Pagamento a prazo; 2=Outros.
    tipo_pagamento=1,
    modelo=65,                 # 55=NF-e; 65=NFC-e
    serie='1',
    numero_nf=response_emitente.json().get("id_nota"),           # Número do Documento Fiscal.
    #numero_nf='144',         # Número do Documento Fiscal.
    data_emissao=datetime.datetime.now(),
    data_saida_entrada=datetime.datetime.now(),
    tipo_documento=1,          # 0=entrada; 1=saida
    municipio='3550308',       # Código IBGE do Município 
    tipo_impressao_danfe=4,    # 0=Sem geração de DANFE;1=DANFE normal, Retrato;2=DANFE normal Paisagem;3=DANFE Simplificado;4=DANFE NFC-e;
    forma_emissao='1',         # 1=Emissão normal (não em contingência);
    cliente_final=1,           # 0=Normal;1=Consumidor final;
    indicador_destino=1,
    indicador_presencial=1,
    finalidade_emissao='1',    # 1=NF-e normal;2=NF-e complementar;3=NF-e de ajuste;4=Devolução de mercadoria.
    processo_emissao='0',      #0=Emissão de NF-e com aplicativo do contribuinte;
    transporte_modalidade_frete=9,
    informacoes_adicionais_interesse_fisco='Mensagem complementar',
    totais_tributos_aproximado=Decimal('21.06'),
  )

  # Produto
  nota_fiscal.adicionar_produto_servico(
      codigo='000328',                           # id do produto
      descricao='NOTA FISCAL EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL',
      ncm='21069090',
      #cest='0100100',                            # NT2015/003
      cfop='5102',
      unidade_comercial='UN',
      ean='SEM GTIN',
      ean_tributavel='SEM GTIN',
      quantidade_comercial=Decimal(quantidade),
      #quantidade_comercial=Decimal('12'),        # 12 unidades
      #valor_unitario_comercial=Decimal('9.75'),
      valor_unitario_comercial=Decimal(valor_total),  # preço unitário
      #valor_total_bruto=Decimal('117.00'), 
      valor_total_bruto = Decimal(valor_bruto),      # preço total
      unidade_tributavel='UN',
      quantidade_tributavel=Decimal(quantidade),
      valor_unitario_tributavel=Decimal(valor_total),
      #quantidade_tributavel=Decimal('12'),
      #valor_unitario_tributavel=Decimal('9.75'),
      ind_total=1,
      # numero_pedido='12345',                   # xPed
      # numero_item='123456',                    # nItemPed
      icms_modalidade='102',
      icms_origem=0,
      icms_csosn='400',
      pis_modalidade='07',
      cofins_modalidade='07',
      valor_tributos_aprox='21.06'
      )

  # responsável técnico
  nota_fiscal.adicionar_responsavel_tecnico(
      cnpj='46780934000194',
      contato='jpsouzaengenhariadedados',
      email='jpsouzaengenhariadedados@gmail.com',
      fone='51985915924'
    )

  # exemplo de nota fiscal referenciada (devolução/garantia)
  # nfRef = NotaFiscalReferenciada(
  #     chave_acesso='99999999999999999999999999999999999999999999')
  # nota_fiscal.notas_fiscais_referenciadas.append(nfRef)

  # exemplo de grupo de pessoas autorizadas a baixar xml
  # autxml_lista = ['99999999000199', '00000000040']
  # for index, item in enumerate(autxml_lista, 1):
  #    nota_fiscal.adicionar_autorizados_baixar_xml(CPFCNPJ=item)

  # serialização
  # serialização
  serializador = SerializacaoXML(_fonte_dados, homologacao=homologacao)
  nfce = serializador.exportar()

  # assinatura
  a1 = AssinaturaA1(certificado, senha)
  xml = a1.assinar(nfce)

  # token de homologacao
  token = '000001'

  # csc de homologação
  #csc = 'ad438d2a-dfbe-4187-a97d-80cfa2a044d9'
  csc=response_emitente.json().get("cod_seguranca")

  # gera e adiciona o qrcode no xml NT2015/003
  xml_com_qrcode = SerializacaoQrcode().gerar_qrcode(token, csc, xml)

  # envio
  con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
  envio = con.autorizacao(modelo='nfce', nota_fiscal=xml_com_qrcode)

  # em caso de sucesso o retorno será o xml autorizado
  # Ps: no modo sincrono, o retorno será o xml completo (<nfeProc> = <NFe> + <protNFe>)
  # no modo async é preciso montar o nfeProc, juntando o retorno com a NFe  
  from lxml import etree
  if envio[0] == 0:
    print('Sucesso!')
    resposta_xml = etree.tostring(envio[1], pretty_print=True, encoding="unicode")
    tags= etree.fromstring(resposta_xml.encode('utf-8'))
    n_nf = tags.find('.//{*}nNF')  # {*} ignora o namespace
    if n_nf is not None:
      print("Número da NF:", n_nf.text)

# Exemplo: extrair a chave de acesso (tag <infNFe>, atributo Id)
    inf_nfe = tags.find('.//{*}infNFe')
    if inf_nfe is not None:
      chave_acesso = inf_nfe.attrib.get('Id', '')[-44:]  # os últimos 44 dígitos geralmente são a chave
      print("Chave de acesso:", chave_acesso)
    n_prot = tags.find('.//{*}nProt')
    if n_prot is not None:
      print("Número do protocolo:", n_prot.text)
    dh_recbto = tags.find('.//{*}dhRecbto')
    if dh_recbto is not None:
        print("Data de recebimento:", dh_recbto.text)
    c_stat = tags.find('.//{*}cStat')
    x_motivo = tags.find('.//{*}xMotivo')
    if c_stat is not None and x_motivo is not None:
      print("Status:", c_stat.text)
      print("Motivo:", x_motivo.text)

    
    print('📜 Resposta completa da SEFAZ:')
    print(resposta_xml)
    print(etree.tostring(envio[1], encoding="unicode").replace('\n','').replace('ns0:',''))
    return {
      "status": "sucesso",
      "chave_acesso": chave_acesso,
      "n_prot": n_prot.text,
      "x_motivo": x_motivo.text,
      "Status_sefaz": c_stat.text,
      "data_recebimento": dh_recbto.text
      }

  # em caso de erro o retorno será o xml de resposta da SEFAZ + NF-e enviada
  else:
    print('Erro:')
    print(envio[1].text) # resposta
    print('Nota:')
    print(etree.tostring(envio[2], encoding="unicode")) # nfe

    return {
        "status": "erro"
        }





###########################MAIN######################


#call_pedido()