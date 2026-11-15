import re
from collections import Counter
from urllib.parse import quote

import streamlit as st

st.set_page_config(page_title="Spider Hot", page_icon="🕷️", layout="wide")

st.title("🕷️ Spider Hot")
st.subheader("Crawler de palavras-chave e tendências")

crawler_html = r"""
<!doctype html><html lang="pt-br"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}html,body{margin:0;background:#05050a;color:#c9c9d8;font:12px/1.6 Georgia,serif;overflow:hidden}
#world{height:440px;overflow:auto;position:relative;padding:16px 17px 55px;background:radial-gradient(ellipse at 50% 0%,#171025 0,#08070d 55%,#05050a 100%);scrollbar-width:thin;scrollbar-color:#51416b #09080e}
#paper{max-width:920px;margin:auto;columns:2;column-gap:28px}
h2{font:600 16px Georgia;color:#eee4ff;letter-spacing:.08em;border-bottom:1px solid #473451;padding-bottom:7px;break-after:avoid}
p{margin:0 0 11px;break-inside:avoid;color:#9da0b5}
.w{display:inline;position:relative;transition:color .18s,text-shadow .18s}
.keyword{color:#f2d9ff;text-decoration:underline;text-decoration-color:#b34dff;text-decoration-thickness:1px;text-underline-offset:3px}
#overlay{position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:8}
#status{position:sticky;top:0;z-index:9;text-align:right;font:9px monospace;color:#aa83d8;letter-spacing:1.5px;pointer-events:none}
.w.touched{color:#fff;text-shadow:0 0 8px #ff32c8,0 0 18px #a12fff}
.lifted{animation:liftWord 1.05s cubic-bezier(.2,.8,.2,1) forwards;pointer-events:none;z-index:20;color:#fff!important;text-shadow:0 0 8px #ff3bd1,0 0 20px #a04bff}
@keyframes liftWord{0%{opacity:1;transform:translate(0,0) scale(1)}35%{opacity:1;transform:translate(var(--dx),-16px) scale(1.28)}100%{opacity:0;transform:translate(calc(var(--dx)*1.3),-42px) scale(.72)}}
@media(max-width:580px){#paper{columns:1}#world{padding:12px 11px}}
</style>
<div id="world"><div id="status">SPIDER HOT / DOM EXPLORER / LIVE</div><main id="paper"></main></div><canvas id="overlay"></canvas>
<script>
(()=>{
const paper=document.getElementById('paper'),world=document.getElementById('world'),canvas=document.getElementById('overlay'),ctx=canvas.getContext('2d');
const terms=['palavras-chave','tendências','hashtags','crawler','aranha','teia','links','busca','conteúdo','dados','referências','público','termos','páginas','descoberta'];
const paragraphs=[
'Uma aranha digital explora a superfície de uma página e encontra palavras que funcionam como pequenos pontos de apoio.',
'Palavras-chave, tendências e hashtags formam trilhas de informação. Cada toque deixa uma marca luminosa e um fio de seda.',
'Um web crawler percorre documentos públicos, segue ligações permitidas e encontra referências relacionadas ao assunto.',
'Quando a aranha encontra um termo importante, ela prende as patas, puxa a palavra e conecta o achado ao seu caminho.',
'Links, títulos e trechos de texto ajudam a revelar relações entre temas, assuntos recorrentes e novas descobertas.',
'A teia cresce a cada encontro: fios finos ligam palavras distantes, enquanto pequenos fragmentos parecem ser recolhidos.',
'Uma busca cuidadosa respeita as páginas visitadas e utiliza apenas conteúdo público ou autorizado para análise.',
'A exploração continua de forma orgânica, com pausas, mudanças de direção e passos independentes das oito patas.'
];
const norm=s=>s.toLocaleLowerCase('pt-BR').replace(/[.,:;!?()[\]{}"“”]/g,'');
for(let i=0;i<32;i++){const p=document.createElement('p');const s=paragraphs[i%paragraphs.length]+' '+paragraphs[(i*3+2)%paragraphs.length];s.split(/(\s+)/).forEach(t=>{if(!t.trim()){p.append(document.createTextNode(t));return}const w=document.createElement('span');w.className='w';w.textContent=t;if(terms.includes(norm(t)))w.classList.add('keyword');p.append(w)});paper.append(p)}
let W=0,H=0,D=1;function resize(){D=Math.min(devicePixelRatio||1,2);W=innerWidth;H=innerHeight;canvas.width=W*D;canvas.height=H*D;canvas.style.width=W+'px';canvas.style.height=H+'px';ctx.setTransform(D,0,0,D,0,0)}addEventListener('resize',resize);resize();
const rand=(a,b)=>a+Math.random()*(b-a),clamp=(v,a,b)=>Math.max(a,Math.min(b,v)),dist=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);
const spider={x:W*.48,y:H*.43,vx:0,vy:0,angle:0,target:null,scale:.64};
const legs=Array.from({length:8},(_,i)=>({i,side:i<4?-1:1,row:i%4,foot:{x:W*.48+rand(-17,17),y:H*.43+rand(-17,17)},from:null,to:null,progress:1,phase:i%2}));
const threads=[],bursts=[];let last=performance.now(),elapsed=0,wordTimer=0;
const line=(a,b,color,width=1)=>{ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.strokeStyle=color;ctx.lineWidth=width;ctx.stroke()};
function visibleKeywords(){return [...paper.querySelectorAll('.keyword:not(.lifted)')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.bottom>28&&r.top<H-12})}
function chooseTarget(){const a=visibleKeywords();if(!a.length)return null;const el=a[(Math.random()*a.length)|0],r=el.getBoundingClientRect();return{el,x:r.left+r.width/2,y:r.top+r.height/2}}
function grabWord(el){if(!el||el.dataset.grabbed)return;el.dataset.grabbed='1';el.classList.add('touched');const r=el.getBoundingClientRect(),p={x:r.left+r.width/2,y:r.top+r.height/2};threads.push({a:{x:spider.x,y:spider.y},b:p,life:5,color:'#ed49d2'});const dx=spider.x-p.x;el.style.setProperty('--dx',dx.toFixed(1)+'px');el.classList.remove('touched');el.classList.add('lifted');bursts.push({x:p.x,y:p.y,life:1});setTimeout(()=>{if(el.isConnected)el.remove()},1150)}
function drawLeg(L){
 const i=L.i,s=L.side,k=L.row,a=spider.angle;
 const sideAng=a+s*(.45+k*.35),hip={x:spider.x+Math.cos(a+Math.PI/2)*s*4.2+Math.cos(a)*(k-1.5)*2.5,y:spider.y+Math.sin(a+Math.PI/2)*s*4.2+Math.sin(a)*(k-1.5)*2.5};
 const reach=14+k*2,rest={x:hip.x+Math.cos(sideAng)*reach,y:hip.y+Math.sin(sideAng)*reach};
 if(!L.to&&dist(L.foot,rest)>8){L.from={...L.foot};let best=null,bd=1e9;for(const el of visibleKeywords()){const r=el.getBoundingClientRect(),p={x:r.left+r.width/2,y:r.top+r.height/2},d=dist(p,rest);if(d<bd&&d<44){bd=d;best={...p,el}}}L.to=best||rest;L.progress=0}
 if(L.to){L.progress=Math.min(1,L.progress+.18);const q=L.progress*(2-L.progress),lift=Math.sin(L.progress*Math.PI)*5;L.foot={x:L.from.x+(L.to.x-L.from.x)*q,y:L.from.y+(L.to.y-L.from.y)*q-lift};if(L.progress>=1){L.foot={x:L.to.x,y:L.to.y};if(L.to.el&&Math.random()<.55)grabWord(L.to.el);L.to=null}}
 const f=L.foot,dx=f.x-hip.x,dy=f.y-hip.y,d=Math.max(1,Math.hypot(dx,dy)),l1=reach*.58,l2=reach*.72,along=clamp((l1*l1-l2*l2+d*d)/(2*d),-l1,l1),h=Math.sqrt(Math.max(0,l1*l1-along*along)),nx=dx/d,ny=dy/d,bend=s*(k<2?-1:1),knee={x:hip.x+nx*along-ny*h*bend,y:hip.y+ny*along+nx*h*bend};
 line(hip,knee,'rgba(199,174,255,.88)',1.25);line(knee,f,'rgba(119,206,255,.9)',1.05);
 ctx.beginPath();ctx.arc(knee.x,knee.y,1.45,0,Math.PI*2);ctx.fillStyle='#f18be9';ctx.fill();ctx.beginPath();ctx.arc(f.x,f.y,1.35,0,Math.PI*2);ctx.fillStyle='#e8f8ff';ctx.fill();
}
function drawSpider(){ctx.save();ctx.translate(spider.x,spider.y);ctx.rotate(spider.angle);ctx.scale(spider.scale,spider.scale);ctx.shadowBlur=9;ctx.shadowColor='#b84cff';ctx.fillStyle='#090b13';ctx.strokeStyle='#cdb3ff';ctx.lineWidth=1.55;
ctx.beginPath();ctx.ellipse(0,3,5.6,9.2,-.12,0,Math.PI*2);ctx.fill();ctx.stroke();
ctx.beginPath();ctx.ellipse(0,-7.8,4.7,4.6,0,0,Math.PI*2);ctx.fill();ctx.stroke();
ctx.fillStyle='#ff5bd6';ctx.shadowColor='#ff35d1';ctx.beginPath();ctx.arc(-1.8,-8.2,1,0,7);ctx.arc(1.8,-8.2,1,0,7);ctx.fill();
ctx.strokeStyle='#d5c5ff';ctx.lineWidth=1;for(let s of [-1,1]){ctx.beginPath();ctx.moveTo(s*2,-11);ctx.quadraticCurveTo(s*5,-15,s*7,-13);ctx.stroke()}ctx.restore()}
function frame(now){const dt=Math.min((now-last)/1000,.035);last=now;elapsed+=dt;ctx.clearRect(0,0,W,H);
if(!spider.target||dist(spider,spider.target)<13){if(spider.target&&spider.target.el)grabWord(spider.target.el);spider.target=chooseTarget()}
if(spider.target){const dx=spider.target.x-spider.x,dy=spider.target.y-spider.y,d=Math.max(1,Math.hypot(dx,dy));spider.vx+=(dx/d*54-spider.vx)*dt*2.3;spider.vy+=(dy/d*54-spider.vy)*dt*2.3;spider.x+=spider.vx*dt;spider.y+=spider.vy*dt;spider.angle=Math.atan2(spider.vy,spider.vx)}
threads.forEach(t=>{t.life-=dt;ctx.globalAlpha=Math.min(1,t.life/1.4);line(t.a,t.b,t.color,.75)});ctx.globalAlpha=1;for(let i=threads.length-1;i>=0;i--)if(threads[i].life<=0)threads.splice(i,1);
bursts.forEach(b=>{b.life-=dt;ctx.globalAlpha=Math.max(0,b.life);ctx.beginPath();ctx.arc(b.x,b.y,5+(1-b.life)*15,0,Math.PI*2);ctx.strokeStyle='#ff48d5';ctx.lineWidth=.8;ctx.stroke()});ctx.globalAlpha=1;for(let i=bursts.length-1;i>=0;i--)if(bursts[i].life<=0)bursts.splice(i,1);
legs.forEach(drawLeg);drawSpider();requestAnimationFrame(frame)}
spider.target=chooseTarget();requestAnimationFrame(frame);
})();
</script></html>
"""

st.components.v1.html(crawler_html, height=440, scrolling=False)

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
