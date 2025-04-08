import xmltodict
import pandas as pd
import os
import re
import xml.parsers.expat

def extrair_dados_de_xmls(lista_de_arquivos):
    colunas = [
        "Nome Cliente", "CNPJ Cliente", "Fornecedor", "CNPJ Fornecedor", "Inscrição Estadual", "Número Nota",
        "Série", "Data Emissão", "Data Saída/Entrada", "Chave NF", "Número Item", "Código Produto", "EAN",
        "Descrição", "NCM", "CFOP", "Quantidade", "Valor Unitário", "Valor Frete", "Valor Seguro",
        "Valor Desconto", "Valor Outros", "Valor Produto", "EAN Tributado", "Unidade Tributada",
        "Quantidade Tributada", "Valor Unitário Tributado", "CSOSN", "Indicador Total",
        "ICMS Origem", "ICMS CST", "ICMS Mod BC", "ICMS VBC", "ICMS PICMS", "ICMS Valor",
        "IPI CST", "IPI VBC", "IPI PIPI", "IPI VIPI",
        "PIS CST", "PIS VBC", "PIS PPIS", "PIS VPIS",
        "COFINS CST", "COFINS VBC", "COFINS PCOFINS", "COFINS VCOFINS"
    ]

    valores = []
    erros = []
    arquivos_processados = set()
    sucesso = 0
    falha = 0
    duplicatas = 0

    for arquivo in lista_de_arquivos:
        try:
            nome_base = os.path.basename(arquivo).replace(".xml", "")
            nome_limpo = re.sub(r"\s\d+$", "", nome_base)

            if nome_limpo in arquivos_processados:
                duplicatas += 1
                continue
            arquivos_processados.add(nome_limpo)

            with open(arquivo, "rb") as f:
                dic_arquivo = xmltodict.parse(f, process_namespaces=False)
                infos_nf = dic_arquivo.get('nfeProc', {}).get('NFe', {}).get('infNFe', {})

                if not infos_nf:
                    raise ValueError("Estrutura do XML inválida ou não é uma NF-e válida.")

                produtos = infos_nf.get('det', [])
                if not isinstance(produtos, list):
                    produtos = [produtos]

                for produto in produtos:
                    try:
                        # Verificar CSOSN
                        regime_tributario = infos_nf.get('emit', {}).get('CRT', ' - ')
                        csosn = " - "
                        if regime_tributario in ['1', '2']:
                            icms = produto.get('imposto', {}).get('ICMS', {})
                            if isinstance(icms, dict):
                                for chave, valor in icms.items():
                                    if isinstance(valor, dict):
                                        csosn = valor.get('CSOSN', ' - ')
                                        break

                        linha = [
                            infos_nf.get('dest', {}).get('xNome', ' - '),
                            infos_nf.get('dest', {}).get('CNPJ', ' - '),
                            infos_nf.get('emit', {}).get('xNome', ' - '),
                            infos_nf.get('emit', {}).get('CNPJ', ' - '),
                            infos_nf.get('emit', {}).get('IE', ' - '),
                            infos_nf.get('ide', {}).get('nNF', ' - '),
                            infos_nf.get('ide', {}).get('serie', ' - '),
                            infos_nf.get('ide', {}).get('dhEmi', ' - ').split("T")[0],
                            infos_nf.get('ide', {}).get('dhSaiEnt', ' - '),
                            infos_nf.get('@Id', ' - '),
                            produto.get('@nItem', ' - '),
                            produto.get('prod', {}).get('cProd', ' - '),
                            produto.get('prod', {}).get('cEAN', ' - '),
                            produto.get('prod', {}).get('xProd', ' - '),
                            produto.get('prod', {}).get('NCM', ' - '),
                            produto.get('prod', {}).get('CFOP', ' - '),
                            produto.get('prod', {}).get('qCom', ' - '),
                            produto.get('prod', {}).get('vUnCom', ' - '),
                            produto.get('prod', {}).get('vFrete', ' - '),
                            produto.get('prod', {}).get('vSeg', ' - '),
                            produto.get('prod', {}).get('vDesc', ' - '),
                            produto.get('prod', {}).get('vOutro', ' - '),
                            produto.get('prod', {}).get('vProd', ' - '),
                            produto.get('prod', {}).get('cEANTrib', ' - '),
                            produto.get('prod', {}).get('uTrib', ' - '),
                            produto.get('prod', {}).get('qTrib', ' - '),
                            produto.get('prod', {}).get('vUnTrib', ' - '),
                            csosn,
                            produto.get('prod', {}).get('indTot', ' - ')
                        ]

                        for imposto in ['ICMS', 'IPI', 'PIS', 'COFINS']:
                            imposto_data = produto.get('imposto', {}).get(imposto, {})
                            if isinstance(imposto_data, dict):
                                for _, valor in imposto_data.items():
                                    if isinstance(valor, dict):
                                        if imposto == "ICMS":
                                            linha.extend([
                                                valor.get('orig', ' - '),
                                                valor.get('CST', ' - '),
                                                valor.get('modBC', ' - '),
                                                valor.get('vBC', ' - '),
                                                valor.get('pICMS', ' - '),
                                                valor.get('vICMS', ' - ')
                                            ])
                                        else:
                                            linha.extend([
                                                valor.get('CST', ' - '),
                                                valor.get('vBC', ' - '),
                                                valor.get(f'p{imposto}', ' - '),
                                                valor.get(f'v{imposto}', ' - ')
                                            ])
                                        break
                        sucesso += 1
                        valores.append(linha)

                    except Exception as e:
                        erros.append((arquivo, f"Erro ao processar item: {str(e)}"))
                        falha += 1

        except xml.parsers.expat.ExpatError as e:
            erros.append((arquivo, f"Erro XML: {str(e)}"))
            falha += 1
        except Exception as e:
            erros.append((arquivo, f"Erro geral: {str(e)}"))

    df = pd.DataFrame(columns=colunas, data=valores)

    resumo = {
        "total_xmls": len(lista_de_arquivos),
        "sucesso": sucesso,
        "falha": falha,
        "duplicatas": duplicatas,
    }
    
    return df, erros, resumo
