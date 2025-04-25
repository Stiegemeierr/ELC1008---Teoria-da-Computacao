import os
from typing import List, Tuple, Optional

from fita import Fita


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

    # Ignora os metadados e pega apenas as transições
    transicoes = linhas[4:-1]  # Última linha é a entrada (ex: "0011")
    entrada = linhas[-1].strip()

    quintuplas = []

    for linha in transicoes:
        # Esperado: (estado,símbolo)=(novo_estado,símbolo_escrito,direção)
        if '(' in linha and ')' in linha and '=' in linha:
            lado_esq, lado_dir = linha.split('=')

            # Remove parênteses
            lado_esq = lado_esq.strip()[1:-1]   # tira os parênteses
            lado_dir = lado_dir.strip()[1:-1]

            # Divide pelos valores
            partes_esq = lado_esq.split(',')
            partes_dir = lado_dir.split(',')

            if len(partes_esq) == 2 and len(partes_dir) == 3:
                estado = partes_esq[0].strip()
                lido = partes_esq[1].strip()
                novo_estado = partes_dir[0].strip()
                escrito = partes_dir[1].strip()
                mov = partes_dir[2].strip()

                quintuplas.append((estado, lido, escrito, mov, novo_estado))
            else:
                print(f"Formato inválido: {linha}")
        else:
            print(f"Formato inválido: {linha}")
    
    return quintuplas, entrada


def gravar_resultado(caminho_arquivo: str, quadruplas: List[str]) -> None:
    with open(caminho_arquivo, 'w') as f:
        for linha in quadruplas:
            f.write(linha + '\n')


def transformar_quintuplas_em_reversivel(entrada_txt: str, saida_txt: str) -> None:
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_entrada = os.path.join(diretorio_atual, entrada_txt)
    caminho_saida = os.path.join(diretorio_atual, saida_txt)
    
    quintuplas, entrada = ler_quintuplas(caminho_entrada)
    quadruplas = transformar_mt_para_reversivel(quintuplas)
    
    gravar_resultado(caminho_saida, quadruplas)
    print(f"Transformação concluída! Saída salva em '{saida_txt}'.")

    return quadruplas, entrada


def imprimir_fita(nome: str, fita: Fita, tamanho: int = 20):
    conteudo = ' '.join(fita.fita[:tamanho])
    print(f"{nome:<18}: {conteudo}")


def main():
    entrada_txt = "input.txt" 
    saida_txt = "output.txt"
    
    quadruplas, entrada = transformar_quintuplas_em_reversivel(entrada_txt, saida_txt)

    fita1 = Fita(entrada)
    fita2 = Fita("")
    fita3 = Fita("")

    fita1.imprimir("Fita 1 (entrada)")
    fita2.imprimir("Fita 2 (histórico)")
    fita3.imprimir("Fita 3 (saída)")


if __name__ == "__main__":
    main()