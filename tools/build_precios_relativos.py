#!/usr/bin/env python3
"""Construye el cap 10 «Los precios relativos» (Bloque III, cuarta pieza).

Reescritura completa. Título sigue siendo técnico («Los precios
relativos») porque ya es comprensible; solo cambia el subtítulo y
el contenido. El cap presenta el efecto Cantillon: el dinero nuevo
entra por un punto y reparte riqueza según el orden de llegada,
mientras deforma la malla de precios relativos.

Estructura:
- Header: eyebrow «Cuarta pieza · gravedad media» + h1 «Los precios
  relativos» + subtítulo «El reparto oculto: quién recibe el dinero
  nuevo primero».
- Prosa corrida sin secciones.
- 4 citas en bloque: Rothbard (2) + Mises (2).
- Todas las atribuciones con cite class='no-audio'.

Continúa la plantilla:
- Causa: la creación de dinero de la nada.
- Consecuencia física: el dinero entra por un punto, no cae sobre
  todos a la vez.
- Señal de este cap: los precios RELATIVOS (la malla de proporciones,
  no el precio de una cosa).
- Reacción: redistribución silenciosa de riqueza de los últimos a
  los primeros.
- Daño doble: la malla deforma su información Y reparte la riqueza
  en el mismo gesto.
"""
import re

EYEBROW = "Cuarta pieza · gravedad media"
TITLE = "Los primeros y los últimos"
SUBTITLE = "El reparto oculto: quién recibe el dinero nuevo primero"

CONTENT = [
    ("lead",
     'A usted le ha pasado esto, aunque quizá nunca lo haya puesto en números. Su sueldo subió este año —el aumento de siempre, el que cierra la cuenta de recursos humanos—. Y sin embargo el mercado alcanza para menos, el arriendo se llevó el aumento entero antes de que usted lo estrenara, y en las noticias, ese mismo año, los bancos anuncian utilidades récord. Entonces aparece la pregunta, aunque quizás nunca con estas palabras: ¿por qué, cada vez que se imprime dinero, los que ya están cerca del dinero parecen hacerse más ricos —los bancos, las grandes fortunas, los que tienen activos— mientras a usted la misma inflación lo empobrece? No es mala suerte ni paranoia. Es un mecanismo, ocurre siempre del mismo modo, y tiene nombre. Cuando lo vea funcionar, no podrá dejar de verlo.'),

    '¿Recuerda el agua vertida por la esquina del estanque —la que mojaba primero las orillas cercanas y después las lejanas—? Le prometimos entonces un capítulo entero para ese desfase. Es este. Para cobrarlo, hay que recordar por dónde entra el dinero nuevo: no cae del cielo sobre todos a la vez. Nace en un punto y de ahí fluye hacia afuera siguiendo un camino. Y ese punto no es solo el banco central: son sobre todo los bancos comerciales, que fabrican dinero nuevo cada vez que prestan —habilitados y respaldados por el banco central, pero son ellos quienes abren el grifo—. (A esa fábrica le dedicaremos su propio capítulo más adelante; por ahora basta con saber que el dinero nuevo entra por ahí.) De quien lo crea pasa a su clientela: las grandes empresas, los que tienen acceso al préstamo, los que están en la primera fila. De ahí, poco a poco, va goteando hacia el resto —los proveedores de esas empresas, sus empleados— hasta llegar, al final del recorrido, a la gente común: el asalariado, el pensionado, el que vive de un ingreso fijo. El dinero nuevo recorre la economía como el agua en aquel estanque: moja primero las orillas cercanas a la esquina por donde entra, y llega tarde, y ya diluido, a las orillas lejanas.',

    'Y aquí está el truco que lo cambia todo —y que casi nadie ve—. El que recibe el dinero nuevo <em>primero</em> lo gasta cuando los precios todavía no han subido. Compra a precios viejos, con dinero nuevo. El que lo recibe <em>último</em> se encuentra con que, para cuando le llega, los precios ya subieron —porque todos los que cobraron antes que él ya salieron a comprar y empujaron los precios hacia arriba—. Compra a precios nuevos, después de que el dinero ya perdió valor. El primero hizo su compra barata; el último la hace cara. Y la diferencia entre uno y otro no la paga nadie en una factura visible: se transfiere, en silencio, del último al primero.',

    'Pongámosle los personajes de siempre. Cuando el dinero nuevo entra, los primeros en gastarlo —los bancos que lo fabrican y las grandes empresas que acceden a ese crédito recién creado— salen a comprar: activos, propiedades, materiales. Lo hacen a los precios de ayer, que aún no reaccionan. Juan y Luisa, en cambio, están al final de la fila. Su sueldo sube —si sube— mucho después, cuando el arriendo, la comida y todo lo demás ya se encarecieron. Reciben más pesos nominales, sí, pero compran menos con ellos que antes.',

    'Y usted conoce esa fila por dentro, porque está parado en ella. Su sueldo llega el treinta; cuando llega, el arriendo ya subió, el mercado ya subió, la pensión del colegio ya subió. Usted no hizo nada distinto este año. Solo cobra de último.',

    'No es, entonces, que la impresión de dinero reparta un beneficio para todos —"más dinero circulando, más prosperidad"—. Lo que hace es <em>redistribuir</em>: pasar riqueza de los que llegan tarde a los que llegan temprano. Rothbard la describe como lo que es, una carrera:',

    ("quote",
     '"La inflación es, en efecto, una carrera que consiste en ver quién es capaz de conseguir el dinero antes."',
     'Rothbard, <em>¿Qué ha hecho el gobierno de nuestro dinero?</em>'),

    'Y los que pierden esa carrera siempre son los mismos: los que viven de un ingreso que no se ajusta rápido. Los asalariados, los pensionados, los profesores, quienes dependen de un contrato firmado en pesos de ayer. No porque sean menos hábiles, sino porque están estructuralmente al final de la fila —lejos de la fábrica del dinero—. Por eso la parte más perversa de este mecanismo es que es invisible. Nadie ve la transferencia, porque no hay un ladrón ni una factura. Rothbard lo señala con precisión:',

    ("quote",
     '"Las ganancias para los inflacionistas son visibles y muy notorias, las pérdidas de los demás quedan ocultas e inadvertidas."',
     'Rothbard, <em>El hombre, la economía y el Estado</em>, cap. 12'),

    'El que se enriqueció comprando barato lo ve y lo celebra. El que se empobreció comprando caro no tiene a quién señalar: solo siente, vagamente, que el dinero ya no le alcanza como antes. La causa y el efecto están separados por todo el recorrido del dinero, y por eso casi nadie une los puntos. La injusticia ocurre a plena luz, pero en un lenguaje que nadie aprendió a leer: el de los precios que suben en distinto momento para distinta gente.',

    'Ahora sí, el nombre que el comienzo le prometió. Este mecanismo —el dinero nuevo que entra por un punto y reparte riqueza según el orden de llegada— se llama el efecto Cantillon, por Richard Cantillon, el banquero irlandés del siglo XVIII que lo describió antes que nadie: el primero en notar que el dinero nuevo no llega a todos a la vez, y que en ese desfase —no en la cantidad— es donde vive el daño. Tres siglos después, el mecanismo sigue funcionando idéntico; solo que hoy lo mueve una imprenta infinitamente más rápida. Ya lo vio funcionar. Ahora ya no podrá dejar de verlo.',

    'Detrás de todo esto hay un principio que conviene nombrar, porque es la raíz teórica de todo el capítulo. Solemos imaginar que imprimir dinero "sube los precios" —como si todos subieran a la vez, parejo, igual que sube la marea—. Si fuera así, la inflación sería injusta pero no tramposa: todos perderían lo mismo. Pero no es así, y nunca lo es. El dinero nuevo entra por un punto y se mueve por etapas, así que los precios suben en desorden —unos antes, otros después, unos más, otros menos—. Mises lo formuló con una claridad definitiva:',

    ("quote",
     '"Las variaciones experimentadas por la relación monetaria... no afectan al mismo tiempo ni en la misma proporción a los precios de los diversos bienes y servicios. De ahí que afecten de forma diferente a la riqueza de los distintos individuos."',
     'Mises, <em>La acción humana</em>, cap. XVII'),

    'Esa última frase es la llave: <em>afectan de forma diferente a la riqueza de los distintos individuos</em>. Como el dinero no es neutral —no sube todos los precios por igual—, su inyección no es un simple cambio de escala: es un reparto. Cambia quién tiene qué. Mises insistía en que pretender lo contrario —un dinero que se pudiera inyectar sin alterar la posición relativa de nadie— es una fantasía:',

    ("quote",
     '"El dinero es un elemento de acción y, por tanto, generador de cambio... Todos los planes que pretenden hacer neutro y estable el dinero son contradictorios."',
     'Mises, <em>La acción humana</em>, cap. XVII'),

    'Recoja ahora la forma, porque es la de siempre con una señal nueva. La señal de este capítulo son los precios relativos —no el precio de una cosa, sino la proporción entre todos los precios: cuánto cuesta el pan respecto a la casa, el trabajo respecto al acero, lo de hoy respecto a lo de mañana—. Esa malla de proporciones es la que le dice a cada uno qué es escaso y qué es abundante, dónde conviene producir y dónde no. Cuando el dinero es honesto, los precios relativos se mueven solo cuando cambia algo real —cuando de verdad hay más trigo o menos petróleo—, y entonces dicen la verdad sobre el mundo. Cuando el dinero se crea de la nada, los precios se mueven por el mero orden en que el dinero nuevo va llegando —no porque algo real cambiara, sino porque unos cobraron antes que otros—. La malla de precios se deforma según el recorrido del dinero, y al deformarse, miente: dice que algo cambió cuando lo único que pasó es que el dinero entró por un lado y no por otro.',

    'Y aquí conviene detenerse en el otro lado, porque es lo que revela la raíz del problema. Todo lo que acaba de leer —la carrera, los primeros y los últimos, el reparto silencioso— depende de una sola condición: que exista dinero nuevo entrando por un punto. Quítela, y el mecanismo entero desaparece. Con dinero duro, donde nadie puede crear unidades de la nada, no hay un punto por donde se inyecte el dinero fresco, no hay primer receptor ni último, no hay carrera que correr. La cantidad de dinero no se expande desde el escritorio de nadie, así que los precios relativos solo se mueven cuando cambia algo real en el mundo —una cosecha mejor, un pozo agotado, un invento—. No es que el dinero duro reparta la riqueza de forma más justa: es que no la reparte en absoluto, porque no hay reparto que hacer. El efecto Cantillon no es una injusticia que el dinero honesto corrija; es una injusticia que el dinero honesto, sencillamente, no puede producir. Nace entera de la posibilidad de crear dinero de la nada —y muere con ella—.',

    'Note que aquí el dinero deshonesto hace dos daños a la vez, no uno. Mancha la señal —los precios relativos dejan de reflejar la escasez real— y, en el mismo gesto, redistribuye la riqueza de los últimos a los primeros. La distorsión de la información y la injusticia no son dos problemas separados: son la misma cosa vista por dos caras. El reparto ocurre <em>a través</em> de la mentira en los precios.',

    'Hasta aquí, todas las señales que hemos visto comparten un supuesto que conviene ahora poner sobre la mesa: que el dinero, al menos, se mantiene reconocible de un año para otro —que sirve para comparar, para calcular, para mirar lejos—. Pero ¿y si el propio dinero, su cantidad futura, fuera incierto? ¿Cómo se planea a diez años sobre algo cuya cantidad nadie puede predecir? Esa es la siguiente pieza —la predictibilidad del dinero mismo—, y es donde, por primera vez, los dos dineros honestos que hasta ahora hemos tratado como uno solo empezarán a mostrar sus diferencias.',
]


def main():
    parts = ['<article class="page" id="contenido" tabindex="-1">\n',
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

    sk = open('tres-regimenes.html', encoding='utf-8').read()
    out = sk
    out = re.sub(r'<title>.*?</title>',
                 '<title>Los primeros y los últimos — Arregla el dinero, arregla el mundo</title>',
                 out, count=1, flags=re.DOTALL)
    out = re.sub(r'<article class="page"[^>]*>.*?</article>',
                 lambda _m: article, out, count=1, flags=re.DOTALL)
    new_nav = ('<nav class="nav-foot">'
               '<a class="prev" href="deteccion-mala-inversion.html">El dolor que avisa</a>'
               '<a class="idx" href="index.html">Índice</a>'
               '<a class="next" href="predictibilidad-estructural.html">La predecibilidad del dinero</a></nav>')
    out = re.sub(r'<nav class="nav-foot">.*?</nav>',
                 lambda _m: new_nav, out, count=1, flags=re.DOTALL)
    out = out.replace('audio/tres-regimenes.mp3', 'audio/precios-relativos.mp3')
    out = out.replace('audio/tres-regimenes.alignment.json',
                      'audio/precios-relativos.alignment.json')
    out = out.replace('data-storage-key="tres-regimenes"',
                      'data-storage-key="precios-relativos"')

    open('precios-relativos.html', 'w', encoding='utf-8').write(out)
    n_par = sum(1 for it in CONTENT if isinstance(it, str) or (isinstance(it, tuple) and it[0] == "lead"))
    n_q = sum(1 for it in CONTENT if isinstance(it, tuple) and it[0] == "quote")
    print(f"precios-relativos.html regenerado: {n_par} párrafos, {n_q} citas")


if __name__ == "__main__":
    main()
