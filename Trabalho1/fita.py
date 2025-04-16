class Fita:
    def __init__(self, conteudo: str):
        self.fita = list(conteudo) + ['B'] * 100
        self.cabeca = 0

    def ler(self):
        return self.fita[self.cabeca]

    def escrever(self, simbolo: str):
        self.fita[self.cabeca] = simbolo

    def mover(self, direcao: str):
        if direcao == 'R':
            self.cabeca += 1
        elif direcao == 'L':
            self.cabeca -= 1

    def imprimir(self, nome: str, tamanho: int = 20) -> None:
        conteudo = ' '.join(self.fita[:tamanho])
        print(f"{nome:<18}: {conteudo}")