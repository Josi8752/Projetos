import pandas as pd
from PyPDF2 import PdfReader
import re
import tkinter as tk
from tkinter import filedialog

def selecionar_pdf():
    root = tk.Tk()
    root.withdraw()
    caminho = filedialog.askopenfilename(
        title="Selecione o arquivo PDF",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    return caminho

def extrair_dados_pdf(caminho_pdf, caminho_saida_excel):
    reader = PdfReader(caminho_pdf)
    linhas = []
    for page in reader.pages:
        texto_pagina = page.extract_text()
        if texto_pagina:
            for linha in texto_pagina.splitlines():
                linha = linha.strip()
                if linha:
                    linhas.append(linha)

    # Padrões
    padrao_unidade_bloco = re.compile(r"(\d{3})\s+BLOCO\s+([A-Z])", re.IGNORECASE)
    padrao_cpf_cnpj = re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b|\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b")
    padrao_telefone = re.compile(r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}")
    padrao_email = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
    padrao_endereco = re.compile(r"(Rua|Av\.|Avenida|Alameda|Travessa|Estrada|Rodovia).*", re.IGNORECASE)
    padrao_fracao = re.compile(r"^\d+[.,]?\d*$")
    tipos_possiveis = ["proprietário", "dependente", "inquilino", "residente", "procurador"]

    dados = []
    registro = {col: "" for col in ['Unidade', 'Bloco', 'Nome', 'Telefone', 'Tipo', 'Endereço', 'CPF/CNPJ', 'E-mail', 'Fração Ideal']}

    def salvar_registro():
        if registro["Unidade"] and registro["Nome"]:
            dados.append(registro.copy())

    for linha in linhas:
        # Nova unidade detectada
        match_unidade = padrao_unidade_bloco.search(linha)
        if match_unidade:
            salvar_registro()
            registro = {col: "" for col in registro}
            registro["Unidade"] = match_unidade.group(1)
            registro["Bloco"] = f"BLOCO {match_unidade.group(2)}"
            continue

        # Nome (primeiro campo que não for telefone, cpf, e-mail, endereço, tipo ou fração)
        if not registro["Nome"]:
            if not padrao_cpf_cnpj.search(linha) and not padrao_telefone.search(linha) \
               and not padrao_email.search(linha) and not padrao_endereco.search(linha) \
               and not any(tp in linha.lower() for tp in tipos_possiveis) \
               and not padrao_fracao.search(linha):
                registro["Nome"] = linha
                continue

        # Tipo
        for tp in tipos_possiveis:
            if tp in linha.lower():
                registro["Tipo"] = tp.capitalize()
                break

        # Telefone
        if not registro["Telefone"]:
            match_tel = padrao_telefone.search(linha)
            if match_tel:
                registro["Telefone"] = match_tel.group()
                continue

        # CPF/CNPJ
        if not registro["CPF/CNPJ"]:
            match_cpf = padrao_cpf_cnpj.search(linha)
            if match_cpf:
                registro["CPF/CNPJ"] = match_cpf.group()
                continue

        # E-mail
        if not registro["E-mail"]:
            match_email = padrao_email.search(linha)
            if match_email:
                registro["E-mail"] = match_email.group()
                continue

        # Endereço
        if not registro["Endereço"]:
            if padrao_endereco.search(linha):
                registro["Endereço"] = linha
                continue

        # Fração Ideal
        if not registro["Fração Ideal"]:
            match_fracao = padrao_fracao.search(linha)
            if match_fracao:
                registro["Fração Ideal"] = match_fracao.group()
                continue

    salvar_registro()

    df = pd.DataFrame(dados)
    df.to_excel(caminho_saida_excel, index=False)
    print(f"[✔] Planilha gerada: {caminho_saida_excel}")

if __name__ == "__main__":
    caminho_pdf = selecionar_pdf()
    if caminho_pdf:
        extrair_dados_pdf(caminho_pdf, "dados_organizados.xlsx")
    else:
        print("Nenhum arquivo selecionado.")
