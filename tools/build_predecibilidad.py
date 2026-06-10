#!/usr/bin/env python3
"""Construye el cap 11 «La predecibilidad del dinero» (Bloque III, quinta pieza).

Reescritura completa. El título cambia sutilmente de «La predictibilidad
del dinero» a «La predecibilidad del dinero» — más natural en español.
El slug del archivo se mantiene: predictibilidad-estructural.html
(preservando URLs y nav-foots).

Este es el cap del DESACOPLE oro/Bitcoin: hasta aquí los hemos
tratado como uno solo (ambos honestos); aquí, por primera vez, se
separan — no en honestidad sino en predecibilidad de la cantidad.

Estructura:
- Header: eyebrow «Quinta pieza · gravedad media» + h1 «La
  predecibilidad del dinero» + subtítulo «Por qué para construir
  el futuro hay que poder leerlo».
- Prosa corrida sin secciones.
- 2 citas en bloque, ambas de Mises, La acción humana (cap. El
  cálculo económico).
- Atribuciones con cite class='no-audio'.

Arco narrativo:
1. El nogal a 40 años: la apuesta más larga.
2. Calcular el futuro exige una cinta que no cambie.
3. Legible ≠ quieto. Mises: el cálculo NO exige estabilidad.
4. El metáfora de la mesa y la cinta: dos formas de subir el número.
5. Falsificación callada: la cantidad futura del dinero fiat es
   imposible de saber.
6. Aquí, por primera vez, el oro y Bitcoin se separan.
7. El oro: honesto, pero de cantidad incierta.
8. Mises: el oro cumplió la función durante siglos.
9. Bitcoin: honesto Y de cantidad fija/conocida.
10. La objeción honesta: «¿Bitcoin predecible? Si su precio sube
    y baja como una montaña rusa.»
11. Distinguir precio de cantidad. La cinta es la cantidad, no el
    precio.
12. La volatilidad de Bitcoin entra por la demanda, no por la
    oferta. El fiat al revés: precio quieto, cantidad traicionera.
13. Recoja la forma — la pieza es una propiedad del dinero mismo,
    no una señal sobre el mundo (la regla del cap 9 v2 sobre cómo
    nombrar las piezas de los últimos caps).
14. Conclusión: Bitcoin es la única cinta honesta Y con tamaño fijo.
15. Apertura cap 12: lo que ya tienes en la mano también encoge.
"""
import re

EYEBROW = "Quinta pieza · gravedad media"
TITLE = "La cinta métrica"
TITLE_TECNICO = "La predecibilidad del dinero"
SUBTITLE = "Por qué para construir el futuro hay que poder medirlo"

CONTENT = [
    ("lead",
     'Plante un nogal. Hágalo en serio, aunque sea con la imaginación: abra el hueco, acomode la raíz, apriete la tierra. Acaba de hacer una de las apuestas más largas que un ser humano puede hacer —y sabe algo al hacerla: usted no comerá esas nueces—. Un nogal tarda treinta, cuarenta años en dar fruto pleno. Lo está plantando para sus nietos, o para venderle la madera a alguien que todavía no nace. Y por eso mismo el árbol lo obliga a una pregunta que las decisiones cortas no exigen: ¿cómo calcula uno algo a cuarenta años?'),

    'Porque al plantarlo, usted hace cuentas. Cuánto le costará cuidarlo, cuánto valdrá la madera cuando esté lista, si conviene dedicarle esa tierra en vez de a un cultivo que rinda el año entrante. Y todas sus cuentas tienen algo en común: están hechas en dinero, y se proyectan hacia un futuro lejano. Está apostando a que el esfuerzo de hoy tendrá sentido dentro de cuatro décadas. Para que esa apuesta no sea una lotería, necesita algo en lo que casi nunca reparamos: que la unidad con la que mide —el dinero— signifique, dentro de cuarenta años, algo reconocible. Que la cinta métrica con la que calcula hoy mida igual mañana.',

    'Detengámonos en eso, porque es la condición silenciosa de toda decisión larga. No solo su nogal: la carrera de seis años que usted estudió —o que todavía está pagando—, la hipoteca que firmó a treinta, la fábrica que alguien levanta sabiendo que se paga en veinte, la pensión que le prometieron cobrar en medio siglo. Todas son apuestas sobre el futuro lejano, y todas se calculan en dinero. Ninguna es posible si la unidad de medida puede cambiar de tamaño sin aviso entre el día que uno calcula y el día que cosecha. Y fíjese en que usted no necesita que el futuro sea próspero —eso nadie se lo puede garantizar—. Necesita algo más modesto y más fundamental: que el futuro sea <em>legible</em>. Que pueda calcularlo.',

    '¿Y de qué depende que el futuro sea legible? Aquí hay que afinar, porque es fácil confundirse —y la confusión es justo la que desarmamos en un capítulo anterior—. Legible no quiere decir quieto. No se trata de que los precios no se muevan; ya vimos que un precio que se mueve está haciendo su trabajo, contándonos que algo cambió en el mundo. Un futuro legible no es un futuro sin cambios. Es un futuro en el que los cambios que uno ve son cambios reales, y no sustos provocados por la propia cinta métrica con que mide.',

    'Mises lo dejó dicho con todas las letras, y conviene tenerlo presente, porque desmonta de raíz una confusión muy extendida —la de creer que un buen dinero es el de precios quietos—:',

    ("quote",
     '"El cálculo económico no exige la estabilidad monetaria... El funcionamiento del cálculo económico sólo precisa de un sistema monetario inmune a la interferencia estatal."',
     'Mises, <em>La acción humana</em>, El cálculo económico'),

    'Lo que el cálculo necesita, entonces, no es que los precios no se muevan —eso es imposible y además indeseable, porque mataría la información—. Lo que necesita es que nadie pueda meterle mano a la cantidad de dinero: que la cinta no la encoja una autoridad por decreto.',

    'Vuelva a su nogal. A usted no le hace falta saber qué pasará en cuarenta años —ningún dinero del mundo le daría esa bola de cristal—. Lo que necesita es más sutil: confiar en que, cuando llegue el momento de cosechar, podrá <em>leer</em> lo que pasó. Que si la madera vale más, sea porque de verdad escaseó o se volvió más deseada —información que usted podrá usar—, y no porque entretanto se fabricaron montañas de dinero que inflaron todos los números sin que nada real cambiara. Usted no pide un mundo inmóvil. Pide una cinta que no cambie de tamaño.',

    'Porque ese es el punto: una cinta métrica solo sirve si conserva su tamaño. Una cinta que cambia de tamaño sin aviso no mide; engaña con apariencia de medir. Y un dinero cuya cantidad puede cambiar sin que nadie lo prevea es exactamente eso: una cinta de tamaño incierto.',

    'A esa firmeza de la cinta —no a la quietud de lo que mide— la llamaremos predecibilidad del dinero; o, con más precisión, predecibilidad <em>estructural</em>, porque no se trata de que los precios estén quietos, sino de que la estructura misma del dinero —cuánto habrá— sea conocida de antemano. Es la condición de fondo que permite el cálculo a largo plazo: no saber qué traerá el futuro, sino confiar en que la unidad con la que lo calculamos seguirá significando lo mismo cuando el futuro llegue. Es la diferencia entre un mundo que cambia y se puede leer, y un mundo que cambia y además se mide con una cinta de goma que alguien encoge a su antojo. Mises lo reducía a una sola exigencia de fondo: lo único que la buena marcha del cálculo pide es que no haya variaciones graves y bruscas en la cantidad de dinero. No la quietud de los precios: la firmeza de la cantidad. Toda la diferencia del mundo cabe en esa distinción.',

    'Ya sabemos qué dinero le cambia el tamaño a la cinta, porque lo venimos viendo desde el principio del libro: el que se puede crear de la nada. En un dinero honesto, nadie puede inflar la cantidad con una orden —no hay una palanca que alguien accione para fabricar unidades por decreto—, y por eso su cinta no la puede encoger nadie a voluntad: su tamaño no depende de lo que decida ninguna autoridad. Pero el dinero fiat lleva adentro, justamente, esa palanca —la posibilidad de crear unidades nuevas de la nada, por decisión de quien manda—. Cuántos pesos, cuántos dólares habrá dentro de diez, veinte, cuarenta años, no lo decide ninguna ley de la naturaleza ni ningún límite infranqueable: lo decide un comité. Y un comité puede cambiar de opinión.',

    'Vale la pena detenerse aquí, porque hay algo que se vuelve cristalino justo en este punto —y que cambia para siempre cómo se lee un precio—. Imagine que usted mide una mesa con una cinta métrica y obtiene un metro veinte. Al año siguiente la mide otra vez y obtiene un metro y medio. El número subió. ¿Qué pasó? Hay exactamente dos posibilidades, y son opuestas.',

    'La primera: <strong>la mesa creció</strong>. Alguien le añadió madera, de verdad es más grande que antes. La cinta es la misma de siempre, mide bien, y el número mayor le está diciendo una verdad sobre la mesa. Esto es lo que pasa cuando hay un shock real: una plaga arrasa los bosques, la madera se vuelve de verdad más escasa, y su precio sube. El número subió porque la cosa cambió. La cinta no se tocó.',

    'La segunda: <strong>la cinta encogió</strong>. La mesa está intacta, idéntica a la del año pasado —pero la cinta con que la mide se achicó, de modo que la misma mesa ahora arroja un número mayor—. Esto es lo que pasa cuando crece la masa monetaria: se crea dinero nuevo, cada unidad vale menos —la cinta menguó—, y entonces <em>todos</em> los precios suben aunque ninguna cosa haya cambiado. La madera está igual que ayer; lo que se encogió fue el metro con que le pone precio.',

    'Ahí está lo decisivo, y es lo que casi nadie ve: en los dos casos el número subió de un metro veinte a un metro y medio. Idéntico resultado. Si usted solo mira el número —solo el precio—, no tiene cómo saber cuál de las dos cosas ocurrió: si la mesa creció o si la cinta encogió, si la madera de verdad escaseó o si simplemente diluyeron el dinero. El precio, por sí solo, no se lo dice. Y de esa indistinción vive toda la falsificación monetaria: el dinero que se imprime encoge la cinta, pero el número que sube se parece exactamente al de una escasez real. La inflación se disfraza de mundo cambiante.',

    '¿Cómo se distinguen, entonces? Por lo que ya aprendió a leer. Si subió <em>esa</em> mesa y unas pocas cosas más, mientras otras bajaron, fue el mundo: cambiaron las cosas, la cinta está sana. Si suben <em>todas</em> las mesas a la vez, todos los precios juntos y sostenidamente, sin que nada real lo explique, fue la cinta: se encogió la unidad, y el dinero se está diluyendo. Una cosa que cambia deja un rastro disparejo; una cinta que encoge mueve todo en bloque. Esa es la huella que delata cuál de los dos ocurrió.',

    'Ahí está la falsificación propia de esta pieza, y es más callada que las anteriores. No es un precio puntual que miente, como en los capítulos pasados. Es algo de fondo: la cantidad futura del dinero —el tamaño que tendrá la cinta cuando usted vaya a cosechar— se vuelve imposible de saber. No porque sea un secreto, sino porque literalmente no está decidido: depende de elecciones que nadie ha tomado todavía, de presiones políticas que aún no existen, de la próxima crisis y de cómo reaccione a ella quien mande entonces. Usted no puede calcular sobre eso, porque no hay nada firme sobre lo cual calcular.',

    'Vuelva a su nogal, ahora bajo este dinero. Usted hace sus cuentas a cuarenta años —cuánto valdrá la madera, si compensa el esfuerzo—, pero todas sus cuentas penden de un hilo que usted no controla ni puede prever: cuánto dinero habrá creado, para entonces, la autoridad de turno. Si crearon poco, sus números más o menos se sostienen. Si crearon mucho —y la historia del dinero fiat es la historia de crear cada vez más—, el número que usted calculó como ganancia puede haberse vuelto, en términos reales, una pérdida, sin que la madera haya cambiado en nada. Usted no fracasó por haber leído mal el mercado de la madera. Fracasó porque la cinta con que midió encogió mientras su árbol crecía.',

    'Y fíjese en lo que esto le hace al cálculo a largo plazo, que es lo que está en juego. Ya no se trata de leer el mundo —la escasez real, la demanda real de madera—. Se trata de adivinar la conducta de un comité a cuarenta años. El que planta a largo plazo deja de ser alguien que apuesta sobre la realidad y pasa a ser alguien que apuesta sobre la política monetaria. Y como esa conducta es impredecible, la respuesta racional es no plantar el nogal: acortar el horizonte, buscar lo que rinda pronto, antes de que la cinta vuelva a moverse. El dinero que no se puede prever no solo dificulta los planes largos: los desalienta. Empuja a toda una sociedad a pensar en corto.',

    'Hasta aquí hemos hablado del dinero honesto como si fuera uno solo. Es hora de mirarlo de cerca, porque por primera vez en el libro vamos a encontrar una diferencia entre sus dos formas —y es justo en esta pieza, la predecibilidad, donde aparece—.',

    'Recuerde lo que vimos al presentar los regímenes: tanto el oro como Bitcoin son honestos, porque ninguno de los dos se puede crear por decreto. En la pregunta que ha guiado todo el libro —¿deja este dinero que la señal diga la verdad?— los dos están del mismo lado. Ninguno miente. Pero honestidad y predecibilidad no son lo mismo, y aquí, donde lo que importa es poder calcular el futuro, esa distinción —que hasta ahora podíamos pasar por alto— se vuelve decisiva.',

    'Vuelva a la cinta. Una cinta honesta es la que no la puede encoger nadie por decreto: su tamaño no está al capricho de ninguna autoridad. El oro es exactamente eso —y por eso es dinero honesto—. Pero hay una pregunta distinta que conviene hacerle a una cinta: además de que nadie la manipule, ¿se sabe con certeza qué tamaño tendrá mañana? Y aquí el oro flaquea un poco. No porque alguien lo manipule —nadie puede—, sino porque su cantidad futura no está escrita en ninguna parte: depende de qué vetas se descubran, de qué tan rentable sea cavar, de cuánto empuje el precio a los mineros a sacar más. El oro no miente nunca, pero sí puede sorprender. Su cinta es honesta, y aun así de tamaño no del todo conocido.',

    'Conviene ser justos con el oro, eso sí: su sorpresa es pequeña y lenta. Tan pequeña que, durante siglos, bastó para calcular. El propio Mises lo reconocía:',

    ("quote",
     '"El patrón oro cumplió satisfactoriamente las condiciones requeridas para el cálculo económico. Variaba tan escasamente la relación entre las existencias y la demanda... que los empresarios podían despreciar en sus cálculos tales mutaciones sin temor a equivocarse gravemente."',
     'Mises, <em>La acción humana</em>, El cálculo económico'),

    'El oro, entonces, no es una cinta defectuosa: es una cinta lo bastante firme como para haber sostenido el cálculo de la humanidad durante generaciones. Su ruido es leve. Pero leve no es nulo, y la pregunta de este capítulo es si se puede hacer mejor —si existe una cinta que conserve toda la honestidad del oro y, además, elimine hasta esa sorpresa pequeña—.',

    'Bitcoin cierra esa última rendija. No solo nadie puede crearlo por decreto —eso lo comparte con el oro, es la honestidad—; además, su cantidad futura está fijada y es pública hasta la última unidad: veintiún millones, en un calendario escrito que cualquiera puede leer, y que ni el precio ni la demanda ni la ambición de nadie pueden alterar. Por más que su valor se dispare y más gente se ponga a producirlo, no aparece una sola unidad de más de las previstas. Donde el oro dice "nadie me manipula, pero no sé exactamente cuánto vendré a ser", Bitcoin dice "nadie me manipula, y además sé exactamente cuánto seré, para siempre". Es una cinta no solo honesta, sino de tamaño fijo y conocido de antemano.',

    'Por eso aquí —y solo aquí, en la pieza de la predecibilidad— los dos dineros honestos por fin se separan. No en honestidad: en eso siguen empatados, los dos dicen la verdad. Se separan en la firmeza de la cinta de cara al futuro. Para casi todo lo que vimos en los capítulos anteriores, la diferencia no importaba —para que la tasa no mienta, para que las pérdidas avisen, para que los precios relativos no se distorsionen, basta con que el dinero sea honesto, y los dos lo son—. Pero para esta pieza, la de poder plantar un nogal y calcular a cuarenta años, la predecibilidad lo es todo. Es la primera de nuestras piezas en la que el oro y Bitcoin dejan de ir del brazo: la primera en que uno ofrece algo que el otro no puede dar.',

    'Aquí es donde usted, con razón, va a levantar la mano. "¿Bitcoin, predecible? Si su precio sube y baja como una montaña rusa —veinte por ciento en una semana, a veces en un día—. ¿Cómo va a ser eso una cinta de tamaño fijo?" La objeción es buena, y merece una respuesta franca, porque encierra justo la confusión que este libro existe para deshacer.',

    'Hay que separar dos cosas que la objeción mete en el mismo saco: el <em>precio</em> de Bitcoin y la <em>cantidad</em> de Bitcoin. Son cosas distintas, y solo una de las dos es la cinta. El precio —cuántos dólares cuesta un bitcoin hoy— en efecto se mueve, y mucho. La cantidad —cuántos bitcoins existen y existirán— no se mueve en absoluto: está fijada hasta la última unidad. Cuando este capítulo dice que Bitcoin es predecible, no habla del precio. Habla de la cantidad. La cinta es la cantidad, no el precio.',

    '¿Y por qué se mueve tanto el precio, entonces? Por la razón contraria a la que la objeción supone. El precio de Bitcoin oscila porque es un dinero joven, que el mundo apenas está adoptando, y cuya demanda cambia rápido mientras la humanidad decide, en tiempo real, cuánto vale. Pero fíjese de dónde viene ese vaivén: viene de la demanda —de cuánta gente lo quiere—, nunca de la oferta —de cuánto hay—. Y esa es precisamente la diferencia con el oro y con el fiat. En el oro, la cantidad misma puede sorprender; en el fiat, la cantidad cambia por decreto. En Bitcoin, jamás. Toda su volatilidad entra por la puerta de la demanda; ninguna entra por la puerta de la oferta, porque esa puerta está sellada. Es, de los tres, el único cuyo vaivén no contamina nunca la cinta.',

    'Recuerde lo que aprendió a leer hace unos capítulos. Un precio que se mueve no es, por sí mismo, una mentira —puede estar diciendo una verdad sobre cuánto desea el mundo una cosa—. El precio de Bitcoin subiendo y bajando es el mundo opinando sobre cuánto vale, en vivo: es información, no falsificación. Lo que sería falsificación —lo que rompería la cinta— es que apareciera Bitcoin de la nada para diluir el que usted tiene. Y eso no puede pasar. La montaña rusa del precio y la fijeza de la cantidad conviven sin contradicción, porque son dos planos distintos: uno es lo que el mundo paga por la cinta; el otro es el tamaño de la cinta.',

    'Hay, sí, una concesión honesta que hacer, y conviene hacerla de frente. Mientras el precio de Bitcoin siga tan movido, usar a Bitcoin como unidad de cálculo <em>hoy</em> —firmar una hipoteca a treinta años denominada en bitcoins— todavía es incómodo. Pero eso es una propiedad de su juventud como activo en adopción, no de su diseño: a medida que el mundo termine de valorarlo y su base se amplíe, el vaivén del precio tiende a calmarse. La predecibilidad de su cantidad, en cambio, es perfecta desde el primer día y para siempre. El fiat le ofrece lo contrario: un precio quieto en el corto plazo —gracias a la intervención— sobre una cantidad que se diluye sin freno en el largo. Bitcoin es ruidoso en el precio de hoy y firme en la cantidad de siempre; el fiat, plácido hoy y traicionero a cuarenta años. Para plantar su nogal, ya sabe cuál de los dos sirve.',

    'Recoja la forma de lo que vio, porque es la misma de siempre con una señal nueva. La causa sigue siendo la de todo el libro: el querer construir a futuro, plantar lo que tarda. La pieza de este capítulo ya no es una señal sobre el mundo, sino una propiedad del dinero mismo: la predecibilidad de la cinta —si su tamaño futuro es firme o incierto—. El que la lee decide cuánto se atreve a planear: con una cinta firme, planta el nogal; con una de tamaño incierto, acorta el horizonte. Y el desenlace depende, como siempre, del dinero: si la cinta no cambia, el cálculo a largo plazo es posible; si cambia sin aviso, plantar a futuro se vuelve una apuesta a ciegas, y la sociedad entera se repliega hacia lo inmediato.',

    'El dinero fiat es una cinta que cambia de tamaño cuando lo decide quien manda: con ella, calcular a futuro es adivinar. El oro es una cinta honesta —nadie la encoge por decreto—, pero de tamaño incierto: nadie sabe cuánto medirá mañana. Y Bitcoin es una cinta igual de honesta que el oro, pero de tamaño fijo para siempre.',

    'En conclusión: si una sociedad quiere medir el futuro —plantar nogales, firmar a treinta años, construir lo que tarda décadas— necesita una cinta métrica que no cambie de tamaño jamás. Bitcoin es esa cinta métrica: la única cuyo tamaño es honesto como el del oro y, además, conocido hasta la última unidad y para siempre. La única con la que usted podría calcular a cien años sin miedo a que la regla cambie bajo sus pies.',

    'Hemos hablado de poder <em>calcular</em> el futuro —de que la unidad de medida no cambie de tamaño bajo sus pies—. Pero ese cálculo mira siempre hacia adelante: hacia el nogal que aún no da fruto, hacia lo que todavía no se construye. Hay un daño hermano que no espera al futuro, porque cae sobre lo que usted ya tiene en la mano. La misma cinta que encoge y le arruina las cuentas a cuarenta años está, al mismo tiempo, encogiendo el valor de lo que usted ya guardó. No solo se vuelve difícil planear: lo que ya ganó empieza a menguar mientras duerme. Esa es la pieza que el ciudadano siente más de cerca, mes a mes, en el bolsillo —la más visible de todas—. Y es la que sigue.',
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
                 '<title>La cinta métrica — Arregla el dinero, arregla el mundo</title>',
                 out, count=1, flags=re.DOTALL)
    out = re.sub(r'<article class="page"[^>]*>.*?</article>',
                 lambda _m: article, out, count=1, flags=re.DOTALL)
    new_nav = ('<nav class="nav-foot">'
               '<a class="prev" href="precios-relativos.html">Los primeros y los últimos</a>'
               '<a class="idx" href="index.html">Índice</a>'
               '<a class="next" href="poder-adquisitivo.html">El poder adquisitivo del dinero</a></nav>')
    out = re.sub(r'<nav class="nav-foot">.*?</nav>',
                 lambda _m: new_nav, out, count=1, flags=re.DOTALL)
    out = out.replace('audio/tres-regimenes.mp3', 'audio/predictibilidad-estructural.mp3')
    out = out.replace('audio/tres-regimenes.alignment.json',
                      'audio/predictibilidad-estructural.alignment.json')
    out = out.replace('data-storage-key="tres-regimenes"',
                      'data-storage-key="predictibilidad-estructural"')

    open('predictibilidad-estructural.html', 'w', encoding='utf-8').write(out)
    n_par = sum(1 for it in CONTENT if isinstance(it, str) or (isinstance(it, tuple) and it[0] == "lead"))
    n_q = sum(1 for it in CONTENT if isinstance(it, tuple) and it[0] == "quote")
    print(f"predictibilidad-estructural.html regenerado: {n_par} párrafos, {n_q} citas")


if __name__ == "__main__":
    main()
