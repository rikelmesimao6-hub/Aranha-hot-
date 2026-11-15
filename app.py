import streamlit as st
from urllib.parse import quote

st.set_page_config(page_title="Spider Hot", page_icon="🕷️", layout="wide")

st.title("🕷️ Spider Hot")
st.subheader("Central de pesquisa de tendências do TikTok")

# Cena animada: a aranha percorre palavras-chave e lança fios de teia.
st.markdown("""
<style>
.web-scene {
  position: relative; height: 300px; width: 100%; overflow: hidden;
  border-radius: 18px; margin: 12px 0 24px;
  background: radial-gradient(ellipse at 50% 45%, #18213b 0%, #090d19 62%, #05070d 100%);
  border: 1px solid #293650;
}
.web-scene .web-lines { position:absolute; inset:0; width:100%; height:100%; opacity:.65; }
.web-scene .web-lines path, .web-scene .web-lines line, .web-scene .web-lines circle {
  fill:none; stroke:#31dfff; stroke-width:1.2; opacity:.65;
}
.keyword {
  position:absolute; padding:8px 13px; border-radius:20px; color:#eafaff;
  border:1px solid #31dfff; background:#101d31dd; font:600 13px sans-serif;
  box-shadow:0 0 12px #1ccfff55; white-space:nowrap;
}
.k1 { left:7%; top:22%; animation: glow 2s infinite alternate; }
.k2 { left:39%; top:13%; animation: glow 2s .5s infinite alternate; }
.k3 { right:7%; top:29%; animation: glow 2s 1s infinite alternate; }
.k4 { left:18%; bottom:17%; animation: glow 2s 1.5s infinite alternate; }
.k5 { right:18%; bottom:14%; animation: glow 2s .8s infinite alternate; }
.spider-runner {
  position:absolute; left:-90px; top:43%; width:76px; height:76px; z-index:5;
  animation: spider-route 13s linear infinite;
  filter:drop-shadow(0 0 7px #27dfff) drop-shadow(0 0 12px #b94cff);
}
.spider-runner svg { width:100%; height:100%; overflow:visible; }
.spider-runner path, .spider-runner ellipse, .spider-runner circle {
  fill:none; stroke-width:2.4; stroke-linecap:round; stroke-linejoin:round;
}
.spider-runner .blue { stroke:#26e5ff; }
.spider-runner .purple { stroke:#b66aff; }
.spider-runner .pink { stroke:#ff4bc8; }
.spider-runner .legs { transform-origin:50% 50%; animation: legs  .22s ease-in-out infinite alternate; }
.spider-thread {
  position:absolute; width:2px; height:110px; top:-110px; left:50%;
  background:linear-gradient(transparent,#31e8ff,#bd63ff);
  transform-origin:top; animation: thread-swing 2s ease-in-out infinite alternate;
}
@keyframes spider-route {
  0% { transform:translateX(0) translateY(0) rotate(-8deg); }
  20% { transform:translateX(22vw) translateY(-26px) rotate(7deg); }
  40% { transform:translateX(44vw) translateY(22px) rotate(-7deg); }
  60% { transform:translateX(66vw) translateY(-20px) rotate(7deg); }
  80% { transform:translateX(88vw) translateY(18px) rotate(-7deg); }
  100% { transform:translateX(calc(100vw + 110px)) translateY(0) rotate(7deg); }
}
@keyframes legs { from { transform:rotate(-9deg); } to { transform:rotate(9deg); } }
@keyframes glow { from { box-shadow:0 0 5px #22dfff44; } to { box-shadow:0 0 18px #b84dffbb; border-color:#d26bff; } }
@keyframes thread-swing { from { transform:rotate(-10deg); } to { transform:rotate(10deg); } }
@media (prefers-reduced-motion: reduce) {
 .spider-runner,.spider-runner .legs,.keyword,.spider-thread { animation:none; }
}
</style>
<div class="web-scene" aria-label="Animação de aranha digital capturando palavras-chave">
<svg class="web-lines" viewBox="0 0 800 300" preserveAspectRatio="none">
 <path d="M400 0 L400 300 M0 150 L800 150 M100 0 L700 300 M700 0 L100 300"/>
 <path d="M400 150 Q300 80 200 150 Q300 220 400 150 Q500 80 600 150 Q500 220 400 150"/>
 <path d="M400 150 Q320 30 400 20 Q480 30 400 150 Q320 270 400 280 Q480 270 400 150"/>
 <circle cx="400" cy="150" r="45"/><circle cx="400" cy="150" r="90"/><circle cx="400" cy="150" r="135"/>
</svg>
<div class="keyword k1">#viral</div>
<div class="keyword k2">#tendências</div>
<div class="keyword k3">#TikTok</div>
<div class="keyword k4">#criadores</div>
<div class="keyword k5">#engajamento</div>
<div class="spider-runner">
 <div class="spider-thread"></div>
 <svg viewBox="0 0 100 100">
  <g class="legs pink">
   <path d="M40 38 L23 24 L8 14 M37 48 L17 45 L4 54 M40 59 L22 73 L10 88 M45 65 L38 84 L43 98"/>
  </g>
  <g class="legs blue">
   <path d="M60 38 L77 24 L92 14 M63 48 L83 45 L96 54 M60 59 L78 73 L90 88 M55 65 L62 84 L57 98"/>
  </g>
  <ellipse class="purple" cx="50" cy="57" rx="13" ry="19"/>
  <ellipse class="blue" cx="50" cy="34" rx="10" ry="12"/>
  <circle class="pink" cx="46" cy="32" r="2"/><circle class="pink" cx="54" cy="32" r="2"/>
 </svg>
</div>
</div>
""", unsafe_allow_html=True)

st.caption("A animação é visual: as palavras mostradas são exemplos, não resultados coletados.")

st.write(
    "Use este painel para organizar suas pesquisas. "
    "A consulta de tendências abre fontes públicas do TikTok."
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
    "Esta versão abre fontes públicas para consulta. "
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
