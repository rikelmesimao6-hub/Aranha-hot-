import re
from collections import Counter
from urllib.parse import quote

import streamlit as st

st.set_page_config(page_title="Spider Hot", page_icon="🕷️", layout="wide")

st.title("🕷️ Spider Hot")
st.subheader("Crawler de palavras-chave e tendências")

st.markdown("""
<style>
.spider-stage{position:relative;height:390px;overflow:hidden;border:1px solid #22283a;border-radius:12px;
background:#050609;color:#c7c8d1;margin:12px 0 18px;font-family:Georgia,serif}
.docline{position:absolute;left:3%;right:3%;height:18px;white-space:nowrap;overflow:hidden;
font-size:12px;line-height:18px;color:#aaa9b7;opacity:.9}
.d1{top:22px}.d2{top:50px}.d3{top:78px}.d4{top:106px}.d5{top:134px}
.d6{top:162px}.d7{top:190px}.d8{top:218px}.d9{top:246px}.d10{top:274px}
.d11{top:302px}.d12{top:330px}.d13{top:358px}
.hl{position:absolute;height:17px;border-radius:1px;opacity:.88;mix-blend-mode:screen;
box-shadow:0 0 8px currentColor;animation:hlpulse 2.8s ease-in-out infinite alternate}
.pink{background:#ed00b8;color:#ed00b8}.blue{background:#168fff;color:#168fff}
.violet{background:#762cff;color:#762cff}.yellow{background:#e8c52e;color:#e8c52e}
.h1{top:47px;left:28%;width:44%}.h2{top:103px;left:8%;width:37%;animation-delay:.5s}
.h3{top:158px;left:53%;width:35%;animation-delay:1s}.h4{top:215px;left:22%;width:48%;animation-delay:1.4s}
.h5{top:272px;left:57%;width:31%;animation-delay:.8s}.h6{top:327px;left:5%;width:29%;animation-delay:1.8s}
@keyframes hlpulse{from{opacity:.42}to{opacity:.95}}
.spider-svg{position:absolute;left:42%;top:35%;width:115px;height:115px;z-index:4;
filter:drop-shadow(0 0 5px #9b38ff);animation:crawlpath 8s ease-in-out infinite alternate}
@keyframes crawlpath{0%{transform:translate(-85px,-28px) rotate(-18deg)}
24%{transform:translate(18px,4px) rotate(13deg)}
52%{transform:translate(112px,-18px) rotate(-12deg)}
78%{transform:translate(32px,54px) rotate(17deg)}
100%{transform:translate(-72px,20px) rotate(-8deg)}}
.leg{fill:none;stroke:#9b8acb;stroke-width:2;stroke-linecap:round;transform-box:fill-box;transform-origin:50% 50%;animation:step .24s ease-in-out infinite alternate}
.leg:nth-child(even){animation-delay:.12s}
@keyframes step{to{transform:rotate(17deg) translateY(-3px)}}
.body{fill:#101019;stroke:#b7a5e9;stroke-width:1.6}
.eye{fill:#ff42d4;filter:drop-shadow(0 0 3px #ff00c8)}
.thread{position:absolute;z-index:3;left:49%;top:43%;width:2px;height:110px;
background:linear-gradient(transparent,#b69cff,transparent);transform:rotate(27deg);
transform-origin:top;opacity:.85;animation:threadmove 2s ease-in-out infinite alternate}
@keyframes threadmove{to{transform:rotate(-22deg) scaleY(.72)}}
.trace{position:absolute;inset:0;width:100%;height:100%;z-index:2;pointer-events:none}
.trace path{fill:none;stroke:#a58bff;stroke-width:1;opacity:.38;stroke-dasharray:3 5;animation:dash 7s linear infinite}
@keyframes dash{to{stroke-dashoffset:-90}}
.stage-label{position:absolute;right:12px;top:9px;z-index:5;font:10px monospace;color:#9b8bcb;letter-spacing:1px}
@media(max-width:600px){.spider-stage{height:360px}.docline{font-size:10px}.spider-svg{left:34%;width:105px;height:105px}}
</style>
<div class="spider-stage">
<div class="stage-label">SPIDER HOT // WEB CRAWLER</div>
<div class="docline d1">[102] Smith, J. &amp; Brown, K. Digital networks and information retrieval — journal of web systems...</div>
<div class="docline d2">A crawler follows links, reads page structure and indexes relevant terms for later analysis.</div>
<div class="docline d3">[103] Web data extraction and semantic search. International Review of Computer Science, 2024.</div>
<div class="docline d4">Keywords detected: social media, creator trends, audience signals, public metadata, discovery...</div>
<div class="docline d5">[104] Machine learning methods for ranking documents and identifying recurring phrases.</div>
<div class="docline d6">The indexing process stores page references and matches terms against the search query.</div>
<div class="docline d7">[105] Arachnid-inspired navigation systems and distributed web crawling architectures.</div>
<div class="docline d8">Public sources // page scan // text recognition // keyword frequency // link graph</div>
<div class="docline d9">[106] Data collection should respect access permissions, privacy and website terms of service.</div>
<div class="docline d10">Detected phrase: trending topics — relevance score — source reference — indexed result.</div>
<div class="docline d11">[107] Network analysis, information retrieval and automated document classification.</div>
<div class="docline d12">Crawler status: traversing visible text ... following permitted links ... extracting terms ...</div>
<div class="docline d13">Spider Hot // keyword map // public web signals // analysis engine</div>
<div class="hl pink h1"></div><div class="hl blue h2"></div><div class="hl violet h3"></div>
<div class="hl pink h4"></div><div class="hl yellow h5"></div><div class="hl blue h6"></div>
<svg class="trace" viewBox="0 0 800 390" preserveAspectRatio="none">
<path d="M400 180L210 45L620 65L130 260L690 300L400 180M400 180L80 120L720 190L400 180"/>
<path d="M400 180Q260 75 130 190T400 180Q560 80 690 190T400 180"/>
</svg>
<div class="thread"></div>
<div class="spider-svg">
<svg viewBox="0 0 120 120" width="100%" height="100%" aria-label="Aranha robótica rastejando sobre texto">
<g>
<path class="leg" d="M49 46L31 31L14 37L5 25"/><path class="leg" d="M46 55L25 49L10 61L2 57"/>
<path class="leg" d="M47 66L27 77L17 92L6 96"/><path class="leg" d="M52 74L42 94L46 109L38 116"/>
<path class="leg" d="M71 46L89 31L106 37L115 25"/><path class="leg" d="M74 55L95 49L110 61L118 57"/>
<path class="leg" d="M73 66L93 77L103 92L114 96"/><path class="leg" d="M68 74L78 94L74 109L82 116"/>
</g>
<ellipse class="body" cx="60" cy="64" rx="15" ry="21"/>
<ellipse class="body" cx="60" cy="37" rx="11" ry="10"/>
<circle class="eye" cx="55" cy="35" r="2"/><circle class="eye" cx="65" cy="35" r="2"/>
<path d="M53 27L48 20M67 27L72 20" stroke="#b7a5e9" stroke-width="1.4"/>
</svg>
</div>
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
