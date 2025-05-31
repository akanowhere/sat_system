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
from lxml import etree
import requests
from decimal import Decimal, ROUND_HALF_UP

#https://homologacao.nfce.fazenda.sp.gov.br/ws/NFeAutorizacao4.asmx       

script_dir = os.path.dirname(os.path.abspath(__file__))



#def call_pedido(senha, certificado, response_emitente, quantidade, forma_pagamento_codigo):
def call_pedido(senha, certificado, response_emitente, quantidade, valor_total, forma_pagamento_codigo, cpf, produtos_nome, produto_selecionado, carrinho):
#def call_pedido():

  
  print("Response JSON:", response_emitente.json())
  print("Response FORMA DE PAGAMNETO_________:", forma_pagamento_codigo)
  print("Response PRODUTO NOME_________:",produtos_nome)
  print("Response PRODUTO SELECIONADO_________:",produto_selecionado)
  print("Response NCM___________________________:",produto_selecionado["ncm"])
  print("Response CARRINHO___________________________:",carrinho)
  print("Response CARRINHO TESTE___________________________:",carrinho[0])
  print("Response CARRINHO csosn___________________________:",carrinho[0]["csosn"])
  print("Response CARRINHO origem_icms___________________________:",carrinho[0]["origem_icms"])
  print("Response CARRINHO origem_icms___________________________:",carrinho[0]["preco_unitario"])
  print("Response CARRINHO origem_icms___________________________:",carrinho[0]["quantidade"])
  #valor_bruto = (quantidade*valor_total)
  #valor_bruto = (quantidade*produto_selecionado["preco_unitario"])
  #valor_final =  (quantidade*produto_selecionado["preco_unitario"])
  #valor_tributos_aprox = (valor_final*produto_selecionado["valor_tributos_aprox"])

 #valor_bruto = (quantidade*valor_total)
  #valor_bruto = (quantidade*produto_selecionado["preco_unitario"])
  #valor_bruto = (carrinho[0]["quantidade"] * carrinho[0]["preco_unitario"])
  #valor_final =  (quantidade*produto_selecionado["preco_unitario"])
  #valor_tributos_aprox = (valor_final*produto_selecionado["valor_tributos_aprox"])
  #valor_tributos_aprox = round(valor_bruto*carrinho[0]["valor_tributos_aprox"],2)
  #valor_total_unit = (carrinho[0]["quantidade"] * carrinho[0]["preco_unitario"])
  #valor_total = sum(item['quantidade'] * item['preco_unitario'] for item in carrinho)

  
  #valor_bruto = (quantidade*produto_selecionado["preco_unitario"])
  # print("Response JSON:", response_emitente.json())
  # print("Response FORMA DE PAGAMNETO_________:", forma_pagamento_codigo)
  # print("Response CPF CLIENTE_________:", cpf)
  # print("Response PRODUTO NOME_________:",produtos_nome)
  # print("Response produto_selecionado___________________________:",produto_selecionado)
  # print("Response NCM___________________________:",produto_selecionado["ncm"])
  # print("Response VALOR BRUTO___________________________:",valor_bruto)
  # print("Response VALOR BRUTO___________________________:",valor_final)
  # print("Response CARRINHO___________________________:",carrinho)
  # print("Response valor_tributos_aprox___________________________:",valor_tributos_aprox)
  # print("Response VALOR BRUTO___________________________:",valor_bruto)
  # print("Response VALOR FINAL___________________________:",valor_final)
  # print("Response VALOR UNIT___________________________:",valor_total_unit)
  
  cpf = str(cpf)
  #certificado = "/mnt/d/pythonDSA/sat/sat_system/certificados_digitais/JP_E_SOUZA_SOLUCOES_2024.pfx"
  #senha = 'tlaush2020'
  uf = 'sp'

  certificado = os.path.abspath(os.path.join(script_dir, "..", "..", "certificados_digitais_emitentes", f"{certificado}.pfx"))


  if response_emitente.json().get("env") == True:
    homologacao = True #Altere para True se for homologação
  elif response_emitente.json().get("env") == False:
    homologacao = False #Altere para False se for produção

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
      razao_social='',
      tipo_documento='CPF',           #CPF ou CNPJ
      email='',
      #numero_documento='00403914000',
      numero_documento=cpf, # numero do cpf ou cnpj
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
    tipo_pagamento = forma_pagamento_codigo,
    #tipo_pagamento=1,
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
    #totais_tributos_aproximado=Decimal('21.06'),
    #totais_tributos_aproximado=Decimal(valor_tributos_aprox),
    totais_tributos_aproximado=Decimal('0.00'),
    #totais_tributos_aproximado=Decimal(valor_tributos_aprox),
  )

  #total_valor_bruto = Decimal('0.00')
  #nItem = 1

  # for produto in carrinho:
  #       quantidade = Decimal(str(produto["quantidade"]))
  #       preco_unitario = Decimal(str(produto["preco_unitario"]))
  #       valor_total_produto = quantidade * preco_unitario
  #       total_valor_bruto += valor_total_produto
  
  # Produto
   # Produto
  #valor_bruto_total = 0.00
  #valor_tributos_aprox_total = 0.00
  valor_bruto_total = Decimal('0.00')        # alterado para Decimal
  valor_tributos_aprox_total = Decimal('0.00') # alterado para Decimal
  nItem = 1

  for produto in carrinho:
    print(produto)

    quantidade_prod = Decimal(str(produto["quantidade"]))
    preco_unit_prod = Decimal(str(produto["preco_unitario"]))
    valor_tributos_aprox_porcent = Decimal(str(produto["valor_tributos_aprox"]))

  
    #valor_bruto = (produto["quantidade"] * produto["preco_unitario"])
    valor_bruto = (quantidade_prod * preco_unit_prod).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)  # <-- ARREDONDAMENTO AQUI

    #valor_final =  (quantidade*produto_selecionado["preco_unitario"])
    valor_final = (Decimal(str(quantidade)) * Decimal(str(produto_selecionado["preco_unitario"]))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)  # <-- ARREDONDAMENTO AQUI

    #valor_tributos_aprox = round(valor_bruto*produto["valor_tributos_aprox"],2)
    valor_tributos_aprox = (valor_bruto * valor_tributos_aprox_porcent).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)  # <-- ARREDONDAMENTO AQUI

    #valor_total_unit = (produto["quantidade"] * produto["preco_unitario"])
    valor_total_unit = (quantidade_prod * preco_unit_prod).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)  # <-- ARREDONDAMENTO AQUI

    valor_bruto_total += valor_bruto
    valor_tributos_aprox_total += valor_tributos_aprox

    print("Response preco_unitario:", produto_selecionado["preco_unitario"] ,"tipo", type(produto_selecionado["preco_unitario"] ))
    print("Response QUANTIDADE___________________________:",quantidade,"tipo", type(quantidade))
    print("Response VALOR TOTAL___________________________:",valor_total,"tipo", type(valor_total))
    #print("Response VALOR BRUTO___________________________:",valor_bruto, "tipo", type(valor_bruto))
    print("Response VALOR BRUTO___________________________:", valor_bruto)
    #print("Response VALOR FINAL___________________________:",valor_final,"tipo", type(valor_final))
    print("Response VALOR FINAL___________________________:", valor_final)
    #print("Response valor_tributos_aprox___________________________:",valor_tributos_aprox,"tipo", type(valor_final))
    print("Response valor_tributos_aprox___________________________:", valor_tributos_aprox)
    print("Response VALOR BRUTO___________________________:",valor_bruto)
    print("Response VALOR FINAL___________________________:",valor_final)
    print("Response VALOR UNIT___________________________:",valor_total_unit)



    nota_fiscal.adicionar_produto_servico(
        #codigo='000328',                           # id do produto
        codigo=produto["codigo"],
        #descricao='NOTA FISCAL EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL',
        #descricao=produtos_nome,
        descricao=produto["descricao"],
        #ncm='21069090',
        ncm=produto["ncm"],
        #cest='0100100',                            # NT2015/003
        #cfop='5102',
        cfop=produto["cfop"],
        #unidade_comercial='UN',
        unidade_comercial=produto["unidade_tributavel"],
        ean='SEM GTIN',
        ean_tributavel='SEM GTIN',
        #quantidade_comercial=Decimal(quantidade),
        #quantidade_comercial=Decimal(produto["quantidade"]),
        quantidade_comercial=quantidade_prod,
        #quantidade_comercial=Decimal('12'),        # 12 unidades
        #valor_unitario_comercial=Decimal('9.75'),
        #valor_unitario_comercial=Decimal(valor_total),  # preço unitário
        #valor_unitario_comercial=Decimal(produto["preco_unitario"]),  ###### preço unitário
        valor_unitario_comercial=preco_unit_prod,
        #valor_total_bruto=Decimal('117.00'), 
        valor_total_bruto=valor_bruto,
        #valor_total_bruto = Decimal(valor_bruto),      # preço total
        #unidade_tributavel='UN',
        unidade_tributavel=produto["unidade_tributavel"],
        #quantidade_tributavel=Decimal(quantidade),
        #quantidade_tributavel=Decimal(produto["quantidade"]),
        quantidade_tributavel=quantidade_prod,
        #valor_unitario_tributavel=Decimal(valor_total),################
        #valor_unitario_tributavel=Decimal(produto_selecionado["preco_unitario"] ),
        valor_unitario_tributavel=Decimal(produto["preco_unitario"]),
        #quantidade_tributavel=Decimal('12'),
        #valor_unitario_tributavel=Decimal('9.75'),
        ind_total=1,
        # numero_pedido='12345',                   # xPed
        # numero_item='123456',                    # nItemPed
        icms_modalidade='102', # 101	Tributada com permissão de crédito  102	Tributada sem permissão de crédito 103	Isenção do ICMS   201	Tributada com permissão de crédito e com cobrança do ICMS por Substituição Tributária (ST)  202	Tributada sem permissão de crédito e com cobrança do ICMS por ST   203	Isenção do ICMS e com cobrança do ICMS por ST  300	Imune  400	Não tributada pelo Simples Nacional  500	ICMS cobrado anteriormente por substituição tributária (ST) ou por antecipação   900	Outros
        #icms_modalidade='102',
        #icms_origem=0,  # 0	Nacional – exceto as indicadas nos códigos 3, 4, 5 e 8 -- 1	Estrangeira – Importação direta --2	Estrangeira – Adquirida no mercado interno ---3	Nacional – com conteúdo de importação superior a 40%    ----4	Nacional – produzida com processo básico da ZFM  ----   5	Nacional – com conteúdo de importação inferior a 40%   ---- 6	Estrangeira – Importação direta sem similar nacional ---- 7	Estrangeira – Adquirida no mercado interno sem similar nacional   --- 8	Nacional – conteúdo de importação entre 70% e 100%
        icms_origem=produto["origem_icms"],
        #icms_csosn='400', # ("101", "Tributada pelo Simples Nacional com permissão de crédito"),("102", "Tributada pelo Simples Nacional sem permissão de crédito"), ("103", "Isenção do ICMS no Simples Nacional para faixa de receita bruta"),("201", "Tributada pelo Simples Nacional com permissão de crédito e com cobrança do ICMS por substituição tributária"),("202", "Tributada pelo Simples Nacional sem permissão de crédito e com cobrança do ICMS por substituição tributária"),("203", "Isenção do ICMS no Simples Nacional para faixa de receita bruta e com cobrança do ICMS por substituição tributária"),("300", "Imune"),("400", "Não tributada pelo Simples Nacional"),("500", "ICMS cobrado anteriormente por substituição tributária (substituído) ou por antecipação"),("900", "Outros")
        icms_csosn=produto["csosn"],
        #pis_modalidade='07', # ("01", "Margem Valor Agregado (%)"), ("02", "Pauta (valor)"), ("03", "Preço Tabelado Máx. (valor)"), ("04", "Valor da operação"),  ("05", "Operação Tributável (alíquota diferenciada)"), ("06", "Outros"), ("07", "Operação Isenta da Contribuição"),("08", "Operação sem Incidência da Contribuição"), ("09", "Operação com Suspensão da Contribuição")
        pis_modalidade=produto["pis_modalidade"],
        #cofins_modalidade='07', # # ("01", "Margem Valor Agregado (%)"), ("02", "Pauta (valor)"), ("03", "Preço Tabelado Máx. (valor)"), ("04", "Valor da operação"),  ("05", "Operação Tributável (alíquota diferenciada)"), ("06", "Outros"), ("07", "Operação Isenta da Contribuição"),("08", "Operação sem Incidência da Contribuição"), ("09", "Operação com Suspensão da Contribuição")
        cofins_modalidade=produto["cofins_modalidade"],
        #valor_tributos_aprox='10.06'
        valor_tributos_aprox= str(valor_tributos_aprox)
        #valor_tributos_aprox=Decimal(valor_tributos_aprox)
        )
    nItem += 1
  nota_fiscal.totais_tributos_aproximado = valor_tributos_aprox_total


  # nota_fiscal.adicionar_produto_servico(
  #     #codigo='000328',                           # id do produto
  #     codigo=carrinho[0]["codigo"],
  #     #descricao='NOTA FISCAL EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL',
  #     #descricao=produtos_nome,
  #     descricao=carrinho[0]["descricao"],
  #     #ncm='21069090',
  #     ncm=carrinho[0]["ncm"],
  #     #cest='0100100',                            # NT2015/003
  #     cfop=carrinho[0]["cfop"], # 5101: Venda de produção do estabelecimento   5102: Venda de mercadoria de terceiros   5405: Venda de mercadoria adquirida de terceiros, sujeita à ST
  #     #unidade_comercial='UN', # unidades de medida
  #     unidade_comercial=carrinho[0]["unidade_tributavel"],
  #     ean='SEM GTIN', #código de barras
  #     ean_tributavel='SEM GTIN', #código de barras
  #     quantidade_comercial=Decimal(carrinho[0]["quantidade"]),        # 12 unidades
  #     valor_unitario_comercial=Decimal(carrinho[0]["preco_unitario"]),
  #     #valor_unitario_comercial=Decimal('9.75'),  # preço unitário
  #     #valor_total_bruto=Decimal('117.00'),       # preço total
  #     valor_total_bruto = Decimal(valor_bruto),      # preço total,
  #     unidade_tributavel=carrinho[0]["unidade_tributavel"], # unidades de medida
  #     #quantidade_tributavel=Decimal('12'),
  #     #valor_unitario_tributavel=Decimal('9.75'),
  #     quantidade_tributavel=Decimal(carrinho[0]["quantidade"]),
  #     valor_unitario_tributavel=Decimal(carrinho[0]["preco_unitario"]),
  #     ind_total=1, # 0 = Não compõe o valor total da NF-e (não soma no total) 1 = Compõe o valor total da NF-e (soma no total)
  #     # numero_pedido='12345',                   # xPed
  #     # numero_item='123456',                    # nItemPed
  #     icms_modalidade='102',
  #     icms_origem=carrinho[0]["origem_icms"],
  #     icms_csosn=carrinho[0]["csosn"],
  #     pis_modalidade=carrinho[0]["pis_modalidade"],
  #     cofins_modalidade=carrinho[0]["cofins_modalidade"],
  #     #valor_tributos_aprox='21.06'
  #     valor_tributos_aprox= str(valor_tributos_aprox)
  #     #valor_tributos_aprox=Decimal(valor_tributos_aprox)
  #     )

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

  
  # token de produçãp
  # token = '1'

  if response_emitente.json().get("env") == True:
    # csc de homologação
    csc = response_emitente.json().get("cod_seguranca")
  elif response_emitente.json().get("env") == False:
    # csc de produção
    csc = response_emitente.json().get("cod_seguranca_prod")

  # csc de homologação
  #csc = response_emitente.json().get("cod_seguranca")

  # gera e adiciona o qrcode no xml NT2015/003
  xml_com_qrcode = SerializacaoQrcode().gerar_qrcode(token, csc, xml)

  # envio
  con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
  envio = con.autorizacao(modelo='nfce', nota_fiscal=xml_com_qrcode)

  # em caso de sucesso o retorno será o xml autorizado
  # Ps: no modo sincrono, o retorno será o xml completo (<nfeProc> = <NFe> + <protNFe>)
  # no modo async é preciso montar o nfeProc, juntando o retorno com a NFe  
  
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
    nfe_tree = etree.ElementTree(envio[2])  # Cria a árvore a partir do XML da NF-e
    print(etree.tostring(nfe_tree.getroot(), encoding="unicode", pretty_print=True))  # Exibe o XML em formato de árvore


    return {
        "status": "erro"
        }





#def call_pedido_sem_cpf(senha, certificado, response_emitente, forma_pagamento_codigo):
def call_pedido_sem_cpf(senha, certificado, response_emitente, quantidade, valor_total, forma_pagamento_codigo, produtos_nome, produto_selecionado, carrinho):


  print("Response JSON:", response_emitente.json())
  print("Response FORMA DE PAGAMNETO_________:", forma_pagamento_codigo)
  print("Response PRODUTO NOME_________:",produtos_nome)
  print("Response PRODUTO SELECIONADO_________:",produto_selecionado)
  print("Response NCM___________________________:",produto_selecionado["ncm"])
  print("Response CARRINHO___________________________:",carrinho)
  print("Response CARRINHO TESTE___________________________:",carrinho[0])
  print("Response CARRINHO csosn___________________________:",carrinho[0]["csosn"])
  print("Response CARRINHO origem_icms___________________________:",carrinho[0]["origem_icms"])
  print("Response CARRINHO origem_icms___________________________:",carrinho[0]["preco_unitario"])
  print("Response CARRINHO origem_icms___________________________:",carrinho[0]["quantidade"])
  
  
  
  
  uf = 'sp'

  certificado = os.path.abspath(os.path.join(script_dir, "..", "..", "certificados_digitais_emitentes", f"{certificado}.pfx"))

  #homologacao = True

  if response_emitente.json().get("env") == True:
    homologacao = True #Altere para True se for homologação
  elif response_emitente.json().get("env") == False:
    homologacao = False #Altere para False se for produção


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
    forma_pagamento=0, 
    tipo_pagamento = forma_pagamento_codigo,        # 0=Pagamento à vista; 1=Pagamento a prazo; 2=Outros.
    #tipo_pagamento=1,
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
    #totais_tributos_aproximado=Decimal('10.06'),
    #totais_tributos_aproximado=Decimal(valor_tributos_aprox),
    totais_tributos_aproximado=Decimal('0.00'),
    #totais_tributos_aproximado=Decimal(valor_tributos_aprox),
  )


  # Produto
  #valor_bruto_total = 0.00
  #valor_tributos_aprox_total = 0.00
  valor_bruto_total = Decimal('0.00')        # alterado para Decimal
  valor_tributos_aprox_total = Decimal('0.00') # alterado para Decimal
  nItem = 1

  for produto in carrinho:
    print(produto)
  

    quantidade_prod = Decimal(str(produto["quantidade"]))
    preco_unit_prod = Decimal(str(produto["preco_unitario"]))
    valor_tributos_aprox_porcent = Decimal(str(produto["valor_tributos_aprox"]))


    #valor_bruto = (produto["quantidade"] * produto["preco_unitario"])
    valor_bruto = (quantidade_prod * preco_unit_prod).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)  # <-- ARREDONDAMENTO AQUI
    
    #valor_final =  (quantidade*produto_selecionado["preco_unitario"])
    valor_final = (Decimal(str(quantidade)) * Decimal(str(produto_selecionado["preco_unitario"]))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)  # <-- ARREDONDAMENTO AQUI



    #valor_tributos_aprox = round(valor_bruto*produto["valor_tributos_aprox"],2)
    valor_tributos_aprox = (valor_bruto * valor_tributos_aprox_porcent).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)  # <-- ARREDONDAMENTO AQUI
    
    #valor_total_unit = (produto["quantidade"] * produto["preco_unitario"])
    valor_total_unit = (quantidade_prod * preco_unit_prod).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)  # <-- ARREDONDAMENTO AQUI

    valor_bruto_total += valor_bruto
    valor_tributos_aprox_total += valor_tributos_aprox

    print("Response preco_unitario:", produto_selecionado["preco_unitario"] ,"tipo", type(produto_selecionado["preco_unitario"] ))
    print("Response QUANTIDADE___________________________:",quantidade,"tipo", type(quantidade))
    print("Response VALOR TOTAL___________________________:",valor_total,"tipo", type(valor_total))
    #print("Response VALOR BRUTO___________________________:",valor_bruto, "tipo", type(valor_bruto))
    print("Response VALOR BRUTO___________________________:", valor_bruto)
    #print("Response VALOR FINAL___________________________:",valor_final,"tipo", type(valor_final))
    print("Response VALOR FINAL___________________________:", valor_final)
    #print("Response valor_tributos_aprox___________________________:",valor_tributos_aprox,"tipo", type(valor_final))
    print("Response valor_tributos_aprox___________________________:", valor_tributos_aprox)
    print("Response VALOR BRUTO___________________________:",valor_bruto)
    print("Response VALOR FINAL___________________________:",valor_final)
    print("Response VALOR UNIT___________________________:",valor_total_unit)

      
    
    
    


    nota_fiscal.adicionar_produto_servico(
        #codigo='000328',                           # id do produto
        codigo=produto["codigo"],
        #descricao='NOTA FISCAL EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL',
        #descricao=produtos_nome,
        descricao=produto["descricao"],
        #ncm='21069090',
        ncm=produto["ncm"],
        #cest='0100100',                            # NT2015/003
        #cest=produto["cest"],
        #cfop='5102',
        cfop=produto["cfop"],
        #unidade_comercial='UN',
        unidade_comercial=produto["unidade_tributavel"],
        ean='SEM GTIN',
        ean_tributavel='SEM GTIN',
        #quantidade_comercial=Decimal(quantidade),
        #quantidade_comercial=Decimal(produto["quantidade"]),
        quantidade_comercial=quantidade_prod,
        #quantidade_comercial=Decimal('12'),        # 12 unidades
        #valor_unitario_comercial=Decimal('9.75'),
        #valor_unitario_comercial=Decimal(valor_total),  # preço unitário
        #valor_unitario_comercial=Decimal(produto["preco_unitario"]),  ###### preço unitário
        valor_unitario_comercial=preco_unit_prod,
        #valor_total_bruto=Decimal('117.00'), 
        valor_total_bruto=valor_bruto,
        #valor_total_bruto = Decimal(valor_bruto),      # preço total
        #unidade_tributavel='UN',
        unidade_tributavel=produto["unidade_tributavel"],
        #quantidade_tributavel=Decimal(quantidade),
        #quantidade_tributavel=Decimal(produto["quantidade"]),
        quantidade_tributavel=quantidade_prod,
        #valor_unitario_tributavel=Decimal(valor_total),################
        #valor_unitario_tributavel=Decimal(produto_selecionado["preco_unitario"] ),
        valor_unitario_tributavel=Decimal(produto["preco_unitario"]),
        #quantidade_tributavel=Decimal('12'),
        #valor_unitario_tributavel=Decimal('9.75'),
        ind_total=1,
        # numero_pedido='12345',                   # xPed
        # numero_item='123456',                    # nItemPed
        icms_modalidade='102', # 101	Tributada com permissão de crédito  102	Tributada sem permissão de crédito 103	Isenção do ICMS   201	Tributada com permissão de crédito e com cobrança do ICMS por Substituição Tributária (ST)  202	Tributada sem permissão de crédito e com cobrança do ICMS por ST   203	Isenção do ICMS e com cobrança do ICMS por ST  300	Imune  400	Não tributada pelo Simples Nacional  500	ICMS cobrado anteriormente por substituição tributária (ST) ou por antecipação   900	Outros
        #icms_modalidade='102',
        #icms_origem=0,  # 0	Nacional – exceto as indicadas nos códigos 3, 4, 5 e 8 -- 1	Estrangeira – Importação direta --2	Estrangeira – Adquirida no mercado interno ---3	Nacional – com conteúdo de importação superior a 40%    ----4	Nacional – produzida com processo básico da ZFM  ----   5	Nacional – com conteúdo de importação inferior a 40%   ---- 6	Estrangeira – Importação direta sem similar nacional ---- 7	Estrangeira – Adquirida no mercado interno sem similar nacional   --- 8	Nacional – conteúdo de importação entre 70% e 100%
        icms_origem=produto["origem_icms"],
        #icms_csosn='400', # ("101", "Tributada pelo Simples Nacional com permissão de crédito"),("102", "Tributada pelo Simples Nacional sem permissão de crédito"), ("103", "Isenção do ICMS no Simples Nacional para faixa de receita bruta"),("201", "Tributada pelo Simples Nacional com permissão de crédito e com cobrança do ICMS por substituição tributária"),("202", "Tributada pelo Simples Nacional sem permissão de crédito e com cobrança do ICMS por substituição tributária"),("203", "Isenção do ICMS no Simples Nacional para faixa de receita bruta e com cobrança do ICMS por substituição tributária"),("300", "Imune"),("400", "Não tributada pelo Simples Nacional"),("500", "ICMS cobrado anteriormente por substituição tributária (substituído) ou por antecipação"),("900", "Outros")
        icms_csosn=produto["csosn"],
        #pis_modalidade='07', # ("01", "Margem Valor Agregado (%)"), ("02", "Pauta (valor)"), ("03", "Preço Tabelado Máx. (valor)"), ("04", "Valor da operação"),  ("05", "Operação Tributável (alíquota diferenciada)"), ("06", "Outros"), ("07", "Operação Isenta da Contribuição"),("08", "Operação sem Incidência da Contribuição"), ("09", "Operação com Suspensão da Contribuição")
        pis_modalidade=produto["pis_modalidade"],
        #cofins_modalidade='07', # # ("01", "Margem Valor Agregado (%)"), ("02", "Pauta (valor)"), ("03", "Preço Tabelado Máx. (valor)"), ("04", "Valor da operação"),  ("05", "Operação Tributável (alíquota diferenciada)"), ("06", "Outros"), ("07", "Operação Isenta da Contribuição"),("08", "Operação sem Incidência da Contribuição"), ("09", "Operação com Suspensão da Contribuição")
        cofins_modalidade=produto["cofins_modalidade"],
        #valor_tributos_aprox='10.06'
        #valor_tributos_aprox= str(valor_tributos_aprox)
        valor_tributos_aprox=str(valor_tributos_aprox),  # mantendo string pois parece ser esperado assim
        #valor_tributos_aprox=Decimal(valor_tributos_aprox)
        )
    nItem += 1
  #nota_fiscal.totais_tributos_aproximado = valor_tributos_aprox_total
  nota_fiscal.totais_tributos_aproximado = valor_tributos_aprox_total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)  # <-- ARREDONDAMENTO AQUI



    

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

  if response_emitente.json().get("env") == True:
    # csc de homologação
    csc = response_emitente.json().get("cod_seguranca")
  elif response_emitente.json().get("env") == False:
    # csc de produção
    csc = response_emitente.json().get("cod_seguranca_prod")
  #csc=response_emitente.json().get("cod_seguranca")

  # gera e adiciona o qrcode no xml NT2015/003
  xml_com_qrcode = SerializacaoQrcode().gerar_qrcode(token, csc, xml)

  # envio
  con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
  envio = con.autorizacao(modelo='nfce', nota_fiscal=xml_com_qrcode)

  # em caso de sucesso o retorno será o xml autorizado
  # Ps: no modo sincrono, o retorno será o xml completo (<nfeProc> = <NFe> + <protNFe>)
  # no modo async é preciso montar o nfeProc, juntando o retorno com a NFe  
 
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
    print('RESPOSTA XML_________________________',resposta_xml)
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
    print(envio[1].text)  # resposta
    print('Nota:')
    print(etree.tostring(envio[2], encoding="unicode"))  # nfe
    nfe_tree = etree.ElementTree(envio[2])  # Cria a árvore a partir do XML da NF-e
    print(etree.tostring(nfe_tree.getroot(), encoding="unicode", pretty_print=True))  # Exibe o XML em formato de árvore

    return {
        "status": "erro"
    }




###########################MAIN######################


#call_pedido()