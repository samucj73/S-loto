from collections import Counter
from itertools import combinations

def dezenas_mais_sorteadas(resultados):
    contagem = Counter(num for jogo in resultados for num in jogo)
    return contagem.most_common(10)

def dezenas_menos_sorteadas(resultados):
    contagem = Counter(num for jogo in resultados for num in jogo)
    return contagem.most_common()[-10:]

def trincas_mais_frequentes(resultados):
    trincas = Counter()
    for jogo in resultados:
        for trio in combinations(sorted(jogo), 3):
            trincas[trio] += 1
    return trincas.most_common(5)

def linhas_mais_frequentes(resultados):
    contagem = Counter()
    for jogo in resultados:
        linhas = [0]*5
        for num in jogo:
            linha = (num - 1) // 5
            linhas[linha] += 1
        for i, q in enumerate(linhas, 1):
            contagem[f"Linha {i}"] += q
    return contagem.most_common(5)

def colunas_mais_frequentes(resultados):
    contagem = Counter()
    for jogo in resultados:
        colunas = [0]*5
        for num in jogo:
            coluna = (num - 1) % 5
            colunas[coluna] += 1
        for i, q in enumerate(colunas, 1):
            contagem[f"Coluna {i}"] += q
    return contagem.most_common(5)

def faixas_mais_frequentes(resultados):
    faixas = {"1-5":0, "6-10":0, "11-15":0, "16-20":0, "21-25":0}
    for jogo in resultados:
        for n in jogo:
            if 1 <= n <= 5:
                faixas["1-5"] += 1
            elif 6 <= n <= 10:
                faixas["6-10"] += 1
            elif 11 <= n <= 15:
                faixas["11-15"] += 1
            elif 16 <= n <= 20:
                faixas["16-20"] += 1
            elif 21 <= n <= 25:
                faixas["21-25"] += 1
    return sorted(faixas.items(), key=lambda x: x[1], reverse=True)

def primos_por_concurso(resultados):
    primos = {2, 3, 5, 7, 11, 13, 17, 19, 23}
    return [sum(1 for n in jogo if n in primos) for jogo in resultados]

def dezenas_atrasadas(resultados):
    todas = set(range(1, 26))
    ultima_ocorrencia = {n: None for n in todas}
    for i, jogo in enumerate(reversed(resultados)):
        for n in jogo:
            if ultima_ocorrencia[n] is None:
                ultima_ocorrencia[n] = i
    atrasadas = [(n, ultima_ocorrencia[n] if ultima_ocorrencia[n] is not None else len(resultados)) for n in todas]
    return sorted(atrasadas, key=lambda x: x[1], reverse=True)[:10]