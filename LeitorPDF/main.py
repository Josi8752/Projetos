from extratores.extrator_padrao import extrair_dados_pdf
import os

# Caminho do arquivo PDF de entrada
caminho_pdf = os.path.join("arquivos", "exemplo.pdf")

# Caminho do Excel de saída
caminho_saida = os.path.join("resultados", "dados_organizados.xlsx")

# Executa a extração
extrair_dados_pdf(caminho_pdf, caminho_saida)
