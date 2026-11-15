import streamlit as st
from urllib.parse import quote

st.set_page_config(page_title="Spider Hot", page_icon="🕷️", layout="wide")

st.title("🕷️ Spider Hot")
st.subheader("Central de pesquisa de tendências do TikTok")

st.write(
    "Use este painel para organizar suas pesquisas. "
    "A consulta de tendências abre a fonte oficial do TikTok."
)

st.divider()

st.header("🔎 Pesquisar tendências")
nicho = st.text_input("Digite um tema, hashtag ou palavra-chave", "beleza")

col1, col2 = st.columns(2)
with col1:
    st.link_button(
        "Abrir tendências oficiais do TikTok",
        "https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en"
    )
with col2:
    if nicho.strip():
        url_busca = (
            "https://www.tiktok.com/search?q=" + quote(nicho.strip())
        )
        st.link_button("Pesquisar este tema no TikTok", url_busca)

st.info(
    "Atenção: esta versão abre fontes públicas para consulta. "
    "Ela ainda não coleta métricas automaticamente nem acessa dados privados."
)

st.header("📋 Registro da pesquisa")
tema = st.text_input("Tema que você está analisando", key="tema_registro")
observacao = st.text_area("Anotações (ex.: hashtags, visualizações, formato do vídeo)")
if st.button("Salvar anotação nesta sessão"):
    if tema.strip() or observacao.strip():
        st.success("Anotação registrada nesta sessão.")
        st.write("**Tema:**", tema)
        st.write("**Anotações:**", observacao)
    else:
        st.warning("Digite um tema ou uma anotação primeiro.")

st.caption("Spider Hot — versão inicial. Não insira senhas nem dados privados.")
