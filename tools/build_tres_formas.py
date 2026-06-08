#!/usr/bin/env python3
"""Construye «Las tres formas de organizar el dinero» — VERSIÓN CORREGIDA
del cap 3 del Bloque I. NO reemplaza al cap 3 original (tres-regimenes.html):
es una versión alternativa que coexiste con la original, enlazada desde el
índice con un estado «Corrección» en rojo."""
import re

EYEBROW = "Bloque I · Fundamentos · corrección"
TITLE = "Las tres formas de organizar el dinero"
SUBTITLE = "Tres maneras, dos resultados"

# Tipos de item dentro de cada sección:
#   ("lead", texto)             → primer párrafo con capital
#   "texto"                     → párrafo normal
#   ("lema", texto)             → máxima destacada (blockquote.lema)
#   ("quote", texto, atribución) → cita de autor (blockquote.pull-quote + cite)
CONTENT = [
    (None, [
        ("lead", 'Saque un billete del bolsillo y véalo de frente. O mire el saldo de su cuenta bancaria en su teléfono, da igual. Esa cifra le promete algo: que con ella podrá comprar mañana más o menos lo mismo que hoy, que no se va a evaporar entre sus manos. Usted confía en esa promesa todos los días sin pensarlo —tiene que confiar, no le queda otra—. La pregunta de este capítulo es si esa promesa es verdadera. Porque hay dinero que no puede mentirle, y hay dinero que miente. Y desde donde usted está, con el billete en la mano, no hay forma de notar la diferencia. Pero la hay, y lo cambia todo.'),
    ]),
    ("¿Qué significa que el dinero mienta?", [
        '¿Cómo puede mentir una cifra? Pensémoslo con un caso extremo, que es como mejor se ve. Imagine que esta noche, mientras todos duermen, la cantidad de dinero del país se duplica: cada billete, cada cuenta, ahora marca el doble. ¿Amaneció el país dos veces más rico? No hay un solo pan más, ni un par de zapatos más, ni una casa más que ayer. Lo único que cambió fue el número. Y como ahora hay el doble de dinero persiguiendo las mismas cosas de siempre, los precios no tardan en acomodarse: todo termina costando el doble, y usted volvió al punto de partida —o peor, porque ese dinero nuevo no le llegó a usted primero—. Ahí está la mentira, a plena luz: el dinero anunció que había el doble de riqueza, y era falso. No la dijo con palabras; la dijo con cantidad. Un dinero dice la verdad cuando la cantidad que hay corresponde a cosas que de verdad se produjeron; miente cuando aparecen cifras nuevas que no corresponden a nada. Y lo que usted acaba de ver —los precios que suben— es apenas la cara visible de esa mentira: por debajo desordena cosas mucho más hondas, de las que se ocupará buena parte de este libro.',

        'Eso que el dinero falso traiciona tiene la forma de un acuerdo tan elemental que casi nunca se dice en voz alta:',

        ("lema", 'El dinero no se crea de la nada: se produce.'),

        'Dicho de otro modo: el dinero solo debería entrar por una puerta, la de la producción —arrancar el oro a la tierra, minar un bitcoin, fabricar algo que alguien quiera—. Por esa puerta, para llevarse una unidad de dinero hay que dejar, a cambio, algo real. El dinero honesto tiene solo esa entrada. El dinero deshonesto tiene una segunda puerta, una que no da a ningún taller ni a ninguna mina —y no importa quién la abra: puede ser el sello de un gobierno o la firma de un banco privado—. Por ella entran unidades nuevas sin que nadie haya producido nada, y quien las emite se lleva un valor que no creó, restándoselo, sin que se note, a todos los que sí lo crearon.',

        'A lo largo de la historia, la humanidad ha organizado su dinero de tres maneras —lo que los economistas llaman <em>regímenes monetarios</em>—, y se distinguen por cómo tratan ese acuerdo. Una lo respeta por completo: nadie puede crear dinero de la nada. Otra lo rompe a medias, casi sin proponérselo. Y la tercera lo rompe del todo. Tres maneras distintas; pero, para lo único que aquí importa —si el dinero dice la verdad—, solo dan dos resultados: o se respeta el acuerdo, o se rompe. Empezaremos por los dos extremos, donde todo se ve más nítido, y dejaremos para el final el caso del medio, que es donde se esconde la lección más fina de todas.',
    ]),
    ("El dinero duro · el que respeta el acuerdo", [
        'Empecemos por el dinero que respeta el acuerdo sin reservas. A lo largo de casi toda la historia, ese dinero fue el oro. No porque tuviera algo mágico, sino por una propiedad simple y decisiva: nadie puede fabricarlo de la nada. Para tener más oro hay que encontrarlo, extraerlo de la roca, refinarlo —no se decreta, se produce—. Nadie puede despertar una mañana y, con una orden, duplicar el oro del mundo. Y eso es justamente lo que lo vuelve <em>honesto</em>: como cada gramo nuevo tuvo que arrancarse a la tierra, la cantidad de oro que circula no miente: corresponde a algo que de verdad se produjo. Nadie puede inflarla con un papel firmado. La señal no se puede falsificar, porque el oro no se puede falsificar.',

        'Pero el oro tiene una grieta —y conviene ver con precisión cuál es, porque no es la que parece—. El oro no miente: cada gramo que aparece vino de extraerlo. En eso es plenamente honesto. Su grieta es otra: <em>nadie sabe cuánto vendrá</em>. Se puede descubrir una veta nueva, puede mejorar la tecnología de extracción y —esto es lo decisivo— si el precio del oro sube lo suficiente, de pronto resulta rentable cavar donde antes no lo era, y la oferta se acelera. La historia lo conoce: la avalancha de oro que España trajo de América diluyó el valor del que ya existía y encareció todo a su paso. Fíjese en lo sutil: ese oro nuevo no era una mentira —se había extraído de verdad—, pero sí fue una sorpresa. Y esa es la grieta: no que el oro engañe, sino que su cantidad futura es incierta. El oro es <em>honesto</em>, pero no del todo <em>predecible</em>.',

        'Y aquí aparece, por primera vez en esta historia, algo nuevo. Bitcoin es honesto igual que el oro —tampoco se crea por decreto; cada unidad nueva hay que minarla—. Pero cierra la grieta que el oro deja abierta: la de la predecibilidad. Su cantidad total está fijada de antemano —nunca habrá más de veintiún millones de unidades, y el ritmo al que se producen está escrito en el sistema, a la vista de todos, hasta la última que se emitirá dentro de más de un siglo—. Y a diferencia del oro, su oferta no cede ante el precio: por más que su valor se dispare y más gente se ponga a minar, no aparece ni una unidad de más; lo único que cambia es cuántos compiten por la misma cantidad ya pautada. No hay veta nueva que descubrir, no hay incentivo que acelere su producción, no hay continente por saquear. Donde la cantidad futura del oro es incierta, la de Bitcoin es certeza absoluta: cualquiera puede saber hoy cuánto existirá en cualquier momento del porvenir. Bitcoin es <em>honesto y predecible</em> —las dos virtudes a la vez—.',

        'No confunda esto con una comparación de conveniencia. El oro y Bitcoin difieren en muchas cosas prácticas —en cómo se guardan, se mueven, se dividen—, y esas diferencias importan para la vida diaria. Pero esa es otra discusión, y todavía no la nuestra; volveremos a una de ellas más adelante, cuando descubramos que no era tan práctica como parecía, sino una cuestión de honestidad. Para nuestra única pregunta —¿deja este dinero que la señal diga la verdad?— oro y Bitcoin están del mismo lado, el lado honesto: ninguno de los dos miente, ninguno se crea por decreto. Su diferencia no está en la honestidad, sino en la predecibilidad: el oro dice la verdad pero su cantidad futura puede sorprender; Bitcoin dice la verdad y además su cantidad no sorprende jamás. Una señal honesta con un poco de ruido, frente a una señal honesta y nítida. Pero esa diferencia entre ellos es pequeña al lado de lo que ambos comparten, y que los separa de todo lo que viene después: en ninguno de los dos puede nadie crear unidades de la nada para falsificar lo que el dinero dice. Esa —la línea entre un dinero que no se puede falsificar y uno que sí— es la que de verdad parte la historia en dos.',
    ]),
    ("La banca central · el que rompe el acuerdo", [
        'Saltemos ahora al otro extremo, al dinero que rompe el acuerdo por completo —y que, casi con seguridad, es el que usted lleva hoy en el bolsillo—. Es el dinero <em>fiat</em>: billetes y saldos que no son títulos sobre nada real —no representan oro, ni plata, ni ningún activo que alguien tuvo que producir—. Su valor no viene de algo que respaldan, sino de un decreto —“esto es dinero porque el Estado lo dice”— y de la costumbre de todos de aceptarlo. La palabra latina <em>fiat</em> significa, precisamente, “hágase”. Dinero que existe porque alguien ordenó que existiera.',

        'Pero conviene ver de dónde sale, exactamente, porque la respuesta es más extraña de lo que parece. Cuando usted dice “mi banco”, piensa en el de la esquina, el de su tarjeta y su aplicación —su banco comercial—. Pero por encima de él existe otra entidad de la que usted nunca ha sido cliente y que sin embargo manda sobre todo el dinero del país: el banco central. La relación entre los dos es una pirámide. En la base, el banco central pone los cimientos: el dinero primario, el que solo él puede crear. Encima, apoyándose en esa base, los bancos comerciales levantan pisos —prestan, y al prestar crean dinero nuevo que no estaba—. Los dos fabrican, no solo el de abajo. Y aquí está lo inquietante: cuántos pisos se levanten sobre cada cimiento no lo controla bien nadie, ni siquiera el banco central de la base.',

        'Y ese dinero nuevo —el de cualquiera de los dos niveles— no viene de que alguien lo haya ganado, ni producido, ni extraído de la tierra. Viene de que alguien decidió crearlo: antes con una imprenta, hoy con un registro electrónico. Es exactamente la segunda puerta de la que hablábamos —la que no da a ningún taller ni a ninguna mina—, abierta de par en par y vuelta funcionamiento normal. Lo que en el oro sería una rareza, aquí es el diseño.',

        'Recuerde lo que esto significa, porque ya lo vimos. Si el dinero es el sistema que transmite la información con que todos decidimos, entonces crear dinero de la nada no es “estimular la economía” ni “inyectar liquidez” —esos son los nombres amables—. Es introducir información falsa en el sistema que todos leen. Es anunciarle a la sociedad que hay más de lo que en verdad hay, sin que nada nuevo se haya producido para respaldarlo. Cada unidad nueva es un mensaje que miente, y como todos leen los precios para decidir, la mentira se reparte por la economía entera sin que nadie la haya autorizado. Llamarlo por su nombre no es exagerar: es <em>falsificación de la señal</em>, hecha por quien tiene el monopolio de hacerla.',

        'Y conviene ver desde ya qué tiene de particular que sea el Estado quien hace esto. No es un detalle. Que el dinero falso lo emita una entidad con el poder de la fuerza cambia todo lo que sigue: significa que puede prohibir que cualquier otro compita con ella, y puede obligarlo a usted a aceptar su dinero aunque mienta. Un falsificador cualquiera tiene que esconderse; este falsificador hace ley. Guardaremos ese hilo —la fuerza— porque es el que, al final, separa al banco central de todo lo demás. Pero antes hay que ver algo que sorprende: que la falsificación, el primero de los dos pecados, no es exclusiva del Estado. También un sistema enteramente privado puede cometerla. Y eso nos lleva al tercer caso, el más instructivo de los tres.',
    ]),
    ("La banca libre · el que rompe el acuerdo a medias", [
        'Llegamos al tercer caso, el del medio, y es el más instructivo de los tres —porque revela algo que casi nadie espera—. Imagine un sistema sin banco central, sin Estado emitiendo dinero: bancos privados, libres, compitiendo, cada uno trabajando con dinero sólido, con oro de verdad en sus bóvedas y recibos que lo representan. Suena a la antítesis del banco central, al dinero limpio por excelencia. Y sin embargo, puede falsificar la misma señal —con el mismo mecanismo que el banco central usará después—. Aquí está la sorpresa: el primero de los dos pecados, falsificar, no necesita al Estado. Un privado también puede.',

        'Pero antes de ver el truco, hay que ver el mundo donde ocurre —porque es un mundo que usted nunca habitó, y sin imaginarlo nada de lo que sigue tiene sentido—. Empecemos por algo que sí conoce. Hoy usted casi no toca su dinero: lo deja en el banco y en su lugar usa un saldo, un número en una pantalla que circula por usted cuando paga. Ese número no es el dinero; es la promesa del banco de que el dinero está ahí, guardado, disponible cuando lo pida. Pues bien: eso no lo inventó la era digital. Nació hace siglos, con el oro. Cargar metal era incómodo y peligroso, así que la gente lo dejaba en un banco y recibía a cambio un papel —un <em>recibo</em>— que decía “su oro está aquí, tantos gramos, devolvibles cuando los pida”. Y como ese papel era más cómodo de llevar que el metal, la gente empezó a pagarse con el papel en vez de ir por el oro. El recibo empezó a circular <em>como si fuera</em> el dinero. Ese recibo de oro es, literalmente, el abuelo de su saldo bancario de hoy.',

        'Con una diferencia que importa, y que distingue este mundo del suyo. Hoy hay un solo dinero: el peso, el billete del Estado, igual para todos. En este sistema no había un emisor único. Cada banco emitía su propio papel. Suponga que Hernando guarda su oro en el Banco del Puente y Luisa en el Banco de la Plaza: cada uno carga billetes con el nombre de <em>su</em> banco, papeles distintos circulando a la vez. El día que Hernando le paga a Luisa con billetes del Banco del Puente, ella tiene en la mano un recibo de un banco que no es el suyo —y antes de guardarlo hace, sin pensarlo, la pregunta que sostenía todo el sistema: <em>¿confío en que el Banco del Puente tiene de verdad el oro que este papel promete?</em>—. Y fíjese en algo: no eran monedas caprichosas, cada una con su valor inventado. Los dos billetes prometían lo mismo, oro; lo único que cambiaba era quién lo prometía, y por tanto cuánta confianza merecía. Si Luisa confiaba en el Banco del Puente, aceptaba su papel como dinero y seguía circulando. Si no, lo rechazaba, o iba de inmediato a cambiarlo por el metal. Esa pregunta —la confianza en que detrás del papel está el oro— es el resorte que vamos a ver saltar.',

        'Ese mecanismo tiene nombre, y conviene aprenderlo porque es el corazón de todo lo que sigue: la <em>reserva fraccionaria</em>. Funciona así. Usted deposita su oro en un banco, y el banco le entrega un recibo —un papel que promete devolverle ese oro cuando lo pida—. Hasta ahí, todo honesto: el recibo representa oro que existe, oro real en la bóveda. Pero el banquero nota algo tentador: casi nadie reclama su oro al mismo tiempo. Así que emite <em>más</em> recibos de los que tiene oro en la bóveda —recibos por oro que no existe— y los presta para ganar interés. Y aquí es donde reaparece, intacta, la lógica del fiat: esos recibos falsos son pasivos del banco —promesas que dice tener respaldo y no lo tienen— pero circulan como si fueran lo mismo que los recibos genuinos, es decir, como si fueran títulos sobre un activo real que está. La señal vuelve a mentir porque el dinero deshonesto reaparece bajo otra forma —no billetes del banco central, sino recibos de un banco privado—, pero el truco es el mismo: hacer pasar una promesa por algo que existe.',

        'Aquí conviene una precisión, porque es donde muchos se confunden. El banco no le está <em>pidiendo prestado</em> su oro —eso sería honesto y distinto—. Si usted le presta su oro al banco por un año, sabe que no lo tiene disponible; nadie miente. El fraude es otra cosa: el banco emite recibos que prometen devolver el oro <em>a la vista, en cualquier momento</em>, mientras sabe que no puede cumplirlos todos. El recibo no dice “le debo”; dice “su oro está aquí”. Y no está. Rothbard no suaviza lo que esto es:',

        ("quote",
         '“Si bien ‘fraude’ es una expresión dura, es adecuada para describir esta práctica, aun cuando la legislación no la reconozca como tal.”',
         'Rothbard, <em>El hombre, la economía y el Estado</em>, cap. 11'),

        'Y lo ilustra con una imagen que no deja escapatoria: si alguien le vende una caja etiquetada “copos de avena” y al abrirla contiene paja, eso no es un mal negocio —es un robo—. Emitir recibos por un oro que no existe, idénticos a los genuinos, es exactamente lo mismo: vender una etiqueta que miente sobre su contenido.',

        'Y aquí está la pieza que hay que ver con claridad, porque es la que conecta los tres regímenes. Esta práctica —la reserva fraccionaria— no es un vicio exclusivo de los bancos privados. Es <em>el mismo mecanismo</em> que el banco central lleva al extremo. La pregunta, entonces, no es quién hace reserva fraccionaria, sino qué tan lejos puede llegar sin que nada lo frene. Y aquí, en la banca libre, hay dos frenos poderosos que el banco central no tiene. El primero: el oro. Por más recibos falsos que emita, este banco sigue anclado a un metal real que no puede fabricar —su mentira tiene un techo—. El segundo: el miedo. Sin un Estado que lo respalde, un banco que emite de más vive amenazado: si la gente sospecha y acude a reclamar su oro, el banco quiebra ese mismo día. Esa amenaza constante lo obliga a contenerse.',

        'Por eso ocurre algo que sorprende incluso a quien desconfía de los bancos. Este régimen falsifica la señal, sí —pero mucho menos que el banco central, porque el mercado lo disciplina—. Lejos de inflar la moneda sin límite, como suele temerse, Rothbard sostiene lo contrario:',

        ("quote",
         '“El sistema de libertad bancaria llevó a un sistema monetario mucho más sólido del que hoy tenemos.”',
         'Rothbard, <em>¿Qué ha hecho el gobierno de nuestro dinero?</em>'),

        'El falsificador privado vive con la soga al cuello. Lo que la banca central añadirá —lo veremos enseguida— es precisamente cortar esa soga: quitar el ancla del oro y poner a alguien que rescate al banco cuando lo atrapen. La reserva fraccionaria sin freno. Eso, y no otra cosa, es el banco central.',
    ]),
    ("Los tres, juntos", [
        'Tenemos ya los tres frente a nosotros, y conviene verlos juntos por última vez. El <strong>dinero duro</strong> —el oro, y sobre todo Bitcoin— respeta el acuerdo: nadie puede crear unidades de la nada, así que la señal dice la verdad. La <strong>banca libre con reserva fraccionaria</strong> lo rompe a medias: emite pasivos del banco haciéndolos pasar por recibos de un oro que no existe, pero anclada a un metal real y disciplinada por el miedo a la quiebra, su mentira tiene techo. La <strong>banca central</strong> lo rompe del todo: la misma reserva fraccionaria, pero sin ancla —pasivos puros, sin ningún activo real detrás— y sin freno —alguien rescata al banco cuando lo atrapan—. Tres formas de tratar una sola promesa: cumplirla, romperla con límite, romperla sin límite.',

        'Y aquí hay que decir algo que incomoda, porque va contra la intuición de casi todos. Si usted siente que la banca libre con reserva fraccionaria es “más o menos aceptable” —que al fin y al cabo es privada, compite, está anclada al oro— y que el verdadero villano es solo el banco central, hay una parte en la que se equivoca y una parte en la que tiene razón. Conviene separarlas con cuidado, porque en esa separación está la lección entera del capítulo.',

        'Piénselo así, que es la forma más simple de verlo: robar diez pesos y robar mil no son delitos distintos —son el mismo delito, en distinta cantidad—. Entre la banca libre y la banca central pasa exactamente eso: una falsifica poco, la otra sin medida. En cuanto a falsificar la señal, son la misma falta —y por eso ninguna de las dos merece llamarse dinero honesto—. El único régimen que de verdad respeta el acuerdo es el primero, el dinero duro.',

        'Pero falta el segundo pecado, y es el más grave —tan grave que conviene no cerrar sin decirlo—. Hasta aquí juzgamos a los dos falsificadores por <em>cuánto</em> mienten. Y ahí la banca libre sale mejor parada: miente poco, porque el mercado la disciplina. Pero hay algo que la banca libre, por privada, <em>no puede hacer</em>, y que la banca central hace por definición: obligarlo a usted a aceptar su dinero. Al banco privado que falsifica usted puede abandonarlo —llevarse su oro, cambiar de banco, rechazar sus recibos—. Al banco central no, porque detrás de él está la fuerza del Estado: prohíbe que cualquier otro emita dinero —quien lo intente va preso, “por falsificador”— y lo obliga a usted por ley a aceptar el suyo, eso que llaman <em>curso legal</em>. Rothbard lo pone junto a los otros monopolios coercitivos del Estado: así como llama recaudación al robo legalizado y conscripción al secuestro legalizado, llama política monetaria a la falsificación legalizada.',

        'Y no es solo Rothbard quien lo ve así. Hayek —que llegó al problema del dinero por un camino muy distinto, el de la competencia y el conocimiento, no el del fraude— señaló lo mismo sobre ese mecanismo legal que lo obliga a aceptar la moneda del Estado:',

        ("quote",
         '“El curso legal es simplemente una estratagema jurídica para obligar a la gente a que acepte como cumplimiento de un contrato algo que nunca pretendió cuando lo firmó.”',
         'Hayek, <em>La desnacionalización del dinero</em> (1976)'),

        'Dos pensadores que discrepaban en mucho —incluso en si la reserva fraccionaria es o no un fraude— coinciden, sin embargo, en este punto: lo que distingue al dinero del Estado no es que falsifique, porque eso también puede hacerlo un privado. Es que lo obliga a usted, por la fuerza de la ley, a aceptar esa falsificación. La coerción es la línea que ninguno de los dos perdona.',

        'Por eso la pregunta de quién controla el dinero —la que el debate de siempre plantea— no era superficial: era decisiva, solo que por una razón más honda de la que el debate ve. No importa por una cuestión de banderas, de público contra privado en abstracto. Importa porque <em>solo lo público trae la fuerza</em>, y la fuerza es lo que convierte una mentira que usted podría rechazar en una mentira que está obligado a vivir. El falsificador privado le miente y usted puede irse. El falsificador estatal le miente y le cierra la puerta. Esa es la diferencia que de verdad condena a la banca central por encima de todo lo demás —no que falsifique más, sino que lo encadene a su falsificación—.',

        'Antes de seguir, conviene detenerse en algo que cambiará la forma de leer todo lo que viene. Estos tres regímenes no son un asunto que ahora cerramos para pasar a otra cosa. Son el suelo sobre el que se parará el resto del libro. Porque cada cosa que examinaremos de aquí en adelante —la paciencia de una sociedad, su ahorro, la tasa de interés, los precios que coordinan a millones— no flota en el aire: viaja sobre el dinero. Y por eso hereda su honestidad o su mentira. Donde el dinero respeta el acuerdo, esas señales pueden decir la verdad. Donde el dinero se crea de la nada, todas nacen contaminadas: no hay forma de que la tasa diga la verdad si el dinero que la expresa es falso, ni de que el ahorro signifique algo si puede fabricarse de un plumazo. El tipo de dinero no es un tema más entre otros: es la condición de que todos los demás puedan funcionar. Esa es la razón profunda detrás del título de este libro —y la iremos viendo, señal por señal, hasta que al final no quede duda—.',

        'Con esto cerramos los cimientos. Ya sabemos qué es el dinero —el sistema que transporta la información con que todos decidimos—, con qué vara se juzga —si esa información dice la verdad— y cuáles son las tres formas de organizarlo según cuánto la respetan. Pero hemos hablado de “la señal”, de “la información”, como si fueran una sola cosa abstracta. No lo son. La información que el dinero transmite tiene una forma concreta, cotidiana, que usted lee todos los días sin saber que la lee: son los precios, y sobre todo uno de ellos, el más importante y el más manipulado de todos. A entenderlo dedicaremos lo que viene. Pero antes necesitamos dos piezas que están debajo de todo precio: la paciencia, y lo que ocurre cuando alguien ahorra.',
    ]),
]

# CSS de .lema + .pull-quote (.lema sobrescribe el blockquote base del esqueleto)
EXTRA_CSS = """
/* ===== Máxima destacada: centrada, con filetes finos arriba y abajo ===== */
blockquote.lema {
  margin: 2.8rem 0; padding: 1.4rem 1rem;
  border-left: none;
  border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule);
  text-align: center; font-style: italic;
  font-size: 1.18rem; line-height: 1.5; color: var(--ink);
}
/* ===== Citas de autor — filete fino gris a la izquierda ===== */
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
for sec_title, items in CONTENT:
    if sec_title:
        parts.append(f'\n    <span class="section-num">{sec_title}</span>\n')
    for it in items:
        if isinstance(it, str):
            parts.append(f'    <p>{it}</p>\n')
        elif it[0] == "lead":
            parts.append(f'    <p class="lead">{it[1]}</p>\n')
        elif it[0] == "lema":
            parts.append(f'    <blockquote class="lema">{it[1]}</blockquote>\n')
        elif it[0] == "quote":
            _, qtext, atrib = it
            parts.append('\n    <blockquote class="pull-quote">\n')
            parts.append(f'      <p>{qtext}</p>\n')
            parts.append(f'      <cite>{atrib}</cite>\n')
            parts.append('    </blockquote>\n\n')
parts.append('\n  </div>\n\n</article>')
article = ''.join(parts)

# ---- Esqueleto del cap 3 ----
sk = open('tres-regimenes.html', encoding='utf-8').read()
out = sk
out = re.sub(r'<title>.*?</title>',
             '<title>Las tres formas de organizar el dinero — Arregla el dinero, arregla el mundo</title>',
             out, count=1, flags=re.DOTALL)
out = re.sub(r'<article class="page"[^>]*>.*?</article>', lambda _m: article, out, count=1, flags=re.DOTALL)
new_nav = ('<nav class="nav-foot">'
           '<a class="prev" href="criterio-de-evaluacion.html">El criterio de evaluación</a>'
           '<a class="idx" href="index.html">Índice</a>'
           '<a class="next" href="preferencia-temporal.html">La preferencia temporal</a></nav>')
out = re.sub(r'<nav class="nav-foot">.*?</nav>', lambda _m: new_nav, out, count=1, flags=re.DOTALL)
out = out.replace('</style>', EXTRA_CSS + '</style>', 1)
out = out.replace('audio/tres-regimenes.mp3', 'audio/tres-formas-organizar-dinero.mp3')
out = out.replace('audio/tres-regimenes.alignment.json', 'audio/tres-formas-organizar-dinero.alignment.json')
out = out.replace('data-storage-key="tres-regimenes"', 'data-storage-key="tres-formas-organizar-dinero"')

open('tres-formas-organizar-dinero.html', 'w', encoding='utf-8').write(out)
n_par = sum(1 for s, items in CONTENT for it in items if isinstance(it, str) or (isinstance(it, tuple) and it[0] in ('lead',)))
n_lema = sum(1 for s, items in CONTENT for it in items if isinstance(it, tuple) and it[0] == 'lema')
n_quote = sum(1 for s, items in CONTENT for it in items if isinstance(it, tuple) and it[0] == 'quote')
n_sec = sum(1 for s, _ in CONTENT if s)
print("tres-formas-organizar-dinero.html creado")
print(f"párrafos: {n_par} | lemas: {n_lema} | citas: {n_quote} | secciones: {n_sec}")
