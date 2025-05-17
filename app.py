import streamlit as st
from api_lotofacil import capturar_ultimos_resultados
from lotofacil_estatisticas import (
    dezenas_mais_sorteadas,
    dezenas_menos_sorteadas,
    trincas_mais_frequentes,
    linhas_mais_frequentes,
    colunas_mais_frequentes,
    faixas_mais_frequentes,
    primos_por_concurso,
    dezenas_atrasadas
)
from util import exportar_txt, exportar_pdf
from gerador_lotofacil import gerar_cartoes_personalizados

st.set_page_config(page_title="LotoFácil Inteligente", layout="wide")
st.markdown("<h1 style='text-align: center;'>🍀 LotoFácil Inteligente</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Gere cartões com base em estatísticas reais e personalização</p>", unsafe_allow_html=True)

resultados = [r[1] for r in capturar_ultimos_resultados(10)]

aba = st.tabs(["🎯 Geração de Cartões", "📊 Estatísticas", "🗓 Últimos Resultados", "📤 Exportação"])

with aba[0]:
    st.header("🎯 Geração de Cartões Inteligentes")
    qtd_cartoes = st.slider("Quantos cartões deseja gerar?", 1, 100, 5)
    fixas = st.multiselect("Escolha até 7 dezenas fixas:", list(range(1, 26)))
    excluir = st.multiselect("Deseja excluir até 5 dezenas?", [i for i in range(1, 26) if i not in fixas])

    if len(fixas) > 7:
        st.warning("Máximo de 7 dezenas fixas permitidas.")
    elif len(excluir) > 5:
        st.warning("Máximo de 5 dezenas para excluir.")
    elif st.button("🔁 Gerar Cartões"):
        cartoes = gerar_cartoes_personalizados(fixas, excluir, qtd_cartoes, resultados)
        for i, cartao in enumerate(cartoes, 1):
            st.success(f"Cartão {i}: {' - '.join(f'{n:02}' for n in sorted(cartao))}")
        st.session_state['cartoes'] = cartoes

with aba[1]:
    st.header("📊 Estatísticas dos Últimos 10 Concursos")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🔢 Mais Sorteadas")
        for dez, freq in dezenas_mais_sorteadas(resultados):
            st.write(f"{dez:02}: {freq}x")

        st.subheader("📉 Menos Sorteadas")
        for dez, freq in dezenas_menos_sorteadas(resultados):
            st.write(f"{dez:02}: {freq}x")

        st.subheader("🎯 Atrasadas")
        for dez, atraso in dezenas_atrasadas(resultados):
            st.write(f"{dez:02}: {atraso} concursos")

    with col2:
        st.subheader("🔀 Trincas Frequentes")
        for trio, freq in trincas_mais_frequentes(resultados):
            st.write(f"{trio}: {freq}x")

        st.subheader("📌 Faixas Frequentes")
        for faixa, freq in faixas_mais_frequentes(resultados):
            st.write(f"{faixa}: {freq}x")

    with col3:
        st.subheader("📍 Linhas Frequentes")
        for linha, freq in linhas_mais_frequentes(resultados):
            st.write(f"{linha}: {freq}x")

        st.subheader("📍 Colunas Frequentes")
        for col, freq in colunas_mais_frequentes(resultados):
            st.write(f"{col}: {freq}x")

        st.subheader("🧮 Primos por Concurso")
        primos = primos_por_concurso(resultados)
        for i, p in enumerate(primos, 1):
            st.write(f"Concurso {-i}: {p} primos")

with aba[2]:
    st.header("🗓 Últimos 10 Concursos da LotoFácil")
    ultimos = capturar_ultimos_resultados(10)
    for concurso, dezenas in ultimos:
        dezenas_formatadas = ' - '.join(f"{d:02}" for d in sorted(dezenas))
        st.markdown(f"**Concurso {concurso}:** {dezenas_formatadas}")

with aba[3]:
    st.header("📤 Exportar Cartões")
    if st.session_state.get('cartoes'):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬇️ Exportar .TXT"):
                caminho = exportar_txt(st.session_state['cartoes'])
                st.success(f"Salvo em {caminho}")
        with col2:
            if st.button("⬇️ Exportar .PDF"):
                caminho = exportar_pdf(st.session_state['cartoes'])
                st.success(f"Salvo em {caminho}")
    else:
        st.info("Gere cartões antes de exportar.")

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 14px;'>Desenvolvido por <strong>SAMUCJ TECHNOLOGY</strong> 💡</p>", unsafe_allow_html=True)
