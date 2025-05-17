import requests

def capturar_ultimos_resultados(qtd=10):
    url_base = "https://loteriascaixa-api.herokuapp.com/api/lotofacil/"
    concursos = []

    try:
        # Primeiro busca o último concurso
        resp = requests.get(url_base)
        if resp.status_code != 200:
            print("Erro ao buscar o último concurso")
            return []

        ultimo = resp.json()
        numero_atual = int(ultimo.get("concurso"))
        concursos.append((numero_atual, [int(d) for d in ultimo.get("dezenas")]))

        # Agora busca os concursos anteriores
        for i in range(1, qtd):
            resp = requests.get(url_base + str(numero_atual - i))
            if resp.status_code == 200:
                data = resp.json()
                concursos.append((data.get("concurso"), [int(d) for d in data.get("dezenas")]))
            else:
                break
    except Exception as e:
        print("Erro ao acessar API:", e)

    return concursos
