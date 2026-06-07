#!/usr/bin/env python3
"""Construye el capítulo «La degradación alimentaria» (Bloque IV · cap 15)
usando el esqueleto del cap 3. Prosa con 2 subtítulos de sección.

Nota de continuidad: el texto del usuario decía «el pueblo de Tomás —el del
nogal—», pero el protagonista del cap 14 ya quedó como Francisco. Lo cambio
aquí también para mantener la narrativa del libro coherente."""
import re

EYEBROW = "Cuarta consecuencia · lo más visible"
TITLE = "La degradación alimentaria"
SUBTITLE = "Por qué su comida es cada vez más abundante y más vacía"

# (section_title or None, [items])
# items: ("lead", txt) | "texto"
CONTENT = [
    (None, [
        ("lead", 'Esta noche usted va a comer, y lo más probable es que coma bien —al menos eso parece—. Habrá comida de sobra: más barata, más abundante, más variada que la que comieron sus abuelos. Por casi cualquier medida visible, la mesa de hoy le gana a la de hace un siglo. Le dirán, y es cierto, que nunca en la historia tanta gente tuvo tanto que comer.'),
        'Y sin embargo, algo no cuadra. Nunca hubo tanta comida, y nunca estuvimos tan enfermos de cosas que vienen de comer: obesidad donde antes había hambre, diabetes en gente joven, una población entera que come y come y sigue, de algún modo, insatisfecha. La explicación cómoda ya la conoce, porque se la repiten todos los días: comemos mal por glotonería, por falta de voluntad, por pereza, por no informarnos. El problema —dicen— es suyo. Coma menos, muévase más, lea la etiqueta.',
        'Esa explicación es cómoda por la misma razón que lo era la del talador avaro: reparte la culpa entre millones de individuos débiles y deja intacto el sistema que les puso ese plato delante. Y como casi todas las explicaciones cómodas, esconde lo que de verdad importa. Porque la pregunta que nadie hace no es por qué usted come lo que come. Es otra, una que se decide mucho antes de que usted entre a la cocina: ¿por qué lo barato, lo abundante, lo que llena los estantes, es justamente lo más vacío? ¿Quién decidió que el alimento del mundo se inclinara hacia ahí?',
        'Nadie lo decidió —y a la vez, algo lo decidió—. No se decide en su cocina. Se decide mucho antes, en una cuenta que hace alguien que usted nunca ve: el que cultiva lo que usted come. Para entenderlo hay que dejar de mirar el plato y empezar a mirar el suelo del que ese plato salió.',
    ]),
    ("El hombre del suelo", [
        'Imagine otra vez al pueblo de Francisco —el del nogal— y mire ahora al vecino de al lado. Llamémoslo Andrés. Andrés tiene un campo que heredó, como Francisco heredó su árbol. De ese campo ha sacado de comer toda su vida, y antes su padre, y antes su abuelo.',
        'Andrés sabe algo que ningún manual le enseñó, que aprendió mirando trabajar a su padre: que su campo no es solo tierra, es un manantial. Si lo cuida —si lo deja descansar cada cierto tiempo, si alterna las siembras, si mete el ganado a pastar para que abone y la tierra recupere lo que la cosecha le sacó—, el campo le dará de comer todos los años, sin falta, y se lo dará después a sus hijos. El suelo bien cuidado es como el nogal de Francisco: una fuente que mana mientras no la agotes. Cuidarlo cuesta —cuesta paciencia, cuesta dejar una parcela quieta un año que podría estar produciendo, cuesta criar ganado que rinde poco y lento—. Pero a cambio el manantial no se seca nunca.',
        'Andrés tiene delante, sin saber que la tiene, la misma cuenta que Francisco. Puede tratar su tierra como un manantial —sacarle una cosecha sostenible cada año, para siempre— o puede tratarla como un balde: exprimirla al máximo ahora, sembrar lo mismo una y otra vez sin descanso, sacar tres cosechas donde debería sacar una, y vaciarla. El balde da mucho de golpe. Después queda seco.',
        'Fíjese, igual que con Francisco, en qué sostiene la decisión de cuidar. No es que Andrés ame la tierra —aunque la ame—. No es virtud ecológica ni sabiduría ancestral. Es una cuenta: cuidar el suelo solo conviene si Andrés puede confiar en que habrá un mañana que se parezca al hoy —en que sus cosechas futuras seguirán valiendo, en que sus hijos heredarán tierra viva y no polvo—. Cuando el futuro es firme, la cuenta premia conservar el manantial. Andrés cuida su campo por exactamente la misma razón por la que Juan guardaba parte del sueldo y Francisco no vendía el nogal: porque esperar valía la pena.',
    ]),
    ("Cámbiele una sola cosa", [
        'No le toque nada a Andrés. Déjele su conocimiento, su cariño por la tierra, su deseo de dejarles algo a los hijos. No lo vuelva ignorante ni codicioso. Cámbiele una sola cosa, la más invisible de todas: el dinero en que cobra sus cosechas.',
        'Ya sabe lo que ese cambio le hace a una cuenta —lo vio entero en la pieza de la asignación intertemporal—. Cuando el dinero se diluye año tras año, el futuro deja de ser un manantial confiable y se vuelve una promesa escrita en tinta que se borra.',
        'Aquí mucha gente siente, con razón, una objeción —y vale la pena atenderla, porque parece deshacer todo el argumento—. Si el dinero pierde valor, ¿no sería más sensato que Andrés no vaciara su tierra? Al fin y al cabo, un suelo fértil es riqueza real, de la que aguanta la diluición; mientras el dinero se evapora en el bolsillo, la tierra viva sigue valiendo. ¿No debería entonces el dinero blando empujarlo a cuidar el manantial con más celo que nunca?',
        'Parece sólido, hasta que se mira de cerca qué es lo que Andrés cobra. Andrés no vive de tener tierra; vive de vender lo que la tierra produce. Y ahí está la trampa: la cosecha de más que arranca hoy, exprimiendo el suelo, la cobra hoy, en dinero que todavía vale. Las cosechas que conservaría cuidando el manantial le llegarían dentro de diez, veinte, treinta años —en un dinero que para entonces no valdrá casi nada—. El dinero blando no le miente sobre cuánto vale su tierra: le miente sobre cuándo conviene cobrarla. Y la respuesta que le susurra es siempre la misma: ahora, todo, antes de que el número se borre. La tierra conserva su valor, sí —pero el dinero castiga al que espera para cobrarlo, y premia al que lo arranca ya—. La cuenta se da vuelta entera. Y no porque Andrés haya cambiado, sino porque cambió lo único con que calculaba.',
        'Andrés empieza a tratar su manantial como un balde. Siembra lo mismo todos los años sin dejar descansar la tierra. Saca el ganado, porque rinde lento y ya no puede permitirse lo lento. Le exige al campo más de lo que el campo puede reponer. Y cuando la tierra, exhausta, empieza a rendir menos, no la deja sanar: le echa fertilizante comprado, que la obliga a seguir pariendo cosechas sobre un suelo que por dentro ya está muerto. El campo sigue verde por fuera. Por dentro es un balde casi vacío al que se le echa agua de afuera para que parezca lleno.',
        'Aquí conviene detenerse, porque esto es lo que cierra el círculo hasta su plato. Un suelo agotado no deja de producir —produce, mientras le echen fertilizante—. Pero produce distinto. La planta crece rápida, grande, abundante; solo que crece sobre una tierra que ya no tiene casi nada que pasarle. Sale comida con la forma de siempre y cada vez menos de lo que hacía que esa comida alimentara. Abundante por fuera, vacía por dentro —igual que el suelo del que vino—. La cosecha se parece, peldaño por peldaño, al dinero con que se cobró: más cantidad, menos sustancia. Por eso su mesa de esta noche puede tener más que nunca y nutrir menos que nunca. No es una paradoja. Es la misma cuenta de Andrés, servida en su plato.',
    ]),
]

# ---- Construir el HTML del article ----
parts = ['<article class="page" id="contenido" tabindex="-1">\n',
         f'\n  <div class="chapter-eyebrow">{EYEBROW}</div>\n',
         f'  <h1 class="chapter-title">{TITLE}</h1>\n',
         f'  <p class="chapter-subtitle">{SUBTITLE}</p>\n',
         '\n  <div class="ornament">• • •</div>\n',
         '\n  <div class="prose">\n']
for sec_title, items in CONTENT:
    if sec_title:
        parts.append(f'\n    <span class="section-num">{sec_title}</span>\n')
    for it in items:
        if isinstance(it, str):
            parts.append(f'    <p>{it}</p>\n')
        elif it[0] == "lead":
            parts.append(f'    <p class="lead">{it[1]}</p>\n')
parts.append('\n  </div>\n\n</article>')
article = ''.join(parts)

# ---- Esqueleto del cap 3 ----
sk = open('tres-regimenes.html', encoding='utf-8').read()
out = sk
out = re.sub(r'<title>.*?</title>',
             '<title>La degradación alimentaria — Arregla el dinero, arregla el mundo</title>',
             out, count=1, flags=re.DOTALL)
out = re.sub(r'<article class="page"[^>]*>.*?</article>', lambda _m: article, out, count=1, flags=re.DOTALL)
# nav-foot: prev = deforestación; next vacío (cap 16 aún no existe)
new_nav = ('<nav class="nav-foot">'
           '<a class="prev" href="deforestacion.html">La deforestación</a>'
           '<a class="idx" href="index.html">Índice</a>'
           '<span></span></nav>')
out = re.sub(r'<nav class="nav-foot">.*?</nav>', lambda _m: new_nav, out, count=1, flags=re.DOTALL)
# identificadores de audio
out = out.replace('audio/tres-regimenes.mp3', 'audio/degradacion-alimentaria.mp3')
out = out.replace('audio/tres-regimenes.alignment.json', 'audio/degradacion-alimentaria.alignment.json')
out = out.replace('data-storage-key="tres-regimenes"', 'data-storage-key="degradacion-alimentaria"')

open('degradacion-alimentaria.html', 'w', encoding='utf-8').write(out)
n_par = sum(1 for s, items in CONTENT for it in items if isinstance(it, str) or it[0] == "lead")
n_sec = sum(1 for s, _ in CONTENT if s)
print("degradacion-alimentaria.html creado")
print(f"párrafos: {n_par} | secciones: {n_sec}")
