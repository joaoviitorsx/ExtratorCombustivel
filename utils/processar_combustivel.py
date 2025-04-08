import os
import re
from PySide6.QtWidgets import QFileDialog, QMessageBox
from utils.extrator_xml import extrair_dados_de_xmls
from utils.filtro_combustivel import filtrar_diesel, filtrar_gasolina
from utils.exportador_excel import exportar_para_excel
from utils.mensagem import mensagem_aviso, mensagem_sucesso, mensagem_error
from utils.filtro_pneu import filtrar_pneu

def selecionar_e_processar_pasta(progresso_callback=None):
    pasta = QFileDialog.getExistingDirectory(None, "Selecione a pasta com arquivos XML")
    if not pasta:
        if progresso_callback:
            progresso_callback(0)
        return

    if progresso_callback:
        progresso_callback(10)

    # Coletar arquivos
    arquivos_xml = sorted([
        os.path.join(pasta, f) for f in os.listdir(pasta)
        if f.endswith(".xml")
    ])

    if not arquivos_xml:
        mensagem_aviso("Nenhum arquivo XML encontrado na pasta.")
        if progresso_callback:
            progresso_callback(0)
        return

    # Etapa 1: Extração
    df_geral, erros, resumo = extrair_dados_de_xmls(arquivos_xml)

    if progresso_callback:
        progresso_callback(60)

    # Etapa 2: Filtros
    df_diesel = filtrar_diesel(df_geral)
    df_gasolina = filtrar_gasolina(df_geral)
    df_pneu = filtrar_pneu(df_geral)

    if progresso_callback:
        progresso_callback(80)

    resumo_msg = (
        f"Resumo do processamento:\n\n"
        f"📄 Total de XMLs encontrados: {resumo['total_xmls']}\n"
        f"✅ Arquivos lidos com sucesso: {resumo['sucesso']}\n"
        f"⚠️ Arquivos com erro: {resumo['falha']}\n"
        f"🔁 Duplicatas ignoradas: {resumo['duplicatas']}"
    )
    mensagem_aviso(resumo_msg)

    # Etapa 3: Exportação
    caminho_excel, _ = QFileDialog.getSaveFileName(None, "Salvar arquivo Excel", pasta, "Excel Files (*.xlsx)")
    if not caminho_excel:
        if progresso_callback:
            progresso_callback(0)
        return

    exportar_para_excel(df_geral, df_diesel, df_gasolina,df_pneu, caminho_excel)

    if progresso_callback:
        progresso_callback(100)

    mensagem_sucesso("Exportação concluída com sucesso!")

    abrir_arquivo = QMessageBox.question(
        None, "Abrir Arquivo", "Deseja abrir o arquivo gerado?",
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No
    )
    if abrir_arquivo == QMessageBox.Yes:
        progresso_callback(0)
        os.startfile(caminho_excel)

    # Exibir erros, se houver
    if erros:
        print("Alguns arquivos apresentaram falhas:")
        for arq, motivo in erros:
            print(f"Arquivo: {arq}\nMotivo: {motivo}\n")

