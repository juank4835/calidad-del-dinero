#!/usr/bin/env python3
"""Construye el cap 1 «El dinero es información»
con la estructura del libro, usando el esqueleto del cap 3.

Prosa corrida (sin subtítulos de sección) con UNA cita en bloque (Hayek).
La referencia bibliográfica va como <cite class="no-audio"> para que no la
narre el TTS (el narrador ya nombró a Hayek y la fecha justo antes)."""
import re

EYEBROW = "Bloque I · Fundamentos"
TITLE = "El dinero es información"
SUBTITLE = "Por qué una ciudad se alimenta cada mañana sin que nadie lo ordene"

# Items (sin secciones):
#   ("lead", texto)        → primer párrafo con capital
#   "texto"                → párrafo normal
#   ("quote", texto, cita) → cita en bloque; texto narrado, cita no
CONTENT = [
    ("lead", 'Mañana, cuando usted despierte, en su ciudad habrá pan fresco. Habrá leche en las tiendas, gasolina en las bombas, electricidad en los enchufes, café que viajó desde una montaña a miles de kilómetros. Nadie lo organizó. No hay una oficina central que cada noche calcule cuántas barras de pan necesitará la ciudad y le ordene a los panaderos hornearlas. Y sin embargo, casi siempre, hay justo lo suficiente —ni montañas de pan pudriéndose, ni filas de gente sin nada que comprar—.'),

    'Detengámonos en esto, porque de tan cotidiano se ha vuelto invisible, y es una de las cosas más asombrosas que hace una sociedad. Millones de personas que no se conocen, que no se hablan, que no comparten ni idioma ni país, coordinan cada día sus esfuerzos con una precisión que ninguna autoridad podría dictar. El que cultiva el trigo en un lugar, el que lo muele en otro, el que hornea, el que transporta, el que vende —ninguno conoce a los demás, ninguno sabe para quién trabaja exactamente, y aun así el pan llega—. ¿Quién les dijo a todos qué hacer?',

    'La respuesta es: nadie, y a la vez, algo. No hay una persona dándoles órdenes. Pero hay un sistema que les transmite, a cada uno, exactamente la información que necesita para decidir qué hacer —cuánto sembrar, qué producir, dónde llevarlo, a qué precio venderlo—. Ese sistema es tan silencioso y tan constante que dejamos de verlo, como dejamos de oír el motor de un avión a las dos horas de vuelo. Pero está ahí, trabajando sin descanso, coordinando a la humanidad entera. Ese sistema es el dinero —y los precios que el dinero hace posibles—.',

    'Volvamos a ese café que llegó a su taza esta mañana. Suponga que en Brasil, donde se cultiva buena parte del café del mundo, una helada arrasa las cosechas. De pronto hay mucho menos café del que había. ¿Cómo se entera usted, en su ciudad, a miles de kilómetros, de que un cultivo se congeló en otro continente? No lee la noticia. No le llega un comunicado. Y sin embargo, se entera —porque el precio del café sube—.',

    'Ese número más alto es un mensaje, aunque no lo parezca. Le está diciendo, a usted y a millones de personas a la vez: “ahora hay menos café; úselo con más cuidado”. Y cada quien responde a su manera, sin coordinarse con nadie. Usted quizás compra un poco menos, o cambia de marca. Un dueño de cafetería ajusta su carta. Un comerciante al otro lado del planeta, viendo el mismo precio, decide que ahora vale la pena enviar su café guardado. Un agricultor en Colombia o Vietnam concluye que sembrar más café se volvió rentable, y planta. Ninguno habló con los demás. Ninguno conoce la historia completa. Cada uno solo vio un número —y el número les dijo lo justo para decidir bien—.',

    'Esto es lo asombroso del precio: comprime, en una sola cifra que cualquiera entiende, una cantidad de información que ninguna persona podría reunir jamás. Para saber “cuánto café hay disponible en el mundo y cuánto lo desea la gente” haría falta conocer el clima de cada región cafetera, las decisiones de millones de consumidores, el estado de cada bodega y cada barco. Nadie tiene esa información completa —está repartida en millones de cabezas que no se conocen—. Pero el precio la resume toda, sin que nadie la reúna a propósito. Es un mensaje que se escribe solo, con los aportes de todos y la autoría de ninguno.',

    'No es una idea nueva. El economista Friedrich Hayek —que recibiría el Premio Nobel por sus trabajos sobre cómo el conocimiento se distribuye en una sociedad— la formuló hace casi un siglo, y sigue siendo la mejor descripción de lo que un precio hace:',

    ("quote",
     'Es más que una metáfora el describir el sistema de precios como una especie de maquinaria para registrar el cambio, o un sistema de telecomunicaciones que permite a los productores individuales observar solamente el movimiento de unos pocos indicadores, tal como un ingeniero puede mirar las agujas de unos pocos medidores, a fin de ajustar sus actividades.',
     'Hayek, <em>El uso del conocimiento en la sociedad</em> (1945)'),

    'Un sistema de telecomunicaciones: esa es la idea exacta. El precio le transmite a cada quien la señal que necesita para actuar, sin que nadie tenga que entender el sistema entero ni conocer la causa de lo que ocurre lejos. Cada uno mira sus pocos indicadores —como el ingeniero sus agujas— y ajusta. De la suma de todos esos pequeños ajustes, hechos a ciegas sobre el conjunto, emerge la coordinación de la sociedad entera.',

    'Y aquí está lo que convierte a esto en el corazón del libro: para que ese mensaje funcione, hace falta un idioma común en el que escribirlo. Ese idioma es el dinero. El precio del café solo puede compararse con el precio del pan, del trabajo, de la gasolina, porque todos están expresados en la misma unidad. El dinero es lo que vuelve a todos los mensajes comparables entre sí —lo que permite que la señal de un cafetal helado en Brasil llegue, traducida a un número, hasta la decisión de un agricultor en Vietnam—. Sin un idioma común, cada mensaje quedaría aislado, ilegible para los demás. El dinero es la lengua en que la humanidad entera se coordina sin hablarse.',

    'Hasta aquí podría parecer que esto es sobre café, pan y mercancías —cosas allá afuera—. Pero acérquese, porque esas mismas señales lo están guiando a usted, ahora, en las decisiones más grandes de su vida. Y usted las obedece sin haberlas oído.',

    'Piense en un joven eligiendo qué estudiar. Cree que decide libremente, y en parte lo hace. Pero a su alrededor hay señales por todas partes: ciertas carreras pagan bien y otras apenas alcanzan, ciertos oficios abundan en ofertas y otros no aparecen, cierto tipo de conocimiento parece tener futuro y otro parece condenado. Todas esas señales son, en el fondo, precios —el precio del trabajo de cada clase, que le dice a la sociedad dónde hace falta gente y dónde sobra—. El joven no lo piensa en esos términos, pero los precios están inclinando su decisión, empujándolo con suavidad hacia donde la señal dice que hay valor. Y como él, millones de jóvenes a la vez. La suma de todas esas decisiones individuales determina hacia dónde fluye el talento de una generación entera.',

    'Quizá usted eligió así. La carrera que estudió, la ciudad en la que vive, el oficio al que le entregó su veintena —es posible que fueran, en buena parte, la respuesta a una señal que nunca vio como tal—. No lo decidió del todo usted. Lo decidió, en parte, un precio. Y ya no puede devolver esos años para preguntarle al número si decía la verdad.',

    'Lo mismo ocurre con lo que una sociedad llega a construir. ¿Se investiga una cura, se desarrolla una tecnología, se levanta una industria? Nada de eso lo decide una sola persona. Lo deciden, en gran parte, las señales: dónde parece haber recursos disponibles, qué promete recompensa, qué horizonte de tiempo se ve sostenible. Los precios y la tasa de interés no garantizan que se cure el cáncer ni que se invente nada —eso depende de mil cosas más—. Pero sí inclinan la balanza: hacen que valga la pena, o que no valga la pena, dedicarle a algo los años, el dinero y las mejores mentes. A escala de una civilización entera, inclinar esa balanza es, en la práctica, moldear el futuro.',

    'Y aquí está la idea que debería quitarle el sueño. Si esas señales son verdaderas, nos guían bien: el talento fluye hacia donde de verdad se necesita, el esfuerzo se invierte donde de verdad rinde. Pero si las señales mienten, nos guían mal. Y no lo sabemos. Una generación entera puede estar estudiando lo que la señal falsa premia. Una sociedad entera puede estar levantando torres que nadie habitará y abandonando lo que de verdad la sostenía, mientras se felicita por el auge. El talento más brillante de una época puede consumirse persiguiendo espejismos rentables en lugar de curar lo que mata, alimentar lo que falta, construir lo que dura. No por maldad, ni por pereza, ni por falta de talento. Por algo más sencillo y más terrible: las señales que seguíamos no decían la verdad.',

    'No es algo que les pase a otros, en otra parte. Usted y yo vivimos sumergidos en estas señales, y todos los días tomamos decisiones grandes confiando en ellas.',

    'Un hombre pone los ahorros de veinte años en una empresa cuyo precio no para de subir. El número le jura que ahí hay valor —y compra, convencido de que llega a tiempo—. El valor no estaba; estaba el número.',

    'Una pareja joven hace sus cuentas antes de tener un hijo. Los ingresos alcanzan, el costo de la vida parece manejable, el futuro se ve sostenible. La señal les dice que sí. Deciden que sí. Y descubren, demasiado tarde, que las cuentas estaban hechas sobre cifras que mentían.',

    'El dueño de una pequeña tienda ve que su negocio prospera y que pedir prestado para crecer nunca fue tan barato. La señal le dice que es el momento de expandirse. Se endeuda, abre el segundo local —y queda atado a una deuda que se contrajo confiando en un precio que no decía la verdad—.',

    'Una familia compra la casa que durante años creyó imposible, porque de pronto el crédito alcanza. Firma treinta años de su vida sobre una señal. Un trabajador mira crecer el saldo de su cuenta y se siente, cada año, un poco más a salvo —sin saber que lo que crece es el número, no lo que el número puede comprar—.',

    'Y un hombre que trabajó toda su vida llega por fin a su jubilación con una cuenta hecha: lo ahorrado, lo que recibirá cada mes, lo que cuestan sus años por delante. Los números cierran. Puede descansar. Lo que no estaba en la cuenta era que la señal sobre la que descansa todo —cuánto valdrá su dinero mañana— era la única que nadie le aseguró que decía la verdad. Y cuando lo descubra, ya no le quedarán años para volver a empezar.',

    'Ninguno fue imprudente. Cada uno hizo exactamente lo que hace una persona sensata: mirar las señales y decidir en consecuencia. El problema no estuvo en ellos. Estuvo en que las señales que miraban no decían la verdad.',

    'Y cuando esa mentira se sostiene durante años, durante décadas, los efectos se acumulan en un lugar y estallan en otro, y casi nadie une los dos. Tomemos uno solo, el más limpio de ver: una guerra. Una guerra cuesta más de lo que ningún pueblo aceptaría pagar de su bolsillo —si hubiera que cobrar la cuenta entera, en efectivo, de frente, el mismo día, muchas guerras se apagarían por falta de fondos—. Pero cuando el dinero puede fabricarse, la cuenta no se cobra de golpe ni a la cara: se reparte, callada, en el precio de todo lo demás, durante años, sobre gente que jamás la aprobó y que nunca sabrá que la pagó. La señal que debía gritar “esto es insostenible” fue acallada. Y la guerra siguió.',

    'De los bosques que tardarán siglos en volver, del alimento cada vez más abundante y cada vez más vacío, de las burbujas que arruinan a quien llegó tarde —de todo eso hablaremos a su tiempo, despacio, hasta que sea usted quien tire del hilo.',

    'Porque en cada una de esas historias, si uno sigue el hilo lo suficiente, reaparece el mismo instante: una señal que dijo lo que no era. No siempre la falsificó alguien. A veces hay un culpable con nombre; a veces no hay más que un mecanismo que nadie gobierna del todo —y esa es la versión más inquietante, porque entonces no basta con cambiar al que manda—. Pero todavía no. Primero hay que entender bien cómo funciona la señal cuando dice la verdad, para reconocer después, sin que quepa duda, cómo se ve cuando miente. Avanzamos confiados, creyendo que vemos, hacia donde un mensaje falso nos llamó. Este libro trata de cómo se corrompe ese mensaje, quién gana cuando se corrompe, y qué haría falta para volver a confiar en lo que vemos.',

    'Si todo esto es cierto —si el dinero es el sistema que transporta la información con que una sociedad entera decide qué hacer—, entonces se sigue una conclusión que cambia por completo cómo debemos juzgar el dinero. Solemos preguntarnos si una moneda es fuerte o débil, si los precios suben poco o mucho, si la economía crece. Pero esas son preguntas sobre los síntomas. La pregunta de fondo, la que de verdad importa, es otra: ¿qué tan verdadera es la información que este dinero transmite? ¿Sus señales dicen la verdad sobre el mundo, o mienten?',

    'Ese es el criterio de este libro, y es distinto de todos los demás. No vamos a evaluar los sistemas monetarios por su estabilidad, ni por su eficiencia, ni por cuánto crece la economía bajo cada uno —esos son los criterios de siempre, y miran el termómetro en vez de mirar la fiebre—. Vamos a evaluarlos por una sola cosa: la calidad de la información que producen. Un buen dinero es el que transmite señales verdaderas, el que le permite a la sociedad ver con claridad y coordinarse bien. Un mal dinero es el que falsifica esas señales, el que hace que millones de personas decidan sobre la base de mensajes falsos sin saberlo. Todo lo demás —la inflación, las crisis, los auges que terminan en ruina— se sigue de ahí.',

    'Con ese criterio en la mano, el resto del camino queda trazado. Si lo que importa es la calidad de la información, entonces la pregunta práctica es cuáles formas de organizar el dinero la protegen y cuáles la corrompen. Existen, a grandes rasgos, tres maneras de hacerlo, y las examinaremos una por una —desde la que mantiene las señales más limpias hasta la que las falsifica a voluntad—. Pero antes de juzgar ningún sistema, hay que entender bien las piezas con las que todos trabajan: qué es la paciencia de una sociedad, qué ocurre cuando alguien ahorra, y cómo nace de ahí la más importante de todas las señales, la que le pone precio al tiempo. A eso dedicaremos los siguientes capítulos. Cuando volvamos a los sistemas monetarios, ya tendremos con qué juzgarlos.',
]

# CSS de la cita (igual al del resto del libro)
EXTRA_CSS = """
/* ===== Citas en bloque — alineadas a la izquierda, sobrias (filete fino) ===== */
.prose .pull-quote {
  margin: 2.4rem 0; padding: 0.3rem 0 0.3rem 1.5rem;
  border-left: 2px solid var(--rule);
}
.prose .pull-quote p {
  font-size: 1.06rem; font-style: italic; line-height: 1.7; color: var(--ink); margin: 0 0 0.7rem;
}
.prose .pull-quote cite {
  display: block; font-style: italic; font-size: 0.88rem; line-height: 1.5; color: var(--ink-soft);
}
"""

# ---- Construir el HTML del article ----
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

# ---- Esqueleto del cap 3 ----
sk = open('tres-regimenes.html', encoding='utf-8').read()
out = sk
out = re.sub(r'<title>.*?</title>',
             '<title>El dinero es información — Arregla el dinero, arregla el mundo</title>',
             out, count=1, flags=re.DOTALL)
out = re.sub(r'<article class="page"[^>]*>.*?</article>', lambda _m: article, out, count=1, flags=re.DOTALL)
# nav-foot: prev = índice; next = criterio de evaluación
new_nav = ('<nav class="nav-foot">'
           '<a class="prev" href="index.html">Índice</a>'
           '<a class="idx" href="index.html">Índice</a>'
           '<a class="next" href="criterio-de-evaluacion.html">El criterio de evaluación</a></nav>')
out = re.sub(r'<nav class="nav-foot">.*?</nav>', lambda _m: new_nav, out, count=1, flags=re.DOTALL)
out = out.replace('</style>', EXTRA_CSS + '</style>', 1)
out = out.replace('audio/tres-regimenes.mp3', 'audio/dinero-como-informacion.mp3')
out = out.replace('audio/tres-regimenes.alignment.json', 'audio/dinero-como-informacion.alignment.json')
out = out.replace('data-storage-key="tres-regimenes"', 'data-storage-key="dinero-como-informacion"')

open('dinero-como-informacion.html', 'w', encoding='utf-8').write(out)
n_par = sum(1 for it in CONTENT if isinstance(it, str) or it[0] == "lead")
n_q = sum(1 for it in CONTENT if isinstance(it, tuple) and it[0] == "quote")
print("dinero-como-informacion.html creado")
print(f"párrafos narrados: {n_par} | citas: {n_q}")
