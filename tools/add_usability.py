#!/usr/bin/env python3
"""Inyecta mejoras de usabilidad en un capítulo HTML del libro.

1) Comodidad de lectura: tema oscuro/sepia/claro + tamaño de letra (engranaje arriba-der).
2) Progreso y retomar: barra de progreso arriba, tiempo estimado bajo el título,
   memoria de posición de scroll («continuar donde ibas»).
3) Audio entre capítulos: tarjeta «siguiente capítulo» al terminar el audio
   (+ autoplay al llegar desde el capítulo anterior). El «retomar desde X:XX»
   ya existía en el pill.
4) Accesibilidad/móvil: skip-link, focus-visible, target de toque del play.

Todo vía variables CSS del libro, así que se adapta a los temas. Idempotente.
Uso: add_usability.py <archivo.html> [salida.html]
"""
import sys
from pathlib import Path

MARK = "<!-- usabilidad-v1 -->"

HEAD_SCRIPT = (
    "<script>(function(){try{var d=document.documentElement;"
    "var t=localStorage.getItem('ui:theme');if(t&&t!=='oscuro')d.setAttribute('data-theme',t);"
    "var f=localStorage.getItem('ui:fontscale');if(f)d.style.setProperty('--font-scale',f);"
    "}catch(e){}})();</script>\n"
)

CSS = """
/* ===== usabilidad-v1 ===== */
:root[data-theme="sepia"]{ --bg:#f3ead6; --surface:#e9dcc0; --ink:#3b3026; --ink-soft:#7c6f5c; --rule:#d6c9ab; }
:root[data-theme="claro"]{ --bg:#fbf9f5; --surface:#eeeae3; --ink:#232220; --ink-soft:#6a655d; --rule:#e2ddd3; }
:root[data-theme="sepia"] body::before,
:root[data-theme="claro"] body::before{ opacity:.5; }

.read-progress{ position:fixed; top:0; left:0; height:3px; width:100%; background:transparent; z-index:300; pointer-events:none; }
.read-progress > i{ display:block; height:100%; width:0; background:var(--verde); transition:width .08s linear; }

.ui-settings{ position:fixed; top:14px; right:14px; z-index:260; font-family:var(--font-body); }
.ui-gear{ width:42px; height:42px; border-radius:50%; border:1px solid var(--rule); background:var(--surface); color:var(--ink-soft); cursor:pointer; display:flex; align-items:center; justify-content:center; box-shadow:0 4px 16px -6px rgba(0,0,0,.5); -webkit-backdrop-filter:blur(8px); backdrop-filter:blur(8px); }
.ui-gear:hover{ color:var(--ink); }
.ui-gear svg{ width:20px; height:20px; }
.ui-panel{ position:absolute; top:50px; right:0; width:214px; background:var(--surface); border:1px solid var(--rule); border-radius:12px; padding:14px; box-shadow:0 12px 32px -8px rgba(0,0,0,.55); display:none; }
.ui-panel.open{ display:block; }
.ui-panel h4{ font-size:.7rem; letter-spacing:.14em; text-transform:uppercase; color:var(--ink-soft); margin:0 0 .55rem; font-weight:400; }
.ui-row{ display:flex; gap:6px; margin-bottom:13px; }
.ui-row:last-child{ margin-bottom:0; }
.ui-row button{ flex:1; padding:.5rem .2rem; border:1px solid var(--rule); background:transparent; color:var(--ink-soft); border-radius:8px; cursor:pointer; font-family:var(--font-body); font-size:.9rem; line-height:1; }
.ui-row button.active{ background:var(--ink); color:var(--bg); border-color:var(--ink); }

.chapter-meta{ font-family:var(--font-body); font-size:.82rem; color:var(--ink-soft); letter-spacing:.02em; margin-top:.6rem; }

.resume-read{ position:fixed; left:16px; bottom:18px; z-index:240; background:var(--surface); color:var(--ink); border:1px solid var(--rule); border-radius:22px; padding:.55rem .95rem; font-family:var(--font-body); font-size:.86rem; cursor:pointer; box-shadow:0 6px 20px -6px rgba(0,0,0,.5); display:none; }
.resume-read.show{ display:inline-flex; align-items:center; gap:.4rem; }

.next-card{ position:fixed; left:50%; bottom:92px; transform:translateX(-50%) translateY(10px); z-index:250; background:var(--surface); border:1px solid var(--rule); border-radius:14px; padding:1rem 1.2rem; box-shadow:0 16px 40px -10px rgba(0,0,0,.6); font-family:var(--font-body); text-align:center; max-width:88vw; opacity:0; pointer-events:none; transition:opacity .3s, transform .3s; }
.next-card.show{ opacity:1; transform:translateX(-50%) translateY(0); pointer-events:auto; }
.next-card .nc-label{ font-size:.7rem; letter-spacing:.14em; text-transform:uppercase; color:var(--ink-soft); }
.next-card .nc-title{ font-size:1.05rem; color:var(--ink); margin:.3rem 0 .85rem; }
.next-card .nc-actions{ display:flex; gap:.5rem; justify-content:center; }
.next-card button, .next-card a{ border:1px solid var(--rule); background:transparent; color:var(--ink); border-radius:20px; padding:.45rem 1rem; font-family:var(--font-body); font-size:.9rem; cursor:pointer; text-decoration:none; }
.next-card .nc-go{ background:var(--verde); border-color:var(--verde); color:#fff; }

.skip-link{ position:absolute; left:-999px; top:0; z-index:400; background:var(--verde); color:#fff; padding:.6rem 1rem; border-radius:0 0 8px 0; font-family:var(--font-body); }
.skip-link:focus{ left:0; }

a:focus-visible, button:focus-visible, [tabindex]:focus-visible, .ap-track:focus-visible{ outline:2px solid var(--verde); outline-offset:2px; border-radius:3px; }
.audio-pill .ap-play{ min-width:44px; min-height:44px; }
@media (max-width:640px){ .ui-settings{ top:10px; right:10px; } .resume-read{ bottom:14px; } }
"""

BODY_TOP = """<a class="skip-link" href="#contenido">Saltar al contenido</a>
<div class="read-progress" aria-hidden="true"><i></i></div>
<div class="ui-settings">
  <button class="ui-gear" aria-label="Ajustes de lectura" aria-expanded="false">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
  </button>
  <div class="ui-panel" role="menu" aria-label="Ajustes de lectura">
    <h4>Tema</h4>
    <div class="ui-row" data-group="theme">
      <button data-theme-val="oscuro">Oscuro</button>
      <button data-theme-val="sepia">Sepia</button>
      <button data-theme-val="claro">Claro</button>
    </div>
    <h4>Tamaño del texto</h4>
    <div class="ui-row" data-group="fs">
      <button data-fs="0.9" style="font-size:.8rem">A</button>
      <button data-fs="1">A</button>
      <button data-fs="1.15" style="font-size:1.15rem">A</button>
      <button data-fs="1.3" style="font-size:1.3rem">A</button>
    </div>
  </div>
</div>
"""

JS = """<script>
/* usabilidad-v1 */
(function(){
  var doc=document.documentElement;
  function lsGet(k){try{return localStorage.getItem(k)}catch(e){return null}}
  function lsSet(k,v){try{localStorage.setItem(k,v)}catch(e){}}

  var gear=document.querySelector('.ui-gear'), panel=document.querySelector('.ui-panel');
  if(gear&&panel){
    gear.addEventListener('click',function(e){e.stopPropagation();var o=panel.classList.toggle('open');gear.setAttribute('aria-expanded',String(o));});
    document.addEventListener('click',function(e){if(!panel.contains(e.target)&&!gear.contains(e.target)){panel.classList.remove('open');gear.setAttribute('aria-expanded','false');}});
  }
  function markActive(group,attr,val){
    document.querySelectorAll('.ui-row[data-group="'+group+'"] button').forEach(function(btn){
      btn.classList.toggle('active', btn.getAttribute(attr)===val);
    });
  }
  var curTheme=lsGet('ui:theme')||'oscuro';
  markActive('theme','data-theme-val',curTheme);
  document.querySelectorAll('[data-theme-val]').forEach(function(btn){
    btn.addEventListener('click',function(){
      var v=btn.getAttribute('data-theme-val');
      if(v==='oscuro')doc.removeAttribute('data-theme');else doc.setAttribute('data-theme',v);
      lsSet('ui:theme',v); markActive('theme','data-theme-val',v);
    });
  });
  var curFs=lsGet('ui:fontscale')||'1';
  doc.style.setProperty('--font-scale',curFs);
  markActive('fs','data-fs',curFs);
  document.querySelectorAll('[data-fs]').forEach(function(btn){
    btn.addEventListener('click',function(){
      var v=btn.getAttribute('data-fs');
      doc.style.setProperty('--font-scale',v); lsSet('ui:fontscale',v); markActive('fs','data-fs',v);
    });
  });

  var bar=document.querySelector('.read-progress > i'), ticking=false;
  function updBar(){
    var h=document.documentElement, max=h.scrollHeight-h.clientHeight;
    var y=h.scrollTop||window.pageYOffset||0;
    var pct=max>0?(y/max*100):0;
    if(bar)bar.style.width=Math.min(100,Math.max(0,pct))+'%';
    ticking=false;
  }
  window.addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(updBar);}},{passive:true});
  window.addEventListener('resize',updBar); updBar();

  var sub=document.querySelector('.chapter-subtitle');
  if(sub&&!document.querySelector('.chapter-meta')){
    var words=document.querySelectorAll('.prose .w, .chapter-title .w').length||0;
    var mins=Math.max(1,Math.round(words/200));
    var pe=document.querySelector('.audio-pill');
    var dur=pe?pe.getAttribute('data-duration'):'';
    var meta=document.createElement('p'); meta.className='chapter-meta';
    meta.textContent='Lectura ≈ '+mins+' min'+(dur&&dur!=='0:00'?'  ·  audio '+dur:'');
    sub.parentNode.insertBefore(meta, sub.nextSibling);
  }

  var pillEl=document.querySelector('.audio-pill');
  var sk=pillEl?(pillEl.getAttribute('data-storage-key')||'default'):'default';
  var SKEY='ui:scroll:'+sk, sticking=false;
  function saveScroll(){var y=window.pageYOffset||document.documentElement.scrollTop||0;lsSet(SKEY,String(Math.round(y)));}
  window.addEventListener('scroll',function(){if(!sticking){sticking=true;setTimeout(function(){saveScroll();sticking=false;},800);}},{passive:true});
  window.addEventListener('beforeunload',saveScroll);
  var savedY=parseInt(lsGet(SKEY)||'0',10);
  if(savedY>600 && savedY<(document.documentElement.scrollHeight-window.innerHeight-200)){
    var rr=document.createElement('button'); rr.className='resume-read';
    rr.innerHTML='↓ Continuar donde ibas';
    rr.addEventListener('click',function(){window.scrollTo({top:savedY,behavior:'smooth'});rr.classList.remove('show');});
    document.body.appendChild(rr);
    setTimeout(function(){rr.classList.add('show');},500);
    setTimeout(function(){rr.classList.remove('show');},9000);
  }

  var audio=document.querySelector('.ap-audio');
  var nextLink=document.querySelector('.nav-foot a.next');
  if(audio&&nextLink){
    var card=document.createElement('div'); card.className='next-card';
    card.innerHTML='<div class="nc-label">Siguiente capítulo</div>'+
      '<div class="nc-title"></div>'+
      '<div class="nc-actions"><button class="nc-dismiss">Ahora no</button>'+
      '<a class="nc-go">Reproducir →</a></div>';
    card.querySelector('.nc-title').textContent=nextLink.textContent;
    card.querySelector('.nc-go').setAttribute('href', nextLink.getAttribute('href')+'?autoplay=1');
    document.body.appendChild(card);
    audio.addEventListener('ended',function(){card.classList.add('show');});
    card.querySelector('.nc-dismiss').addEventListener('click',function(){card.classList.remove('show');});
  }
  if(audio && /[?&]autoplay=1/.test(location.search)){
    var go=function(){var p=audio.play();if(p&&p.catch)p.catch(function(){});};
    if(audio.readyState>=2)go(); else audio.addEventListener('loadedmetadata',go,{once:true});
  }
})();
</script>
"""


def patch(html: str) -> str:
    if MARK in html:
        return html
    html = html.replace("html { font-size: 19px;",
                        "html { font-size: calc(19px * var(--font-scale, 1));", 1)
    html = html.replace("html { font-size: 17px; }",
                        "html { font-size: calc(17px * var(--font-scale, 1)); }", 1)
    html = html.replace("<head>", "<head>\n" + MARK + "\n" + HEAD_SCRIPT, 1)
    html = html.replace("</style>", CSS + "</style>", 1)
    html = html.replace('<article class="page">',
                        '<article class="page" id="contenido" tabindex="-1">', 1)
    html = html.replace("<body>", "<body>\n" + BODY_TOP, 1)
    html = html.replace("</body>", JS + "</body>", 1)
    return html


def main():
    if len(sys.argv) < 2:
        raise SystemExit("uso: add_usability.py <archivo.html> [salida.html]")
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) >= 3 else src
    html = src.read_text(encoding="utf-8")
    out = patch(html)
    if out == html and MARK in html:
        print("ya tenía usabilidad-v1, sin cambios:", dst)
    else:
        dst.write_text(out, encoding="utf-8")
        print("usabilidad-v1 inyectada →", dst)


if __name__ == "__main__":
    main()
