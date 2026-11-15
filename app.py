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
*{box-sizing:border-box}html,body{margin:0;background:#050609;color:#b9bdca;font:11px/1.55 Georgia,serif;overflow:hidden}
#page{height:430px;overflow:hidden;padding:12px 12px 25px;column-count:2;column-gap:22px}
.entry{break-inside:avoid;margin:0 0 8px}.word{display:inline}
#fx{position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:5}
.hit{outline:1px solid #ff28d7;background:rgba(255,25,205,.16);color:#ff7be6}
@media(max-width:560px){#page{column-count:1;padding:10px 9px}.entry{font-size:10px}}
</style>
<main id="page"></main><canvas id="fx"></canvas>
<script>
(()=>{
const page=document.getElementById('page'),cv=document.getElementById('fx'),ctx=cv.getContext('2d');
const samples=[
'Network discovery and automated information retrieval across public web documents.',
'Social media trends and audience signals in short-form video platforms.',
'Semantic indexing, keyword frequency and topic classification for digital content.',
'Public metadata can reveal recurring subjects, links and related search terms.',
'Content analysis combines captions, hashtags and engagement indicators.',
'Automated crawlers navigate permitted pages and record useful references.',
'Search systems rank documents according to relevance, freshness and context.',
'Digital publishing, creators, community growth and online discovery patterns.',
'Machine learning methods for clustering phrases and identifying emerging topics.',
'Web architecture, link graphs and distributed information systems.'
];
for(let i=0;i<45;i++){
 const p=document.createElement('div');p.className='entry';
 const lead=document.createElement('span');lead.textContent=(i+1)+'. ';
 p.appendChild(lead);
 const sentence=samples[i%samples.length]+' '+samples[(i*3+2)%samples.length];
 sentence.split(/(\s+)/).forEach(part=>{if(!part.trim()){p.appendChild(document.createTextNode(part));return}
 const s=document.createElement('span');s.className='word';s.textContent=part;p.appendChild(s)});
 page.appendChild(p);
}
let W=0,H=0,D=1;
function resize(){D=Math.min(devicePixelRatio||1,2);W=innerWidth;H=innerHeight;cv.width=W*D;cv.height=H*D;cv.style.width=W+'px';cv.style.height=H+'px';ctx.setTransform(D,0,0,D,0,0)}
addEventListener('resize',resize);resize();
const rand=(a,b)=>a+Math.random()*(b-a),clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const legs=Array.from({length:8},(_,i)=>({ang:(-150+i*42.85)*Math.PI/180,fx:0,fy:0,phase:i%2,step:0,from:null,to:null}));
const spider={x:W*.5,y:H*.5,vx:0,vy:0,target:null,heading:0};
const threads=[],extracts=[];let last=performance.now(),elapsed=0,tokenIndex=0;
function choose(){const words=[...page.querySelectorAll('.word')].filter(el=>{const r=el.getBoundingClientRect();return r.width&&r.top>0&&r.bottom<H});
 if(!words.length)return;const el=words[Math.floor(Math.random()*words.length)],r=el.getBoundingClientRect();spider.target={x:r.left+r.width/2,y:r.top+r.height/2,el};}
function line(x1,y1,x2,y2,c,w=1){ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.strokeStyle=c;ctx.lineWidth=w;ctx.stroke()}
function drawSpider(){
 const s=spider,angle=s.heading;
 ctx.save();ctx.translate(s.x,s.y);ctx.rotate(angle);
 legs.forEach((L,i)=>{
  const side=i<4?-1:1,idx=i%4,hipX=(idx-1.5)*5,hipY=side*3;
  const base= L.ang, reach=24+idx*2;
  const swing=Math.sin(elapsed*9+i*Math.PI)*5;
  const fx=Math.cos(base)*reach+swing,fy=Math.sin(base)*reach;
  const kneeX=hipX+fx*.48+(side*-9),kneeY=hipY+fy*.52;
  line(hipX,hipY,kneeX,kneeY,'#8ddcff',1.5);line(kneeX,kneeY,fx,fy,'#5ab9ff',1.4);
  ctx.beginPath();ctx.arc(kneeX,kneeY,1.7,0,Math.PI*2);ctx.fillStyle='#ff45d4';ctx.fill();
 });
 ctx.beginPath();ctx.ellipse(0,0,9,13,0,0,Math.PI*2);ctx.fillStyle='#11152b';ctx.fill();ctx.strokeStyle='#c1a2ff';ctx.lineWidth=1.5;ctx.stroke();
 ctx.beginPath();ctx.arc(0,-12,7,0,Math.PI*2);ctx.fillStyle='#17152b';ctx.fill();ctx.stroke();
 ctx.fillStyle='#ff40d5';ctx.shadowColor='#ff20d4';ctx.shadowBlur=8;ctx.beginPath();ctx.arc(-2,-13,1.5,0,7);ctx.arc(2,-13,1.5,0,7);ctx.fill();ctx.restore();
}
function animate(now){
 const dt=Math.min((now-last)/1000,.04);last=now;elapsed+=dt;ctx.clearRect(0,0,W,H);
 if(!spider.target||Math.hypot(spider.target.x-spider.x,spider.target.y-spider.y)<18){
  if(spider.target?.el){const el=spider.target.el;el.classList.add('hit');setTimeout(()=>el.classList.remove('hit'),1500);
   const r=el.getBoundingClientRect();extracts.push({x:r.left,y:r.top,text:el.textContent,life:1.7,color:Math.random()<.5?'#ff27d5':'#27bfff'});
   if(threads.length>0){const p=threads[threads.length-1];threads.push({x1:p.x2,y1:p.y2,x2:spider.x,y2:spider.y,life:3})}
   threads.push({x1:spider.x,y1:spider.y,x2:spider.target.x,y2:spider.target.y,life:3});
  }choose();
 }
 if(spider.target){const dx=spider.target.x-spider.x,dy=spider.target.y-spider.y,d=Math.hypot(dx,dy)||1;
  spider.vx+=(dx/d*85-spider.vx)*Math.min(1,dt*2.4);spider.vy+=(dy/d*85-spider.vy)*Math.min(1,dt*2.4);
  spider.x+=spider.vx*dt;spider.y+=spider.vy*dt;spider.heading=Math.atan2(spider.vy,spider.vx);
 }
 threads.forEach(t=>{t.life-=dt;line(t.x1,t.y1,t.x2,t.y2,'rgba(180,80,255,'+Math.max(0,t.life/3*.6)+')',.8)});
 for(let i=threads.length-1;i>=0;i--)if(threads[i].life<=0)threads.splice(i,1);
 extracts.forEach(e=>{e.life-=dt;ctx.save();ctx.translate(e.x,e.y-(1.7-e.life)*22);ctx.rotate(-.12);ctx.globalAlpha=Math.max(0,e.life/1.7);ctx.fillStyle=e.color;ctx.fillRect(0,-12,Math.max(35,e.text.length*7),15);ctx.fillStyle='#050609';ctx.font='10px monospace';ctx.fillText(e.text,4,0);ctx.restore()});
 for(let i=extracts.length-1;i>=0;i--)if(extracts[i].life<=0)extracts.splice(i,1);
 drawSpider();requestAnimationFrame(animate);
}
choose();requestAnimationFrame(animate);
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
