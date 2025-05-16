import os
from reportlab.pdfgen import canvas

def exportar_txt(cartoes, nome_arquivo="cartoes.txt"):
    with open(nome_arquivo, "w") as f:
        for i, cartao in enumerate(cartoes, 1):
            f.write(f"Cartão {i}: {' - '.join(f'{d:02}' for d in sorted(cartao))}\n")
    return os.path.abspath(nome_arquivo)

def exportar_pdf(cartoes, nome_arquivo="cartoes.pdf"):
    c = canvas.Canvas(nome_arquivo)
    y = 800
    for i, cartao in enumerate(cartoes, 1):
        texto = f"Cartão {i}: {' - '.join(f'{d:02}' for d in sorted(cartao))}"
        c.drawString(50, y, texto)
        y -= 20
        if y < 50:
            c.showPage()
            y = 800
    c.save()
    return os.path.abspath(nome_arquivo)