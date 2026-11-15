import re
from collections import Counter
from urllib.parse import quote

import streamlit as st

st.set_page_config(page_title="Spider Hot", page_icon="🕷️", layout="wide")

st.title("🕷️ Spider Hot")
st.subheader("Crawler de palavras-chave e tendências")

st.markdown("""
<style>
.spider-stage{position:relative;height:330px;overflow:hidden;border-radius:18px;
background:radial-gradient(ellipse at 50% 45%,#101b35 0%,#050711 72%);
border:1px solid #263b65;margin:12px 0 18px;color:#d9e8ff}
.spider-stage .scanline{position:absolute;inset:-30% 0 auto;height:45%;
background:linear-gradient(180deg,transparent,rgba(0,214,255,.10),transparent);
animation:scan 4s linear infinite;pointer-events:none}
@keyframes scan{to{transform:translateY(390px)}}
.code-row{position:absolute;white-space:nowrap;font:11px/1.5 monospace;color:#a7b6d1;opacity:.62}
.r1{top:28px;left:4%}.r2{top:66px;left:18%}.r3{top:105px;left:7%}
.r4{top:150px;left:25%}.r5{top:205px;left:5%}.r6{top:255px;left:18%}
.hl{position:absolute;height:13px;border-radius:2px;background:#e500bd;opacity:.78;
box-shadow:0 0 13px #ed00cb;animation:pulse 2s ease-in-out infinite alternate}
.h1{top:64px;left:48%;width:22%}.h2{top:147px;left:8%;width:19%;background:#168dff;box-shadow:0 0 13px #168dff}
.h3{top:224px;left:58%;width:26%;background:#168dff;box-shadow:0 0 13px #168dff}
@keyframes pulse{to{opacity:.35;filter:brightness(1.8)}}
.web-lines{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.web-lines path{fill:none;stroke:#41dfff;stroke-width:1;opacity:.3}
.spider-walker{position:absolute;left:43%;top:39%;width:120px;height:120px;
filter:drop-shadow(0 0 9px #00d9ff);animation:travel 9s ease-in-out infinite alternate}
@keyframes travel{0%{transform:translate(-70px,-10px) rotate(-8deg)}
35%{transform:translate(55px,22px) rotate(8deg)}
70%{transform:translate(-5px,-30px) rotate(-5deg)}
100%{transform:translate(120px,10px) rotate(7deg)}}
.leg{fill:none;stroke:#52eaff;stroke-width:3;stroke-linecap:round;transform-box:fill-box;transform-origin:50% 50%;animation:legs .42s ease-in-out infinite alternate}
.leg:nth-child(even){animation-delay:.2s}
@keyframes legs{to{transform:rotate(13deg) translateY(-3px)}}
.spider-body{fill:#111b36;stroke:#ff35d5;stroke-width:2.5}
.spider-eye{fill:#ff4be1;filter:drop-shadow(0 0 4px #ff00d4)}
.web-tag{position:absolute;font: bold 10px monospace;color:#6eeaff;text-shadow:0 0 7px #00cfff}
.t1{top:18px;right:7%}.t2{bottom:20px;left:8%}.t3{bottom:18px;right:10%}
@media(max-width:600px){.spider-stage{height:290px}.spider-walker{left:34%;top:39%;width:110px;height:110px}.code-row{font-size:9px}}
</style>
<div class="spider-stage">
  <div class="scanline"></div>
  <div class="code-row r1">web crawler // indexando palavras e links ...</div>
  <div class="code-row r2">#tendencias&nbsp;&nbsp; relevancia: 0.98&nbsp;&nbsp; sinal detectado</div>
  <div class="code-row r3">engajamento / busca publica / palavras-chave</div>
  <div class="code-row r4">captura de termos&nbsp;&nbsp; conexao estabelecida</div>
  <div class="code-row r5">analise semantica&nbsp;&nbsp; rastreando pagina ...</div>
  <div class="code-row r6">Spider Hot :: crawler visual online</div>
  <div class="hl h1"></div><div class="hl h2"></div><div class="hl h3"></div>
  <svg class="web-lines" viewBox="0 0 800 330" preserveAspectRatio="none">
    <path d="M400 165L0 0M400 165L800 0M400 165L0 330M400 165L800 330M400 165L400 0M400 165L400 330M400 165L0 165M400 165L800 165"/>
    <path d="M400 165Q200 35 30 165Q200 295 400 165Q600 35 770 165Q600 295 400 165"/>
    <path d="M400 165Q280 85 150 165Q280 245 400 165Q520 85 650 165Q520 245 400 165"/>
  </svg>
  <div class="spider-walker">
    <svg viewBox="0 0 120 120" width="100%" height="100%" aria-label="Aranha robótica animada">
      <g>
        <path class="leg" d="M49 48L31 34L13 39L4 28"/><path class="leg" d="M46 57L25 53L12 65L2 61"/>
        <path class="leg" d="M47 68L27 78L18 94L7 96"/><path class="leg" d="M52 76L42 96L47 111L39 117"/>
        <path class="leg" d="M71 48L89 34L107 39L116 28"/><path class="leg" d="M74 57L95 53L108 65L118 61"/>
        <path class="leg" d="M73 68L93 78L102 94L113 96"/><path class="leg" d="M68 76L78 96L73 111L81 117"/>
      </g>
      <ellipse class="spider-body" cx="60" cy="65" rx="17" ry="23"/>
      <ellipse class="spider-body" cx="60" cy="37" rx="13" ry="12"/>
      <circle class="spider-eye" cx="55" cy="35" r="2.8"/><circle class="spider-eye" cx="65" cy="35" r="2.8"/>
      <path d="M60 22L60 5" stroke="#ff35d5" stroke-width="1.5"/>
    </svg>
  </div>
  <div class="web-tag t1">SCANNING ●</div><div class="web-tag t2">KEYWORDS FOUND</div><div class="web-tag t3">SPIDER HOT</div>
</div>
""", unsafe_allow_html=True)

st.caption("A aranha agora tem uma animação inspirada no vídeo: pernas articuladas, teia, varredura e destaques neon. O movimento é visual; a análise real acontece nos dados abaixo.")

st.header("1. Capturar palavras-chave")
st.write("Cole legendas, hashtags ou descrições de conteúdos públicos que você tem autorização para analisar.")
texto = st.text_area("Textos para analisar", height=160, placeholder="Ex.: #beleza #dicas ...")

if st.button("🕸️ Analisar palavras-chave", type="primary"):
    if not texto.strip():
        st.warning("Cole algum texto ou hashtags primeiro.")
    else:
        hashtags = re.findall(r"#[\\wÀ-ÿ]+", texto.lower(), flags=re.UNICODE)
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
