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

    'Que todos prefiramos el presente no significa que lo prefiramos todos por igual. Y aquí aparece la distinción que lo cambia todo.',

    'Piense en dos personas que ganan exactamente lo mismo. Al primero, llamémoslo Carlos, apenas le cae el sueldo se le va de las manos: sale a celebrar, compra lo que se le antoja, y para fin de mes no queda nada. El segundo, Juan, cobra el mismo monto, pero antes de tocar el resto aparta una parte —renuncia a algunos gustos de hoy porque tiene los ojos puestos en algo más grande mañana: una casa, un negocio, la tranquilidad de un colchón para los malos tiempos—. Los dos prefieren el presente; ninguno es un asceta que desprecie el disfrute. Pero Juan puede esperar; Carlos, casi nada.',

    'No es que uno tenga preferencia temporal y el otro no —los dos la tienen, como todo el mundo—. Lo que cambia es la intensidad: con cuánta fuerza tira cada uno hacia el presente. Carlos lo descuenta con ferocidad: el mañana apenas pesa frente al hoy. Juan lo descuenta con suavidad: puede mirar lejos sin que el presente lo arrastre. Es la diferencia entre quien no deja pasar un gusto y quien planta un árbol sabiendo que dará sombra dentro de veinte años. Misma fuerza, distinta magnitud —y de esa magnitud, como veremos, depende casi todo lo que una persona, o una sociedad, llega a construir—.',

    'Y esto no es solo cuestión de carácter. La misma persona puede ser paciente un año e impaciente al siguiente, sin que su forma de ser haya cambiado —porque la paciencia no depende solo de quién es uno, sino del suelo que pisa—. Piense en alguien que vive en un país tranquilo, con un trabajo estable y un ahorro que conserva su valor: puede planear a diez años, comprar una casa a treinta, plantar el árbol cuya sombra no disfrutará hasta viejo. Ahora ponga a esa misma persona en un país donde la moneda pierde la mitad de su valor cada año, donde nadie sabe qué reglas regirán mañana. Lo que ahorró para la vejez se evapora mientras lo mira. ¿Qué hace? Lo sensato: dejar de guardar y disfrutar hoy, antes de que también eso se lo quiten. No se volvió derrochadora; el mundo a su alrededor volvió insensato el esperar.',

    'Esa es la regla, y conviene grabarla: cuando el futuro se ve firme, se puede esperar; cuando se ve incierto, la espera se vuelve un lujo que nadie puede pagar. La incertidumbre acorta el horizonte de todos a la vez.',

    'Guarde esta idea, porque es la bisagra de todo el libro: la paciencia de una sociedad no es fija. Depende de las condiciones en que vive. Y entre esas condiciones hay una más silenciosa que todas, tan silenciosa que casi nadie la ve operar —el tipo de dinero que usa—. Si el dinero mismo puede acortarle el horizonte a una sociedad entera, sin que nadie lo decida y sin que casi nadie lo note, entonces moldea su paciencia desde un lugar al que no llega la voluntad de ninguno. Pero a eso llegaremos, a su tiempo.',

    'Note algo de todo lo anterior: casi ningún ejemplo era sobre dinero. El que estudia una carrera en vez de salir a ganar ya; el que entrena el cuerpo cuando preferiría el sofá; el que se muerde la lengua en una pelea para no romper algo que tardó años en construir; el que cría a un hijo con paciencia en lugar de comprar su cariño con permisos fáciles. Todos hacen lo mismo, en el fondo: pagan un costo hoy por algo mejor que solo llega después. Todos están, sin saberlo, ejerciendo su preferencia temporal.',

    'Por eso no es un concepto económico en sentido estrecho. Es una de las claves de la conducta humana entera: define cuánto puede esperar una persona y, por lo tanto, qué puede construir. Y aquí conviene nombrar las cosas con precisión. A esa capacidad de esperar —de descontar el futuro con suavidad, de no dejarse arrastrar por el hoy— los economistas la llaman <em>preferencia temporal baja</em>. Suena al revés de lo que uno esperaría: el que más puede esperar es el que menos tira hacia el presente, y por eso su preferencia es "baja". No significa no preferir el presente —eso, ya lo vimos, es imposible—, sino preferirlo con menos fuerza: poder renunciar a un gusto de hoy porque se tiene la mirada puesta lejos.',

    'Y fíjese en lo que se construye así. Las cosas que más valen —la salud, el conocimiento, la confianza, una obra, el capital— se levantan todas del mismo modo: renunciando a algo hoy, sostenidamente, por algo mayor que solo llega mañana. Quien no puede esperar no puede construir nada de eso. Por eso la baja preferencia temporal es la materia prima de todo lo que dura: ni una vida sólida ni una civilización entera se levantan sin ella. Toda construcción es, en el fondo, paciencia acumulada. La preferencia temporal mide la capacidad de un ser humano —y de una sociedad entera— para construir su futuro.',

    'De todos los terrenos donde la preferencia temporal deja huella, hay uno donde se vuelve visible, medible, y donde se enlaza con el tema de este libro: el económico. No porque sea el más importante —ya vimos que gobierna cosas que pesan mucho más que el dinero—, sino porque es ahí donde la paciencia de millones de personas deja de ser un asunto privado y se vuelve un hecho que se puede observar. Enfoquemos la lente sobre ese terreno; el resto del libro vivirá en él.',

    'Hasta aquí hablamos de una persona y su paciencia. Pero usted no vive solo. Vive entre millones, y cada uno llega al mundo con la suya: unos impacientes, otros pacientes, la mayoría en algún punto intermedio. ¿Qué pasa cuando todas esas paciencias distintas se encuentran?',

    'Pasa algo notable. Los más pacientes —los que están dispuestos a no consumir hoy— tienen recursos ociosos, ahorro que podrían prestar. Y los que quieren construir algo ahora —una casa, un taller, un negocio que tardará en dar fruto— necesitan esos recursos antes de tiempo, y están dispuestos a dar algo a cambio de adelantarlos. Unos tienen espera de sobra; otros tienen prisa. Cuando se encuentran, ocurre lo que ocurre siempre que algo se ofrece y algo se demanda: surge un precio. Un número que dice cuánto hay que ofrecerle a quien tiene paciencia para que entregue hoy lo que podría guardar, a cambio de recibir más mañana.',

    'Ese precio tiene nombre, y usted lo ha oído mil veces sin sospechar que era esto: la tasa de interés. No la palanca que mueven unos funcionarios —esa es otra historia, y la contaremos a su tiempo—, sino el número que nace, solo, del encuentro entre la paciencia de unos y la prisa de otros. Es la preferencia temporal de una sociedad entera, traducida a una sola cifra que cualquiera puede leer.',

    'Y como toda señal de este libro, encierra una promesa y una amenaza. La promesa: dice una verdad que ninguna autoridad podría averiguar por su cuenta —cuánta paciencia, cuánto futuro está dispuesta a financiar una sociedad hoy—. La amenaza: si se puede decir una verdad con un número, también se puede mentir con él. Esa cifra puede falsificarse. Y cuando se falsifica la señal que coordina el ahorro de unos con los proyectos de otros, no se engaña a una persona: se engaña a todos a la vez, en el lenguaje que todos escuchan sin darse cuenta.',

    'Pero antes de ver cómo se corrompe, falta una pieza. Hemos hablado de la paciencia —la disposición a esperar—, pero no de lo que esa espera produce en el mundo real. Cuando alguien ahorra, ¿qué ocurre exactamente? ¿Qué es lo que queda disponible, y para quién? Esa es la pieza que sigue, y sin ella la tasa de interés no se entiende del todo.',
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
               '<a class="prev" href="cuando-un-precio-dice-la-verdad.html">¿Cuándo un precio dice la verdad?</a>'
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
