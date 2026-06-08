#!/usr/bin/env python3
"""Construye «Las tres formas de organizar el dinero» — VERSIÓN CORREGIDA
del cap 3 del Bloque I. NO reemplaza al cap 3 original (tres-regimenes.html):
es una versión alternativa que coexiste con la original, enlazada desde el
índice con un estado «Corrección» en rojo.

Estructura: lead + 1 subtítulo de sección con 2 párrafos."""
import re

EYEBROW = "Bloque I · Fundamentos · corrección"
TITLE = "Las tres formas de organizar el dinero"
SUBTITLE = "Tres maneras, dos resultados"

# (section_title or None, [items])
# items: ("lead", txt) | "texto"
CONTENT = [
    (None, [
        ("lead", 'Saque un billete del bolsillo y véalo de frente. O mire el saldo de su cuenta bancaria en su teléfono, da igual. Esa cifra le promete algo: que con ella podrá comprar mañana más o menos lo mismo que hoy, que no se va a evaporar entre sus manos. Usted confía en esa promesa todos los días sin pensarlo —tiene que confiar, no le queda otra—. La pregunta de este capítulo es si esa promesa es verdadera. Porque hay dinero que no puede mentirle, y hay dinero que miente. Y desde donde usted está, con el billete en la mano, no hay forma de notar la diferencia. Pero la hay, y lo cambia todo.'),
    ]),
    ("¿Qué significa que el dinero mienta?", [
        '¿Cómo puede mentir una cifra? Pensémoslo con un caso extremo, que es como mejor se ve. Imagine que esta noche, mientras todos duermen, la cantidad de dinero del país se duplica: cada billete, cada cuenta, ahora marca el doble. ¿Amaneció el país dos veces más rico? No hay un solo pan más, ni un par de zapatos más, ni una casa más que ayer. Lo único que cambió fue el número. Y como ahora hay el doble de dinero persiguiendo las mismas cosas de siempre, los precios no tardan en acomodarse: todo termina costando el doble, y usted volvió al punto de partida —o peor, porque ese dinero nuevo no le llegó a usted primero—. Ahí está la mentira, a plena luz: el dinero anunció que había el doble de riqueza, y era falso. No la dijo con palabras; la dijo con cantidad. Un dinero dice la verdad cuando la cantidad que hay corresponde a cosas que de verdad se produjeron; miente cuando aparecen cifras nuevas que no corresponden a nada. Y lo que usted acaba de ver —los precios que suben— es apenas la cara visible de esa mentira: por debajo desordena cosas mucho más hondas, de las que se ocupará buena parte de este libro.',

        'Eso que el dinero falso traiciona tiene la forma de un acuerdo tan elemental que casi nunca se dice en voz alta:',

        ("lema", 'El dinero no se crea de la nada: se produce.'),

        'Dicho de otro modo: el dinero solo debería entrar por una puerta, la de la producción —arrancar el oro a la tierra, minar un bitcoin, fabricar algo que alguien quiera—. Por esa puerta, para llevarse una unidad de dinero hay que dejar, a cambio, algo real. El dinero honesto tiene solo esa entrada. El dinero deshonesto tiene una segunda puerta, una que no da a ningún taller ni a ninguna mina —y no importa quién la abra: puede ser el sello de un gobierno o la firma de un banco privado—. Por ella entran unidades nuevas sin que nadie haya producido nada, y quien las emite se lleva un valor que no creó, restándoselo, sin que se note, a todos los que sí lo crearon.',
    ]),
    ("Tres maneras de tratar el acuerdo", [
        'A lo largo de la historia, la humanidad ha organizado su dinero de tres maneras —lo que los economistas llaman regímenes monetarios—, y se distinguen por cómo tratan ese acuerdo. Una lo respeta por completo: nadie puede crear dinero de la nada. Otra lo rompe a medias, casi sin proponérselo. Y la tercera lo rompe del todo. Tres maneras distintas; pero, para lo único que aquí importa —si el dinero dice la verdad—, solo dan dos resultados: o se respeta el acuerdo, o se rompe. Empezaremos por los dos extremos, donde todo se ve más nítido, y dejaremos para el final el caso del medio, que es donde se esconde la lección más fina de todas.',
    ]),
]

# ---- Construir el HTML del article ----
parts = ['<article class="page" id="contenido" tabindex="-1">\n',
         f'\n  <div class="chapter-eyebrow">{EYEBROW}</div>\n',
         f'  <h1 class="chapter-title">{TITLE}</h1>\n',
         f'  <p class="chapter-subtitle">{SUBTITLE}</p>\n',
         '\n  <div class="ornament">• •</div>\n',
         '\n  <div class="prose">\n']
for sec_title, items in CONTENT:
    if sec_title:
        parts.append(f'\n    <span class="section-num">{sec_title}</span>\n')
    for it in items:
        if isinstance(it, str):
            parts.append(f'    <p>{it}</p>\n')
        elif it[0] == "lead":
            parts.append(f'    <p class="lead">{it[1]}</p>\n')
        elif it[0] == "lema":
            # Máxima destacada: centrada, cursiva, con filetes finos arriba y
            # abajo (variante B del mockup, eco visual de la bisagra del oro).
            # CSS específico de .lema más abajo, sobrescribe el blockquote base.
            parts.append(f'    <blockquote class="lema">{it[1]}</blockquote>\n')
parts.append('\n  </div>\n\n</article>')
article = ''.join(parts)

# CSS de .lema — sobrescribe el blockquote base del esqueleto del cap 3
# para que la máxima quede centrada, con filetes finos arriba/abajo
# (formato definitivo, elegido como variante B en mockups-lemas).
EXTRA_CSS = """
/* ===== Máxima destacada: centrada, con filetes finos arriba y abajo ===== */
blockquote.lema {
  margin: 2.8rem 0; padding: 1.4rem 1rem;
  border-left: none;
  border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule);
  text-align: center; font-style: italic;
  font-size: 1.18rem; line-height: 1.5; color: var(--ink);
}
"""

# ---- Esqueleto del cap 3 ----
sk = open('tres-regimenes.html', encoding='utf-8').read()
out = sk
out = re.sub(r'<title>.*?</title>',
             '<title>Las tres formas de organizar el dinero — Arregla el dinero, arregla el mundo</title>',
             out, count=1, flags=re.DOTALL)
out = re.sub(r'<article class="page"[^>]*>.*?</article>', lambda _m: article, out, count=1, flags=re.DOTALL)
# nav-foot: prev = criterio-de-evaluacion (cap 2); next = preferencia-temporal (cap 4)
new_nav = ('<nav class="nav-foot">'
           '<a class="prev" href="criterio-de-evaluacion.html">El criterio de evaluación</a>'
           '<a class="idx" href="index.html">Índice</a>'
           '<a class="next" href="preferencia-temporal.html">La preferencia temporal</a></nav>')
out = re.sub(r'<nav class="nav-foot">.*?</nav>', lambda _m: new_nav, out, count=1, flags=re.DOTALL)
# CSS de .lema antes de </style>
out = out.replace('</style>', EXTRA_CSS + '</style>', 1)
# identificadores de audio
out = out.replace('audio/tres-regimenes.mp3', 'audio/tres-formas-organizar-dinero.mp3')
out = out.replace('audio/tres-regimenes.alignment.json', 'audio/tres-formas-organizar-dinero.alignment.json')
out = out.replace('data-storage-key="tres-regimenes"', 'data-storage-key="tres-formas-organizar-dinero"')

open('tres-formas-organizar-dinero.html', 'w', encoding='utf-8').write(out)
n_par = sum(1 for s, items in CONTENT for it in items if isinstance(it, str) or it[0] == "lead")
n_sec = sum(1 for s, _ in CONTENT if s)
print("tres-formas-organizar-dinero.html creado")
print(f"párrafos: {n_par} | secciones: {n_sec}")
