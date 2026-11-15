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
*{box-sizing:border-box}html,body{margin:0;background:#050609;color:#c7cbd6;font:12px/1.55 Georgia,serif;overflow:hidden}
#world{height:440px;overflow:auto;position:relative;background:#050609;padding:15px 18px 50px;scrollbar-width:thin;scrollbar-color:#34304a #08090d}
#paper{max-width:920px;margin:auto;columns:2;column-gap:28px}
h2{font:18px Georgia;color:#e1e5f0;border-bottom:1px solid #34394b;margin:4px 0 10px;break-after:avoid}
p{margin:0 0 10px;break-inside:avoid;color:#aeb5c4}
.w{display:inline;position:relative}
#overlay{position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:8}
.touched{outline:1px solid #ff35d2;background:rgba(245,25,190,.22);color:#fff;text-shadow:0 0 7px #ff24d4}
#status{position:sticky;top:0;z-index:9;text-align:right;font:9px monospace;color:#9e8cff;letter-spacing:1.3px;pointer-events:none}
@media(max-width:580px){#paper{columns:1}#world{padding:12px 10px}}
</style>
<div id="world"><div id="status">SPIDER HOT · WEB CRAWLER ONLINE</div><main id="paper"></main></div>
<canvas id="overlay"></canvas>
<script>
(()=>{
const paper=document.getElementById('paper'),world=document.getElementById('world'),canvas=document.getElementById('overlay'),ctx=canvas.getContext('2d');
const paragraphs=[
'A Spider Hot percorre textos públicos e identifica palavras recorrentes, assuntos e referências úteis para pesquisa.',
'Uma página digital reúne títulos, descrições, hashtags e ligações. Cada palavra pode ser um ponto de passagem para a aranha.',
'Rastreamento visual significa percorrer o conteúdo apresentado, marcar termos e desenhar conexões entre os pontos visitados.',
'Análise de tendências compara frequência, contexto, crescimento e relevância de temas em fontes abertas e autorizadas.',
'Criadores acompanham assuntos emergentes, formatos populares e sinais públicos de interesse para planejar novos conteúdos.',
'Um mecanismo de busca organiza documentos, encontra termos e segue links permitidos para descobrir novas páginas.',
'Palavras-chave, legendas e etiquetas ajudam a descrever o tema de uma publicação e facilitam sua descoberta.',
'Os fios luminosos representam o caminho percorrido, enquanto as marcas coloridas mostram palavras tocadas durante a varredura.',
'Uma boa análise separa observações reais de simulações visuais e respeita os limites de acesso de cada plataforma.',
'Spider Hot: rastreamento de texto, descoberta de termos, mapa de palavras e análise de conteúdo público.'
];
for(let i=0;i<36;i++){const p=document.createElement('p');const s=paragraphs[i%paragraphs.length]+' '+paragraphs[(i*3+2)%paragraphs.length];s.split(/(\s+)/).forEach(t=>{if(!t.trim()){p.append(document.createTextNode(t));return}const w=document.createElement('span');w.className='w';w.textContent=t;p.append(w)});paper.append(p)}
let W,H,D=1;function resize(){D=Math.min(devicePixelRatio||1,2);W=innerWidth;H=innerHeight;canvas.width=W*D;canvas.height=H*D;canvas.style.width=W+'px';canvas.style.height=H+'px';ctx.setTransform(D,0,0,D,0,0)}addEventListener('resize',resize);resize();
const rnd=(a,b)=>a+Math.random()*(b-a),clamp=(x,a,b)=>Math.max(a,Math.min(b,x)),hyp=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);
const legs=Array.from({length:8},(_,i)=>({side:i<4?-1:1,index:i%4,foot:{x:W/2+rnd(-45,45),y:H/2+rnd(-45,45)},from:null,to:null,step:1,phase:i%2}));
const spider={x:W*.48,y:H*.42,vx:0,vy:0,angle:0,target:null};let time=0,last=performance.now(),nextThread=0;
const threads=[],glitches=[];
function pickWord(){const list=[...paper.querySelectorAll('.w')].filter(el=>{const r=el.getBoundingClientRect();return r.width>0&&r.bottom>30&&r.top<H-20});if(!list.length)return null;const el=list[(Math.random()*list.length)|0],r=el.getBoundingClientRect();return {el,x:r.left+r.width/2,y:r.top+r.height/2}}
function newTarget(){const t=pickWord();if(t)spider.target=t}
function pointFor(el){const r=el.getBoundingClientRect();return{x:r.left+r.width/2,y:r.top+r.height/2}}
function line(a,b,color,width=1){ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.strokeStyle=color;ctx.lineWidth=width;ctx.stroke()}
function drawLeg(L,i){
 const s=L.side,k=L.index,ang=spider.angle+(s*(.48+k*.46)+(k-1.5)*.12);
 const hip={x:spider.x+Math.cos(spider.angle+Math.PI/2)*s*5+Math.cos(spider.angle)*((k-1.5)*4),y:spider.y+Math.sin(spider.angle+Math.PI/2)*s*5+Math.sin(spider.angle)*((k-1.5)*4)};
 const reach=25+k*2,rest={x:hip.x+Math.cos(ang)*reach,y:hip.y+Math.sin(ang)*reach};
 if(!L.to&&hyp(L.foot,rest)>15){L.from={...L.foot};const candidates=[...paper.querySelectorAll('.w')].filter(el=>{const r=el.getBoundingClientRect();return r.width&&r.top>0&&r.bottom<H});let best=null,bd=1e9;for(let n=0;n<10&&candidates.length;n++){const el=candidates[(Math.random()*candidates.length)|0],p=pointFor(el),d=hyp(p,rest);if(d<bd&&d<65){best={...p,el};bd=d}}L.to=best||rest;L.step=0}
 if(L.to){L.step=Math.min(1,L.step+0.13);const lift=Math.sin(L.step*Math.PI)*8;L.foot={x:L.from.x+(L.to.x-L.from.x)*L.step,y:L.from.y+(L.to.y-L.from.y)*L.step-lift};if(L.step>=1){L.foot={x:L.to.x,y:L.to.y};if(L.to.el){L.to.el.classList.add('touched');glitches.push({el:L.to.el,life:1.3});threads.push({a:{x:spider.x,y:spider.y},b:{...L.foot},life:2.8,color:['#bd55ff','#ff35c8','#39bfff'][i%3]})}L.to=null}}
 const foot=L.foot,dx=foot.x-hip.x,dy=foot.y-hip.y,d=Math.max(1,Math.hypot(dx,dy)),L1=reach*.56,L2=reach*.7,along=clamp((L1*L1-L2*L2+d*d)/(2*d),-L1,L1),height=Math.sqrt(Math.max(0,L1*L1-along*along)),nx=dx/d,ny=dy/d;
 const bend=(s*(k<2?-1:1)),knee={x:hip.x+nx*along-ny*height*bend,y:hip.y+ny*along+nx*height*bend};
 line(hip,knee,'#79cfff',1.65);line(knee,foot,'#4bb7ff',1.35);ctx.beginPath();ctx.arc(knee.x,knee.y,2,0,Math.PI*2);ctx.fillStyle='#ff4bd5';ctx.fill();ctx.beginPath();ctx.arc(foot.x,foot.y,1.8,0,7);ctx.fillStyle='#c7f4ff';ctx.fill();
}
function drawSpider(){ctx.save();ctx.translate(spider.x,spider.y);ctx.rotate(spider.angle);ctx.shadowBlur=12;ctx.shadowColor='#b14dff';ctx.fillStyle='#111321';ctx.strokeStyle='#c5a4ff';ctx.lineWidth=1.7;ctx.beginPath();ctx.ellipse(0,2,10,15,0,0,7);ctx.fill();ctx.stroke();ctx.beginPath();ctx.ellipse(0,-15,8,8,0,0,7);ctx.fill();ctx.stroke();ctx.fillStyle='#ff45d7';ctx.shadowColor='#ff35d7';ctx.beginPath();ctx.arc(-3,-16,1.7,0,7);ctx.arc(3,-16,1.7,0,7);ctx.fill();ctx.restore();legs.forEach(drawLeg)}
function frame(now){const dt=Math.min((now-last)/1000,.04);last=now;time+=dt;ctx.clearRect(0,0,W,H);
 if(!spider.target||hyp({x:spider.x,y:spider.y},spider.target)<17){if(spider.target?.el){const p=pointFor(spider.target.el);threads.push({a:{x:spider.x,y:spider.y},b:p,life:2.4,color:'#ff32d4'})}newTarget()}
 if(spider.target){const dx=spider.target.x-spider.x,dy=spider.target.y-spider.y,d=Math.max(1,Math.hypot(dx,dy));spider.vx+=(dx/d*72-spider.vx)*dt*2.8;spider.vy+=(dy/d*72-spider.vy)*dt*2.8;spider.x+=spider.vx*dt;spider.y+=spider.vy*dt;spider.angle=Math.atan2(spider.vy,spider.vx)}
 threads.forEach(t=>{t.life-=dt;ctx.globalAlpha=Math.max(0,t.life/2.8);line(t.a,t.b,t.color,.85)});ctx.globalAlpha=1;for(let i=threads.length-1;i>=0;i--)if(threads[i].life<=0)threads.splice(i,1);
 glitches.forEach(g=>{g.life-=dt;if(g.life<=0)g.el.classList.remove('touched')});for(let i=glitches.length-1;i>=0;i--)if(glitches[i].life<=0)glitches.splice(i,1);
 drawSpider();requestAnimationFrame(frame)}
newTarget();requestAnimationFrame(frame);
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
