#!/usr/bin/env python3
"""Construye el cap 4 «Saber esperar» (Primer cimiento, Bloque II).

Reescritura completa del cap. Reemplaza el contenido actual de
preferencia-temporal.html con una versión más concisa y didáctica que
arranca por el ejemplo del millón de pesos y construye hacia el
"hecho universal de la preferencia temporal" de Rothbard.

Estructura:
- Header: eyebrow «Primer cimiento» + h1 «Saber esperar» + subtítulo.
- Prosa corrida (sin secciones), con UNA cita en bloque (Rothbard).
- La atribución va como <cite class="no-audio"> porque el párrafo
  previo ya nombra a Rothbard y la obra.
"""
import re

EYEBROW = "Primer cimiento"
TITLE = "Saber esperar"
SUBTITLE = "Por qué prefiere usted lo bueno ahora —y por qué eso lo explica casi todo"

CONTENT = [
    ("lead",
     "Le ofrezco un millón de pesos. Puede tomarlos ahora mismo, o esperar un año y recibir el mismo millón. ¿Cuál escoge? La pregunta casi ofende de tan obvia: ahora, claro. Nadie en su sano juicio espera un año para recibir exactamente lo mismo que podría tener hoy."),

    'Ahora hagámosla interesante. Para que valga la pena esperar ese año, ¿cuánto tendría que ofrecerle de más? ¿Un millón cien mil? ¿Un millón y medio? ¿El doble? Hay un número —distinto para cada persona— a partir del cual usted diría "bueno, por eso sí espero". Ese número, ese "algo de más" que le exige a la espera, no es un capricho suyo. Es una de las fuerzas más poderosas que gobiernan una economía entera, y casi nadie sabe que la lleva dentro.',

    'Lo que acaba de hacer —preferir lo bueno ahora que después— no es un defecto de carácter ni una debilidad que deba corregir: es la forma misma en que actúa todo ser humano. Entre dos satisfacciones iguales, una hoy y otra dentro de un año, cualquiera toma la de hoy. Entre terminar un trabajo pronto o tarde, prefiere pronto. Entre recibir una buena noticia ahora o en un mes, ahora. No hay que enseñarle esto a nadie; nace con la persona y la acompaña en cada decisión que toma.',

    'Los economistas austriacos le dieron un nombre a esta regla —preferencia temporal— y descubrieron que de ella, de algo tan simple que parece no tener nada que enseñar, se deduce buena parte de cómo funciona una economía. Por qué existe el interés. Por qué unas sociedades acumulan riqueza y otras la consumen. Y —esto es lo que nos ocupará en este libro— por qué el tipo de dinero que una sociedad usa moldea, sin que nadie lo decida, la paciencia de quienes viven en ella.',

    'Vale la pena detenerse en lo primero, porque es más fuerte de lo que parece. No se trata de que casi siempre prefiramos el presente, ni de que la mayoría de la gente lo haga. Se trata de que es imposible actuar sin preferirlo. Y se puede demostrar con un experimento mental sencillo.',

    'Imagine a alguien —llamémoslo el hombre que nunca tiene prisa— para quien disfrutar algo hoy o dentro de un año diera exactamente lo mismo. Le regalan una botella de un vino extraordinario. ¿La abre esta noche? No tiene por qué: mañana le dará el mismo placer, así que la guarda —no pierde nada esperando—. Pero mañana se repite la cuenta, idéntica: ¿hoy o mañana? Y como le da igual, vuelve a guardarla. Y pasado mañana otra vez. Si de verdad el momento le fuera por completo indiferente, ese día de abrir la botella no llegaría jamás: la guardaría para siempre, y moriría sin haberla probado.',

    'El absurdo lo delata. Acumularía sin disfrutar nunca —y eso no tiene sentido, porque el sentido de producir y guardar es, al final, consumir—. Rothbard lo dice sin rodeos:',

    ("quote",
     '"Si un hombre, ceteris paribus, no prefiriera la satisfacción presente a la satisfacción futura, no consumiría... Pero el hecho de \'no consumir nunca\' es un absurdo, ya que el consumo es el fin de toda producción."',
     'Rothbard, <em>El hombre, la economía y el Estado</em>, cap. 1'),

    'El que alguien actúe —el que en algún momento deje de posponer y efectivamente consuma— demuestra que prefiere el presente al futuro. No hace falta medir a nadie ni preguntarle: basta con que actúe. Por eso no es una tendencia estadística que admita excepciones, sino una condición de la acción misma. Rothbard la llama, con razón, el hecho universal de la preferencia temporal.',

    'Aquí mucha gente siente una objeción, y conviene atenderla porque parece sólida. Imagine que estamos en pleno invierno y alguien le ofrece un bloque de hielo: ¿lo quiere ahora o el próximo verano? Casi cualquiera responde "en verano". Y entonces parece que preferimos el futuro al presente —justo lo contrario de lo que acabamos de afirmar—.',

    'Pero mire con cuidado qué se está comparando. El hielo en invierno, cuando hace frío y no sirve para casi nada, y el hielo en verano, cuando refresca y se agradece, no son el mismo bien. Físicamente son idénticos —la misma agua congelada—, pero lo que usted valora no es el objeto físico: es la satisfacción que le produce. Y la satisfacción de "hielo cuando hace calor" es sencillamente distinta —y mayor— que la de "hielo cuando ya tengo frío". No está prefiriendo el futuro al presente. Está prefiriendo un bien mejor a uno peor, y resulta que el mejor llega después.',

    'La regla seguía intacta todo el tiempo: si le ofrecieran la misma satisfacción —ese hielo refrescante de verano— hoy mismo o dentro de un año, la querría hoy. La preferencia temporal no dice que siempre queramos los objetos cuanto antes; dice que, comparando la misma satisfacción en dos momentos, siempre preferimos el momento más cercano. El error de la objeción está en confundir la cosa con el valor que la cosa nos da.',
]


def main():
    parts = [f'<article class="page" id="contenido" tabindex="-1">\n',
             f'\n  <div class="chapter-eyebrow">{EYEBROW}</div>\n',
             f'  <h1 class="chapter-title">{TITLE}</h1>\n',
             f'  <p class="chapter-subtitle">{SUBTITLE}</p>\n',
             '\n  <div class="ornament">• • •</div>\n',
             '\n  <div class="prose">\n']
    for it in CONTENT:
        if isinstance(it, str):
            parts.append(f'    <p>{it}</p>\n')
        elif it[0] == "lead":
            parts.append(f'    <p class="lead">{it[1]}</p>\n')
        elif it[0] == "quote":
            _, qtext, cite = it
            parts.append('\n    <blockquote class="pull-quote">\n')
            parts.append(f'      <p>{qtext}</p>\n')
            parts.append(f'      <cite class="no-audio">{cite}</cite>\n')
            parts.append('    </blockquote>\n\n')
    parts.append('\n  </div>\n\n</article>')
    article = ''.join(parts)

    # Esqueleto del cap 3 (tres-regimenes.html)
    sk = open('tres-regimenes.html', encoding='utf-8').read()
    out = sk
    out = re.sub(r'<title>.*?</title>',
                 '<title>Saber esperar — Arregla el dinero, arregla el mundo</title>',
                 out, count=1, flags=re.DOTALL)
    out = re.sub(r'<article class="page"[^>]*>.*?</article>',
                 lambda _m: article, out, count=1, flags=re.DOTALL)
    new_nav = ('<nav class="nav-foot">'
               '<a class="prev" href="tres-formas-organizar-dinero.html">Las tres formas de organizar el dinero</a>'
               '<a class="idx" href="index.html">Índice</a>'
               '<a class="next" href="ahorro-real.html">Lo que la espera libera</a></nav>')
    out = re.sub(r'<nav class="nav-foot">.*?</nav>',
                 lambda _m: new_nav, out, count=1, flags=re.DOTALL)
    out = out.replace('audio/tres-regimenes.mp3', 'audio/preferencia-temporal.mp3')
    out = out.replace('audio/tres-regimenes.alignment.json',
                      'audio/preferencia-temporal.alignment.json')
    out = out.replace('data-storage-key="tres-regimenes"',
                      'data-storage-key="preferencia-temporal"')

    open('preferencia-temporal.html', 'w', encoding='utf-8').write(out)
    n_par = sum(1 for it in CONTENT if isinstance(it, str) or it[0] == "lead")
    n_q = sum(1 for it in CONTENT if isinstance(it, tuple) and it[0] == "quote")
    print(f"preferencia-temporal.html regenerado: {n_par} párrafos, {n_q} citas")


if __name__ == "__main__":
    main()
