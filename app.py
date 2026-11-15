import streamlit as st
from urllib.parse import quote

st.set_page_config(page_title="Spider Hot", page_icon="🕷️", layout="wide")

# Aranha digital neon em estilo wireframe, atravessando a tela
st.markdown("""
<style>
.neon-spider {
  position: fixed;
  left: -130px;
  top: 38%;
  width: 112px;
  height: 112px;
  z-index: 999999;
  pointer-events: none;
  animation: crawl-across 18s linear infinite;
  filter: drop-shadow(0 0 5px #20eaff) drop-shadow(0 0 12px #c13cff);
}
.neon-spider svg { width: 100%; height: 100%; overflow: visible; }
.neon-spider .cyan { stroke: #20eaff; }
.neon-spider .pink { stroke: #ff3bd4; }
.neon-spider .violet { stroke: #a56bff; }
.neon-spider path, .neon-spider line, .neon-spider ellipse, .neon-spider circle {
  fill: none; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round;
}
.neon-spider .body { fill: #16102c; stroke-width: 2.8; }
.neon-spider .leg {
  transform-box: fill-box;
  transform-origin: center;
  animation: leg-twitch .32s ease-in-out infinite alternate;
}
.neon-spider .leg:nth-child(even) { animation-delay: .16s; }
@keyframes crawl-across {
  0% { transform: translateX(0) translateY(0) rotate(-7deg); }
  15% { transform: translateX(15vw) translateY(-10px) rotate(5deg); }
  30% { transform: translateX(30vw) translateY(3px) rotate(-5deg); }
  45% { transform: translateX(45vw) translateY(-9px) rotate(5deg); }
  60% { transform: translateX(60vw) translateY(2px) rotate(-5deg); }
  75% { transform: translateX(75vw) translateY(-9px) rotate(5deg); }
  100% { transform: translateX(calc(100vw + 150px)) translateY(0) rotate(-5deg); }
}
@keyframes leg-twitch { from { rotate: -5deg; } to { rotate: 7deg; } }
@media (prefers-reduced-motion: reduce) {
  .neon-spider { animation: none; left: 12px; }
  .neon-spider .leg { animation: none; }
}
</style>
<div class="neon-spider" aria-hidden="true">
<svg viewBox="0 0 120 120">
  <g class="leg pink">
    <path d="M49 48 L30 31 L13 18 L5 27"/>
    <path d="M45 57 L25 53 L8 61 L3 73"/>
    <path d="M48 68 L28 79 L16 96 L5 94"/>
    <path d="M55 73 L45 94 L48 111 L38 117"/>
  </g>
  <g class="leg cyan">
    <path d="M71 48 L90 31 L107 18 L115 27"/>
    <path d="M75 57 L95 53 L112 61 L117 73"/>
    <path d="M72 68 L92 79 L104 96 L115 94"/>
    <path d="M65 73 L75 94 L72 111 L82 117"/>
  </g>
  <ellipse class="body violet" cx="60" cy="61" rx="15" ry="22"/>
  <ellipse class="body cyan" cx="60" cy="35" rx="11" ry="14"/>
  <circle class="pink" cx="56" cy="32" r="2.5"/>
  <circle class="pink" cx="64" cy="32" r="2.5"/>
  <path class="cyan" d="M53 21 L47 12 M67 21 L73 12"/>
  <path class="violet" d="M50 60 L60 70 L70 60 M51 48 L60 54 L69 48"/>
</svg>
</div>
""", unsafe_allow_html=True)

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
        url_busca = "https://www.tiktok.com/search?q=" + quote(nicho.strip())
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
