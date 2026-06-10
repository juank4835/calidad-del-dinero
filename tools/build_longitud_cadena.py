#!/usr/bin/env python3
"""Construye el cap 8 «La longitud de la cadena» (Bloque III, segunda pieza).

Reescritura completa. Cap nuevo titulado «La longitud de la cadena»
(humano) — el título técnico «La asignación intertemporal» queda como
revelable al hover en el índice, igual que los caps 1–6 humanos.

El slug del archivo NO cambia: sigue siendo asignacion-intertemporal.html
para preservar URLs y nav-foots; cambia el título visible y el audio.

Estructura:
- Header: eyebrow «Segunda pieza · gravedad crítica» + h1 «La
  longitud de la cadena» + subtítulo «Cómo una señal reordena lo que
  una sociedad construye».
- Prosa corrida sin secciones.
- 3 citas en bloque, todas de Hayek, Precios y producción.
- Todas las atribuciones <cite class="no-audio"> — el párrafo previo
  nombra a Hayek en cada caso.
"""
import re

EYEBROW = "Segunda pieza · gravedad crítica"
TITLE = "La longitud de la cadena"
SUBTITLE = "Cómo una señal reordena lo que una sociedad construye"

CONTENT = [
    ("lead",
     'Esta mañana, alguien se comió un pan. Un acto trivial, instantáneo. Pero detrás de ese pan hay una cadena de trabajo que empezó hace meses, y que casi nadie ve. Alguien horneó la masa —pero antes, alguien molió el trigo; y antes, alguien lo cosechó; y antes, lo sembró; y para sembrarlo, alguien aró un campo con un tractor; y ese tractor salió de una fábrica, que a su vez necesitó acero, que alguien fundió a partir de un hierro que alguien extrajo de una mina. El pan de esta mañana descansa sobre una columna de esfuerzo que se hunde meses, años, en el pasado.'),

    'Esa columna tiene un nombre en este libro: la estructura de producción. Toda cosa que usted consume es la punta visible de una cadena de etapas que ocurrieron antes, cada una más lejana del consumo final. El pan está en la punta; el trigo, una etapa más atrás; el tractor, varias más; la mina de hierro, en el fondo. Hayek, que estudió esto como nadie, la describía como una sucesión de estadios que van desde los medios más originales —la tierra, el trabajo en bruto— hasta el bien terminado que llega a sus manos.',

    'Y aquí está la pregunta que define este capítulo: ¿qué tan larga puede ser esa cadena? Porque alargarla —añadir etapas, usar métodos más indirectos— no es un capricho. Es lo que nos hace más productivos. Hayek lo dijo con claridad:',

    ("quote",
     '"Mediante la prolongación del proceso productivo podemos obtener una cantidad mayor de bienes de consumo a partir de una cantidad dada de medios originales de producción... siempre que estemos dispuestos a esperar lo suficiente para la llegada del producto."',
     'Hayek, <em>Precios y producción</em>'),

    'Lea con cuidado las últimas palabras, porque son la bisagra de todo: <em>siempre que estemos dispuestos a esperar</em>. Un pescador que pesca con las manos come hoy, pero poco. Si dedicara una semana a tejer una red —sin pescar, pasando hambre esa semana—, después pescaría diez veces más. La red es una etapa productiva añadida: un método más largo, más indirecto, que rinde mucho más. Pero exige una cosa que no todos pueden pagar: esperar. Pasar hambre la semana que teje. Solo quien tiene reservas —quien ahorró— puede permitirse alargar el proceso.',

    'Multiplique ese pescador por una sociedad entera. Una economía que ahorra —que es paciente, que libera recursos en vez de consumirlos todos hoy— puede permitirse cadenas largas: puede tejer redes, construir fábricas, tender ferrocarriles, financiar la investigación que tarda una década en dar fruto. Una economía que no ahorra —impaciente, que consume todo ya— solo alcanza para las cadenas cortas, para pescar con las manos. La longitud de lo que una sociedad puede construir está atada a su paciencia.',

    '¿Y quién dirige ese tráfico? ¿Quién le dice a los empresarios "adelante con la cadena larga" o "limítese a lo inmediato"? Ya lo conocemos del capítulo anterior: la tasa de interés. Una tasa baja —mucho ahorro, mucha paciencia— hace rentables los procesos largos, las etapas lejanas, lo que tarda. Una tasa alta —poco ahorro— los vuelve inviables y empuja los recursos hacia lo cercano al consumo. La tasa no solo informa cuánta paciencia hay: <em>reorganiza físicamente</em> la economía según esa paciencia. Es el director de orquesta que decide cuántas etapas suenan.',

    'Volvamos al pescador, porque en él se ve toda la cadena de un vistazo. Las manos y la red ya las conoce: comer poco hoy, o esperar una semana de hambre y sacar diez veces más. Pero la escalera sigue. Construir un barco lo obliga a esperar mucho más —meses sin pescar, viviendo de reservas—, pero después saca cien veces más. Y montar un astillero que produzca barcos para toda la aldea tarda años, pero multiplica la pesca de todos. Manos, red, barco, astillero: es una escalera, y cada peldaño hacia atrás está más lejos del pescado que se come hoy, tarda más en dar fruto —y rinde mucho más—.',

    'Esa es la clave, y el pescador la muestra de un vistazo: lo que está "lejos del consumo" no rinde más por estar lejos, sino porque es <em>preparación que multiplica todo lo que viene después</em>. El astillero no se come. Pero hace posible una abundancia de pescado que pescar con las manos jamás alcanzaría. Por eso una sociedad rica no es la que tiene más gente pescando con las manos: es la que pudo permitirse construir astilleros —dedicar recursos a etapas lejanas que, en su momento, no daban nada de comer—.',

    'Pero subir cada peldaño cuesta lo mismo: esperar. Y no todos pueden pagar esa espera. Solo quien tiene reservas —quien ahorró— puede dejar de pescar una semana para tejer la red, o un año para montar el astillero. Y fíjese en qué es, exactamente, ese ahorro: no es un cofre de monedas. Es el pescado que el pescador <em>no se comió</em> mientras tejía. Privarse del pescado de hoy para poder construir —eso es ahorrar, en el sentido real que ya vimos: no guardar dinero, sino dejar recursos sin consumir para que sostengan lo que se está construyendo—. El pescado no comido es lo que alimenta al pescador la semana que no pesca. Sin ese pescado guardado, no hay red; sin reservas, no hay astillero. Aquí es donde la cadena se conecta con todo lo anterior: <em>cuánta espera puede pagar una sociedad es cuánto ahorro real tiene</em>, y eso es exactamente lo que la tasa de interés comunica. Una tasa baja anuncia "hay reservas de sobra, la aldea puede permitirse el astillero". Una tasa alta avisa "apenas hay para hoy, quédese pescando con las manos".',

    'Y cuando la tasa baja, ocurre algo preciso y físico en toda la economía: los recursos —el trabajo, los materiales que pueden usarse en cualquier etapa— empiezan a desplazarse desde las etapas cercanas al consumo hacia las lejanas. Menos manos pescando, más manos construyendo astilleros. Hayek describió ese desplazamiento con cuidado:',

    ("quote",
     '"Una proporción mayor de aquellos bienes de producción que pueden ser utilizados en diferentes estadios productivos —los bienes no específicos— será atraída hacia los estadios anteriores, donde, debido al cambio en la tasa del ahorro, se podrán obtener precios relativamente mayores."',
     'Hayek, <em>Precios y producción</em>'),

    'Traducido a la aldea: cuando hay más ahorro, conviene dedicar gente y materiales a construir astilleros y barcos —las etapas lejanas— en vez de a pescar con las manos. No porque alguien lo ordene, sino porque la tasa baja vuelve rentables esos proyectos largos que antes no lo eran. La señal reorganiza, sola, hacia dónde fluye el esfuerzo de la sociedad. Esto es lo que los economistas llaman <em>asignación intertemporal</em>: la distribución de los recursos a lo largo del tiempo —cuánto se dedica a producir para hoy y cuánto a preparar el mañana—. Y la dirige la tasa, peldaño por peldaño.',

    'Fíjese en lo que tenemos cuando todo es honesto: la gente ahorra porque de verdad quiere esperar (la causa); ese ahorro libera recursos reales (la primera consecuencia); la tasa baja y lo anuncia (la señal); los empresarios la leen y desplazan recursos hacia las etapas largas (la lectura); y la economía se reorganiza para construir más astilleros (la segunda consecuencia: la cadena que cambia de longitud). Todo encaja, porque la espera que la tasa anuncia es espera de verdad: hay reservas para sostener a quienes tejen redes y montan astilleros mientras no pescan. La cadena se alarga sobre suelo firme.',

    'Ahora repitamos la historia, pero con un cambio: la tasa baja sin que nadie haya ahorrado. El banco central inyecta crédito nuevo —dinero creado de la nada, como vimos— y la tasa cae. La aldea no se volvió más paciente; nadie dejó de comer pescado; no hay un solo pescado de más guardado. Pero la señal dice que sí. Dice "hay reservas de sobra, adelante con el astillero".',

    'Y aquí está lo grave, lo que hace de esta la falsificación más profunda de todas: los pescadores leen la señal y hacen <em>exactamente lo que deberían hacer si fuera verdad</em>. Dejan las manos, dejan de pescar, se ponen a construir el astillero. La aldea entera reorienta su esfuerzo hacia las etapas largas —igual que antes—, convencida de que hay pescado guardado para alimentarlos mientras construyen. La estructura se alarga. Por un tiempo, parece progreso: hay un astillero levantándose, todos ocupados, optimismo —eso que, a escala de países, llamamos auge—. Y el auge no es la salud: es el síntoma.',

    'Pero no hay pescado guardado. Esa es la única diferencia con la historia anterior —y lo cambia todo—. Cuando llega el momento de comer, las reservas que debían sostener a los constructores no existen, porque nadie subconsumió para crearlas. La estructura alargada artificialmente choca contra una realidad que el dinero no pudo falsificar —es el día en que el mensaje y el mundo, por fin, se encuentran—: no hay con qué alimentar a los que dejaron de pescar. Y entonces el astillero a medio construir tiene que abandonarse —no porque fuera mala idea, sino porque nunca hubo recursos reales para terminarlo—. Hayek lo demostró con rigor: una prolongación de la cadena que no descansa en ahorro verdadero no puede sostenerse.',

    ("quote",
     '"Una prolongación del proceso productivo causada por ahorro forzoso... no puede ser permanente sino que necesariamente ha de venir seguida por un acortamiento del proceso productivo... tendrá lugar inevitablemente una contracción del proceso productivo artificialmente extendido."',
     'Hayek, <em>Precios y producción</em>'),

    '"Ahorro forzoso" es el nombre técnico de lo que pasó: a la aldea se la forzó a comportarse como si hubiera ahorrado, sin haberlo hecho. Y la contracción que sigue —el acortamiento de la cadena, el regreso forzado a pescar con las manos— es lo que vivimos como crisis. No es un castigo que cae del cielo: es la estructura productiva volviendo, a las malas, al tamaño que el ahorro real siempre pudo sostener. El astillero abandonado, las redes a medio tejer, la gente que vuelve a pescar con las manos con menos de lo que tenía antes de empezar: eso es la mala inversión hecha ruinas físicas.',

    'Y hay un daño que no se recupera. Mientras se construía el astillero imposible, se dejaron de tejer las redes que sí se podían sostener. Los recursos que se hundieron en la etapa demasiado larga —el trabajo, los materiales específicos que solo servían para ese astillero— no se pueden recuperar cuando la cadena se acorta. Hayek lo señaló: los bienes hechos para las etapas lejanas, cuando la estructura se contrae, <em>pierden su valor o se vuelven inútiles</em>. La aldea no solo vuelve a donde estaba: vuelve más pobre, porque gastó esfuerzo real en algo que nunca pudo ser.',

    'Esta es la diferencia con el capítulo anterior, y vale la pena verla con claridad. Allá vimos <em>que</em> la tasa falsa engaña. Aquí vemos <em>qué</em> destruye exactamente: la forma física de la economía —cuántas etapas, cuán largas, cuánto de lo construido sobrevive y cuánto queda en ruinas—. La falsificación de la tasa no es un error de un número en una pantalla. Es un astillero a medio levantar, pudriéndose en la playa, que se construyó con el pescado que la aldea necesitaba para comer. Y aunque hablemos de pescadores, esto tiene nombres que usted reconoce: cada gran crisis financiera de las últimas décadas es, en el fondo, un astillero abandonado a escala de millones —lo veremos, con nombre y fecha, más adelante—.',

    'Conviene recoger lo que esta historia nos enseñó, porque tiene una forma que vale la pena reconocer. Todo empezó con una disposición: cuánta gente está dispuesta a esperar. Esa disposición, cuando es real, libera recursos —el pescado no comido—. La tasa de interés recoge ese hecho y lo anuncia. Los empresarios la leen y reorganizan la economía hacia las etapas largas. Y si la señal decía la verdad, la cadena se alarga sobre suelo firme; si mentía, se alarga sobre el vacío y termina derrumbándose. Una causa, una consecuencia física, una señal que las comunica, una reacción que reorganiza el mundo, y un desenlace que depende de si la señal era honesta. Esa forma —guárdela— va a reaparecer en cada uno de los capítulos que siguen, con otras señales y otros daños, pero con la misma estructura por debajo. Aprender a verla es aprender a leer el libro entero.',

    'Queda, sin embargo, una pregunta que esta historia deja abierta. La aldea construyó el astillero imposible y la cadena se derrumbó —pero eso lo sabemos nosotros, que miramos desde afuera—. ¿Cómo se da cuenta <em>la aldea</em> de que se equivocó? ¿Qué le avisa a una sociedad que construyó de más, que alargó la cadena sobre un ahorro que no existía? Porque mientras se levantaba el astillero, todo parecía ir bien. El error ya estaba cometido mucho antes de que nadie lo notara. Cómo se descubre ese error —qué señal lo delata, y por qué a veces esa señal también puede silenciarse— es una historia con vida propia. Es la del próximo capítulo.',
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
                 '<title>La longitud de la cadena — Arregla el dinero, arregla el mundo</title>',
                 out, count=1, flags=re.DOTALL)
    out = re.sub(r'<article class="page"[^>]*>.*?</article>',
                 lambda _m: article, out, count=1, flags=re.DOTALL)
    new_nav = ('<nav class="nav-foot">'
               '<a class="prev" href="tasa-de-interes.html">La tasa de interés</a>'
               '<a class="idx" href="index.html">Índice</a>'
               '<a class="next" href="deteccion-mala-inversion.html">La detección de la mala inversión</a></nav>')
    out = re.sub(r'<nav class="nav-foot">.*?</nav>',
                 lambda _m: new_nav, out, count=1, flags=re.DOTALL)
    out = out.replace('audio/tres-regimenes.mp3', 'audio/asignacion-intertemporal.mp3')
    out = out.replace('audio/tres-regimenes.alignment.json',
                      'audio/asignacion-intertemporal.alignment.json')
    out = out.replace('data-storage-key="tres-regimenes"',
                      'data-storage-key="asignacion-intertemporal"')

    open('asignacion-intertemporal.html', 'w', encoding='utf-8').write(out)
    n_par = sum(1 for it in CONTENT if isinstance(it, str) or (isinstance(it, tuple) and it[0] == "lead"))
    n_q = sum(1 for it in CONTENT if isinstance(it, tuple) and it[0] == "quote")
    print(f"asignacion-intertemporal.html regenerado: {n_par} párrafos, {n_q} citas")


if __name__ == "__main__":
    main()
