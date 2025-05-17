import requests

def capturar_ultimos_resultados(qtd=10):
    url_base = "https://loteriascaixa-api.herokuapp.com/api/lotofacil/"
    concursos = []

    try:
        # Buscar o último concurso
        resp = requests.get(url_base)
        if resp.status_code != 200:
            print("Erro ao buscar o último concurso.")
            return []

        ultimo = resp.json()
        numero_atual = int(ultimo.get("concurso"))
        dezenas = sorted([int(d) for d in ultimo.get("dezenas")])
        concursos.append((numero_atual, dezenas))

        # Buscar concursos anteriores
        for i in range(1, qtd):
            concurso_numero = numero_atual - i
            resp = requests.get(f"{url_base}{concurso_numero}")
            if resp.status_code == 200:
                data = resp.json()
                numero = int(data.get("concurso"))
                dezenas = sorted([int(d) for d in data.get("dezenas")])
                concursos.append((numero, dezenas))
            else:
                print(f"Concurso {concurso_numero} não encontrado ou erro na API.")
                break

    except Exception as e:
        print("Erro ao acessar API:", e)

    return concursos
