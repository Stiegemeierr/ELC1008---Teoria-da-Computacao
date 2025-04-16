def verificar_labirinto(fita: str) -> bool:
    fita = list(fita)
    try:
        pos = fita.index('S')
    except ValueError:
        print("Erro: ponto de partida 'S' não encontrado.")
        return False

    visitado = set()

    def mover(pos):
        if pos < 0 or pos >= len(fita):
            return False
        if fita[pos] == '*':
            return False
        if fita[pos] == 'E':
            return True
        if pos in visitado:
            return False

        visitado.add(pos)

        return mover(pos + 1) or mover(pos - 1)

    return mover(pos)


labirintos = [
    "S  *  E",
    "S**  E",
    "*S  * E*",
    "*S    E*"
]

for i, labirinto in enumerate(labirintos, 1):
    resultado = verificar_labirinto(labirinto)
    print(f"Labirinto {i}: '{labirinto}' -> {resultado}")