import os
from typing import List, Tuple, Optional

def transformar_mt_para_reversivel(quintuplas: List[Tuple[str, str, str, str, str]]) -> List[str]:
    """
    Cada quintupla é transformada em duas quádruplas:
    1. A primeira preserva o símbolo lido e grava o símbolo escrito (sem movimento)
    2. A segunda grava o histórico (movimento + número da transição) e realiza o movimento
    """
    saida = []
    for i, (estado, lido, escrito, mov, novo_estado) in enumerate(quintuplas):
        # Gera um estado intermediário único para cada transição
        estado_intermediario = f"{estado}'"
        m = i + 1  # número da transição, para fita 2

        # Quádrupla 1: lê e escreve (sem mover)
        quad_1 = f"{estado} [{lido} / /] -> [{escrito} / /] {estado_intermediario}"

        # Quádrupla 2: grava histórico e move
        quad_2 = f"{estado_intermediario} [/ b /] -> [{mov} {m} 0] {novo_estado}"

        saida.append(quad_1)
        saida.append(quad_2)
    
    return saida

def ler_quintuplas(caminho_arquivo: str) -> List[Tuple[str, str, str, str, str]]:
    with open(caminho_arquivo, 'r') as f:
        linhas = [linha.strip() for linha in f if linha.strip()]
    
    quintuplas = []
    for linha in linhas:
        partes = linha.split()
        if len(partes) != 5:
            print(f"Formato inválido: {linha}")
            continue
        estado, lido, escrito, mov, novo_estado = partes
        quintuplas.append((estado, lido, escrito, mov, novo_estado))
    
    return quintuplas

def gravar_resultado(caminho_arquivo: str, quadruplas: List[str]) -> None:
    with open(caminho_arquivo, 'w') as f:
        for linha in quadruplas:
            f.write(linha + '\n')

def transformar_quintuplas_em_reversivel(entrada_txt: str, saida_txt: str) -> None:
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_entrada = os.path.join(diretorio_atual, entrada_txt)
    caminho_saida = os.path.join(diretorio_atual, saida_txt)
    
    quintuplas = ler_quintuplas(caminho_entrada)
    quadruplas = transformar_mt_para_reversivel(quintuplas)
    
    gravar_resultado(caminho_saida, quadruplas)
    print(f"Transformação concluída! Saída salva em '{saida_txt}'.")

"""
O arquivo de entrada(input) deve conter quintuplas no seguinte formato:
<estado> <símbolo_lido> <símbolo_escrito> <movimento> <novo_estado>
cada campo deve ser separado por espaço
apenas 1 test case por arquivo
"""

if __name__ == "__main__":
    transformar_quintuplas_em_reversivel("input.txt", "output.txt")



