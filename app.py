import re
from collections import Counter
from urllib.parse import quote

import streamlit as st

st.set_page_config(page_title="Spider Hot", page_icon="🕷️", layout="wide")

st.title("🕷️ Spider Hot")
st.subheader("Crawler de palavras-chave e tendências")

st.markdown("""
<style>
.web-scene{position:relative;height:250px;overflow:hidden;border-radius:18px;
background:radial-gradient(ellipse at center,#192641,#080c18 72%);
border:1px solid #29415f;margin:12px 0 20px}
.web-scene svg{position:absolute;inset:0;width:100%;height:100%}
.web-scene svg path,.web-scene svg circle{fill:none;stroke:#28dfff;stroke-width:1;opacity:.45}
.crawler{position:absolute;top:42%;left:-75px;font-size:54px;
filter:drop-shadow(0 0 9px #26dfff);animation:crawl 12s linear infinite}
@keyframes crawl{0%{transform:translateX(0) translateY(0) rotate(-8deg)}
25%{transform:translateX(25vw) translateY(-22px) rotate(8deg)}
50%{transform:translateX(50vw) translateY(14px) rotate(-8deg)}
75%{transform:translateX(75vw) translateY(-18px) rotate(8deg)}
100%{transform:translateX(calc(100vw + 90px)) translateY(0) rotate(-8deg)}}
</style>
<div class="web-scene">
<svg viewBox="0 0 800 250" preserveAspectRatio="none">
<path d="M400 0L400 250M0 125H800M100 0L700 250M700 0L100 250"/>
<path d="M400 125Q250 20 100 125Q250 230 400 125Q550 20 700 125Q550 230 400 125"/>
<circle cx="400" cy="125" r="45"/><circle cx="400" cy="125" r="90"/><circle cx="400" cy="125" r="135"/>
</svg>
<div class="crawler">🕷️</div>
</div>
""", unsafe_allow_html=True)

st.caption("A aranha animada é visual. A análise abaixo processa o texto público que você fornecer.")

st.header("1. Capturar palavras-chave")
st.write("Cole legendas, hashtags ou descrições de conteúdos públicos que você tem autorização para analisar.")
texto = st.text_area("Textos para analisar", height=160, placeholder="Ex.: #beleza #dicas ...")

if st.button("🕸️ Analisar palavras-chave", type="primary"):
    if not texto.strip():
        st.warning("Cole algum texto ou hashtags primeiro.")
    else:
        hashtags = re.findall(r"#[\wÀ-ÿ]+", texto.lower(), flags=re.UNICODE)
        palavras = re.findall(r"[a-zA-ZÀ-ÿ0-9]{3,}", texto.lower())
        ignorar = {"para", "com", "uma", "que", "por", "dos", "das", "the", "and", "you", "this"}
        frequencia = Counter(p for p in palavras if p not in ignorar and not p.isdigit())
        st.session_state["spider_hashtags"] = Counter(hashtags)
        st.session_state["spider_words"] = frequencia
        st.success("Análise concluída!")

if "spider_hashtags" in st.session_state:
    st.subheader("Hashtags encontradas")
    hs = st.session_state["spider_hashtags"].most_common(15)
    if hs:
        st.dataframe([{"Hashtag": k, "Ocorrências": v} for k, v in hs], use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma hashtag encontrada no texto.")

    st.subheader("Palavras mais frequentes")
    ws = st.session_state["spider_words"].most_common(15)
    if ws:
        st.dataframe([{"Palavra-chave": k, "Ocorrências": v} for k, v in ws], use_container_width=True, hide_index=True)
        termos = " ".join(k for k, _ in ws[:5])
        st.link_button("Pesquisar palavras encontradas no TikTok", "https://www.tiktok.com/search?q=" + quote(termos))
    else:
        st.info("Não encontrei palavras suficientes para classificar.")

st.divider()
st.header("2. Consultar tendências públicas")
st.link_button(
    "Abrir TikTok Creative Center",
    "https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en"
)
termo = st.text_input("Pesquisar um tema no TikTok", "beleza")
if termo.strip():
    st.link_button("Abrir pesquisa do tema", "https://www.tiktok.com/search?q=" + quote(termo.strip()))

st.info("Limite desta versão: ela analisa o texto colado por você e abre fontes públicas. Não coleta vídeos ou métricas automaticamente.")
st.caption("Spider Hot — análise de texto e hashtags. Use somente conteúdo público e autorizado.")
