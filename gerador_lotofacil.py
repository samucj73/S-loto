import random

def gerar_cartoes_personalizados(fixas, excluir, qtd, ultimos):
    cartoes = []
    universo = [i for i in range(1, 26) if i not in excluir]
    while len(cartoes) < qtd:
        restante = list(set(universo) - set(fixas))
        dezenas = sorted(random.sample(restante, 15 - len(fixas)) + fixas)
        if dezenas not in cartoes:
            cartoes.append(dezenas)
    return cartoes