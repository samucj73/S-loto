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

# Configuração do app
st.set_page_config(page_title="LotoFácil Inteligente", layout="wide")
st.markdown("<h1 style='text-align: center;'>🍀 LotoFácil Inteligente</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Gere cartões com base em estatísticas reais e personalização</p>", unsafe_allow_html=True)

# Captura os resultados apenas uma vez
resultados_raw = capturar_ultimos_resultados(10)
resultados = [r[1] for r in resultados_raw]

# Abas principais
aba = st.tabs(["🎯 Geração de Cartões", "📊 Estatísticas", "🗓 Últimos Resultados", "📤 Exportação"])

# --- Aba 1: Geração de Cartões ---
with aba[0]:
    st.header("🎯 Geração de Cartões Inteligentes")
    qtd_cartoes = st.slider("Quantos cartões deseja gerar?", 1, 100, 5)
    fixas = st.multiselect("Escolha até 7 dezenas fixas:", list(range(1, 26)))
    excluir = st.multiselect("Deseja excluir até 5 dezenas?", [i for i in range(1, 26) if i not in fixas])

    if len(fixas) > 7:
        st.warning("Máximo de 7 dezenas fixas permitidas.")
        st.stop()
    elif len(excluir) > 5:
        st.warning("Máximo de 5 dezenas para excluir.")
        st.stop()

    if st.button("🔁 Gerar Cartões"):
        cartoes = gerar_cartoes_personalizados(fixas, excluir, qtd_cartoes, resultados)
        for i, cartao in enumerate(cartoes, 1):
            st.code(f"Cartão {i}: {' - '.join(f'{n:02}' for n in sorted(cartao))}", language="text")
        st.session_state['cartoes'] = cartoes

# --- Aba 2: Estatísticas ---
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
            trio_str = ' - '.join(f"{n:02}" for n in trio)
            st.write(f"{trio_str}: {freq}x")

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

# --- Aba 3: Últimos Resultados ---
with aba[2]:
    st.subheader("🗓 Últimos 10 Resultados da LotoFácil")
    for concurso, dezenas in sorted(resultados_raw, reverse=True):
        st.markdown(f"**Concurso {concurso}:** {' - '.join(f'{n:02}' for n in dezenas)}")

# --- Aba 4: Exportação ---
with aba[3]:
    st.header("📤 Exportar Cartões")

    def exibir_exportacao(formato, funcao_exportar):
        if st.button(f"⬇️ Exportar .{formato.upper()}"):
            caminho = funcao_exportar(st.session_state['cartoes'])
            st.success(f"Salvo em {caminho}")

    if st.session_state.get('cartoes'):
        col1, col2 = st.columns(2)
        with col1:
            exibir_exportacao("txt", exportar_txt)
        with col2:
            exibir_exportacao("pdf", exportar_pdf)
    else:
        st.info("Gere cartões antes de exportar.")

# Rodapé
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 14px;'>Desenvolvido por <strong>SAMUCJ TECHNOLOGY</strong> 💡</p>", unsafe_allow_html=True)
