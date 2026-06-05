#!/usr/bin/env python3
"""Construye el capítulo bisagra «¿Y por qué no volver al oro?» con la
estructura del libro, usando el esqueleto del cap 3 (toda la maquinaria).
Deja los identificadores de audio apuntando a por-que-no-volver-al-oro;
el audio + spans se agregan después con el flujo normal.

Los recuadros de datos y la cita destacada se marcan con clase `no-audio`:
ni extract_text los manda a TTS ni inject_word_spans los envuelve, así que
se ven como cajas pero NO se narran ni entran al karaoke."""
import re

EYEBROW = "Antes de seguir · La pregunta inevitable"
TITLE = "¿Y por qué no volver al oro?"
SUBTITLE = "Por qué el dinero más honesto de la historia no alcanza"

# Items por sección:
#   ("lead", texto)               → primer párrafo con capital
#   "texto"                       → párrafo normal (se narra)
#   ("recuadro", label, [paras])  → caja de datos (NO se narra)
#   ("quote", texto, cita)        → cita destacada (NO se narra)
CONTENT = [
    (None, [
        ("lead", 'Llegamos a algo incómodo: el oro y Bitcoin son, los dos, dinero honesto. Ninguno miente sobre su origen, ninguno se crea por decreto. Y entonces la pregunta cae por su propio peso —quizá usted ya la tiene en la punta de la lengua—: si el oro es honesto, si sostuvo el comercio del mundo durante milenios, si lo conocemos y le tenemos confianza, ¿para qué Bitcoin? ¿Por qué no volver, sencillamente, al oro?'),
        ('Es la pregunta correcta. Y merece que se la responda de frente, sin esquivarla. En el capítulo de los tres regímenes le dejé una deuda: dije que había una diferencia entre el oro y Bitcoin a la que tendríamos que volver, una que parecía un asunto práctico y resultaría ser, en el fondo, una cuestión de honestidad. Es hora de pagar esa deuda. Y no lo haré con teoría, sino con algo más simple: imagine que de verdad volvemos al oro. Acompáñeme por un día cualquiera de esa vida, y veamos, escena por escena, qué gana —y qué le cuesta.'),
    ]),
    ("El café", [
        ('Empecemos por lo más pequeño. Vuelve el oro, y con él una regla de medir escasa y firme; eso lo gana, y no es poco. Ahora entre a una cafetería y pida un café.'),
        ('Llega el momento de pagar. Lo que tiene en el bolsillo es oro, y un café cuesta una fracción minúscula de un gramo. ¿Raspa una viruta del lingote sobre el mostrador? ¿Saca una balanza de precisión para pesar el polvillo? ¿Y el hombre detrás de la caja, cómo sabe que ese polvo amarillo es oro y no latón molido? La escena es absurda, y el absurdo es la prueba: el oro no se deja partir en pedazos lo bastante pequeños para la vida de todos los días.'),
        ('Por eso, en toda la historia, nadie pagó jamás un café con oro. Se pagó con un papel —un recibo que prometía “vale por un gramo”— que sí se podía dividir, contar y entregar. Para usar el oro en lo cotidiano hubo que dejar de tocar el oro y empezar a pasar de mano en mano una promesa de oro. No es una rareza moderna: esa misma grieta de escala es tan vieja como la acuñación. El oro nunca alcanzó para la transacción pequeña, y por eso la humanidad tuvo que poner debajo de él una moneda más blanda —la plata, el cobre— para las compras de cada día. El oro jamás fue, ni una sola vez en milenios, dinero de bolsillo. Subraye esto, porque va a repetirse toda la tarde: para gastarlo, tuvo que meter un papel entre usted y el metal.'),
    ]),
    ("La huida", [
        ('Subamos la apuesta. Ya no es un café: es su vida entera, y tiene que irse.'),
        ('No de viaje. Irse. Es la historia de millones de latinoamericanos en una sola generación: los que salieron de Venezuela cuando el dinero dejó de comprar el pan, los que salieron de Cuba hace sesenta años, los que en cualquier país amanecieron bajo un gobierno que ya no los quería allí. Usted fue de los previsores: no dejó sus ahorros en una moneda que se derretía, los guardó en oro, la regla que no se deprecia. Hizo todo bien. Y ahora tiene que cruzar una frontera con su vida entera encima.'),
        ('Ahí el oro lo abandona, justo en la hora en que más lo necesita. Porque el oro es un cuerpo: pesa, brilla, suena, se detecta. Lo que se carga encima, en una frontera, se revisa, se declara, se decomisa. El que controla el puesto de aduana controla su oro. Y si para evitarlo se lo confía a alguien —a un banco, a un custodio del otro lado— entonces ya no es suyo: es de aquel en quien tuvo que confiar, el que puede congelar la cuenta, demorar la entrega, o devolvérselo precisamente a quienes usted huía. Para sacar su oro a salvo, tuvo que entregárselo a un tercero. La regla que no se deprecia no sirve de nada si se la quitan en la raya de la frontera. Y aquí asoma, por contraste, lo que el oro nunca pudo ser: el que huye con oro carga un cuerpo que lo delata; el que huye con Bitcoin no carga nada y, sin embargo, lo lleva todo. Su fortuna entera puede caber en una frase guardada en la memoria, una hilera de palabras que ninguna aduana puede pesar, declarar ni decomisar.'),
    ]),
    ("El cable", [
        ('Pero no hace falta huir para que el oro se quede mudo. Basta con encender el computador.'),
        ('Quédese en su casa, tranquilo, y trate de pagar la suscripción de un servicio en otro país, o de mandarle dinero a un hijo que estudia al otro lado del mundo. ¿Cómo mete el oro por el cable? No puede. El oro no viaja por internet —y el mundo entero, hoy, vive por internet—. Para entrar a esa economía tendría que volver, una vez más, a lo de siempre: alguien que guarde su oro en una bóveda y mueva por usted un número en una pantalla que dice representarlo. El papel otra vez, ahora disfrazado de saldo digital; el tercero otra vez, ahora disfrazado de aplicación.'),
        ("recuadro", "Lo que cuesta mover el metal", [
            'El dato no es retórico, es de transportista. Enviar un solo lingote <em>good delivery</em> —400 onzas, unos 750.000 dólares— a través del Atlántico cuesta cerca de 3.000 dólares y tarda dos o tres días, y eso sin verificar su contenido. Cuando Alemania quiso repatriar sus reservas desde Nueva York y París, la operación tardó cuatro años (2013-2017).',
            'Ese peso no es un inconveniente menor: es la causa mecánica de todo lo demás. Como sólo unas pocas instituciones podían liquidar valor a larga distancia —algo que el oro físico no lograba—, el rol del dinero se les fue de las manos a las personas y se concentró en los bancos centrales. La lentitud del oro no acompañó al poder monetario del Estado: lo creó.',
        ]),
        ('Y aquí lo que está en juego ya no es su comodidad. Es algo mucho más grande. La riqueza de una civilización no sale de la tierra ni de las minas: sale de los intercambios. De millones de desconocidos que comercian entre sí, cada uno dedicado a lo que mejor sabe hacer, confiando en que podrá cambiar su trabajo por el de los demás. Mientras más fluidos son esos intercambios, más profunda se vuelve esa división del trabajo, y más riqueza brota de ella. Un dinero que no puede moverse a la velocidad ni al alcance del mundo moderno no es un dinero incómodo: es un torniquete sobre la circulación de la que vive la prosperidad. Volver al oro en plena era digital no sería un paso atrás pintoresco. Sería cortarle el riego a la economía y verla secarse.'),
    ]),
    ("El lingote que podría ser plomo", [
        ('Hay una grieta más, y es la más callada de todas, porque parece confianza y es dependencia.'),
        ('Vuelva a ese lingote en su mano. ¿Cómo sabe que es oro? Un lingote de oro macizo y un lingote de plomo bañado en oro pesan distinto, sí —pero usted no lo nota a simple vista, ni el que se lo vende, ni el que se lo recibirá mañana—. Para estar seguro, alguien tiene que ensayarlo: perforarlo, sumergirlo, atacarlo con ácido, pasarle un haz que lea su interior. Es decir: para confiar en su propio oro, usted necesita a un experto que se lo certifique. Y en ese instante deja de confiar en el oro y empieza a confiar en el experto, en su sello, en su honradez. La honestidad del oro es real —pero usted no la puede comprobar con sus propias manos—. También eso tiene que delegarlo.'),
        ('Y no crea que es problema solo del ciudadano de a pie. En un lingote de ese tamaño, la única forma de estar completamente seguro de lo que hay dentro es fundirlo y volver a fundirlo de nuevo. Cuando el banco central alemán recuperó su oro, hizo exactamente eso: lo derritió todo y lo recoló en lingotes nuevos para verificar su pureza. Un Estado, con todos sus recursos, no confió en su propio oro sin antes destruirlo. Si el Bundesbank tuvo que pasar su oro por el fuego para creerle, ¿qué hará usted en el mostrador de la cafetería?'),
        ("recuadro", "Verificar oro · verificar Bitcoin", [
            'El contraste austriaco es exacto. Verificar oro exige espectrómetros de varios miles de dólares —o, en el peor caso, el horno—. Verificar Bitcoin exige un nodo que cuesta entre 100 y 700 dólares una sola vez, y que después comprueba cada pago del mundo a un costo casi nulo. Por eso Ammous describe Bitcoin como un sistema construido sobre “cien por cien de verificación y cero por ciento de confianza”. El oro le pide creer en alguien; Bitcoin le permite comprobar usted mismo.',
        ]),
    ]),
    ("El tiempo", [
        ('Y queda el costo más invisible de todos, porque no aparece en ninguna cuenta y sin embargo es el más caro.'),
        ('Volver al oro es volver a la fricción. Ir hasta el lugar. Hacer la fila. Cargar el metal o el papel que lo sustituye. Esperar a que lo cuenten, lo pesen, lo verifiquen. Cada recibo de la luz, cada pago del agua, cada arriendo, convertido de nuevo en una diligencia de medio día. Y esa factura no se paga en oro: se paga en horas. En horas de su vida que no regresan jamás.'),
        ('Recuerde cómo empezó este libro. Empezó con el tiempo —con la preferencia temporal, con la paciencia como la materia prima de todo lo que un ser humano construye—. El dinero, el oro, la tierra: todo se puede perder y recuperar. El tiempo no. Es lo único de verdad escaso que poseemos. Y aquí se cierra un círculo cruel. La civilización entera, dijimos al comienzo, es el lento descenso de la preferencia temporal: aprender a valorar el mañana lo bastante como para construirlo. El dinero duro debía servir a eso, enseñarnos a esperar. Por eso esta es la ironía más amarga del oro: lo llamamos escaso, lo atesoramos por escaso —y al obligarnos a gastar nuestras horas en cada transacción, nos hace derrochar a manos llenas lo único que de verdad no nos sobra. El metal que debía bajarnos la preferencia temporal nos la sube, porque nos quema en fricción las horas que son la medida misma del futuro. El oro cuida su propia escasez quemando la nuestra.'),
    ]),
    ("Todas las grietas dan a la misma puerta", [
        ('Detengámonos y miremos el día completo, las escenas una al lado de la otra. El café que no se puede partir. El oro que se queda en la aduana. El metal que no entra por el cable. El lingote que hay que certificar. Las horas que se evaporan. Parecían cinco molestias distintas, cinco inconvenientes sueltos. No lo son. Todas terminaron en el mismo gesto, repetido una y otra vez: para usar el oro, usted tuvo que ponerlo en manos de otro.'),
        ('Y un dinero que solo puede usarse en manos de otros es un dinero que, tarde o temprano, termina junto en manos de unos pocos. En las bóvedas. En los bancos. En las casas que lo custodian. En los Estados. La concentración del oro no fue una desgracia ni la obra de un villano: fue su destino físico, escrito en su propia naturaleza. No es que el oro no tuviera adversarios —los tuvo, y muchos: todo gobierno que quiso inflar, toda guerra que hubo que financiar, todo planificador que necesitó manipular precios vio en el oro un estorbo, como advirtió Mises—. Pero ningún enemigo habría bastado si la propia naturaleza del metal no les hubiera abierto la puerta. El oro, por ser lo que es, rueda siempre hacia donde alguien lo guarde.'),
        ("quote",
         '“La centralización del oro lo hizo vulnerable a que sus enemigos usurparan su rol monetario; y el oro, simplemente, tenía demasiados enemigos.”',
         '— Saifedean Ammous parafraseando a Ludwig von Mises, <em>El Patrón Bitcoin</em>'),
        ('Y ya sabemos —lo vimos entero, en el capítulo de los tres regímenes— qué ocurre cuando el dinero honesto se amontona en pocas manos. De las bóvedas repletas nacieron los recibos. De los recibos, la tentación de firmar más de los que había oro detrás. De esa tentación, el dinero creado de la nada. Y conviene ver que esa tentación no fue un vicio añadido al oro desde fuera: fue lo que su propia torpeza para moverse hizo posible. Precisamente porque a nadie le resultaba fácil ir a la bóveda a redimir su metal y gastarlo al otro lado del mundo, el custodio descubrió que podía firmar más recibos que el oro guardado, casi sin riesgo de que se lo reclamaran todo a la vez. Volver al oro no es regresar a un refugio a prueba de todo: es volver a subirse a la misma rampa que, por su propia inclinación, ya nos hizo resbalar una vez hasta el fondo del fraude. El oro no nos traicionó por mala suerte. Nos entregó al dinero falso porque sus grietas nos obligaban a delegar, y delegar es siempre el primer paso de la falsificación.'),
        ("recuadro", "La trampa final · el oro ya es fiat", [
            'Hay un último giro, y es el más revelador. El oro de hoy ni siquiera escapa a lo que describe este capítulo: el sistema mundial de lingotes <em>good delivery</em> exige que el metal permanezca en manos de custodios autorizados. Si usted toma posesión física de su lingote, sale de la red: queda con un objeto caro de mover, caro de partir y caro de reintegrar. El oro “bueno” es, en la práctica, un saldo en el registro de unos pocos custodios.',
            'Es decir: el oro terminó comportándose como un token fiat sobre una red de pagos privada. Su dureza importa cada vez menos cuando, para circular, depende del permiso de quien lo guarda. La concentración no es solo el destino físico del oro: el sistema actual la vuelve obligatoria.',
        ]),
    ]),
    ("El dinero vuelve a ser lo que siempre fue", [
        ('Y mientras el oro rueda hacia sus bóvedas, el mundo corre en la dirección contraria.'),
        ('Cada año los intercambios son más veloces, más globales, más automáticos. Ya hay sistemas que se liquidan solos, suscripciones que se cobran sin que nadie levante un dedo, máquinas que le pagan a otras máquinas por la electricidad o los datos que consumen. El dinero se está despojando de todo lo accesorio —del peso, del traslado, del papel, del intermediario— y regresa a lo que este libro viene diciendo desde su primera página que siempre fue, debajo de cada disfraz: información que viaja. Valor que se transmite de un punto a otro del mundo.'),
        ('En esa forma desnuda, el oro no puede ni asomarse. No hay manera de empujar un gramo de metal por una fibra óptica, ni de que dos máquinas se pasen un lingote a la velocidad de la luz. El oro, en la era de la información, es un cuerpo demasiado pesado para un mundo que se volvió señal. Bitcoin, en cambio, no tiene esa cualidad: es esa cualidad. Es información honesta que se transmite sin que nadie la pese, la guarde, la apruebe o la detenga. Es verdad que viaja sin ruido y sin permiso. Todo lo que el oro solo podía hacer delegando —en papeles, en custodios, en expertos, en bancos—, Bitcoin lo hace directo, de una persona a otra, sin un alma en el medio.'),
        ('Aquí está, por fin, la respuesta. No volvemos al oro porque el oro siempre nos puso frente a una elección imposible: ser honesto pero inservible sin entregárselo a alguien, o volverse servible entregándolo —y perder, en esa entrega, la honestidad—. Durante siglos esa fue la única disyuntiva que la humanidad conoció, y la resolvió mal: eligió la comodidad del papel, y el papel la arrastró al fraude. Y conviene ser justo con el metal: quizá, en un mundo distinto —uno gobernado por ingenieros y no por tesorerías hambrientas—, el oro habría podido sostener su honestidad un poco más. Pero ese mundo no existió nunca. En el mundo real, el de los Estados que necesitan financiarse, la torpeza física del oro fue siempre una invitación abierta a confiscarlo y a falsificarlo, y la invitación se aceptó cada vez. Bitcoin es la primera vez en la historia en que no hay que elegir. Honesto y ejercible sin permiso. Honesto y divisible hasta lo infinitesimal, transportable a la velocidad de la luz, verificable por uno mismo, imposible de juntar a la fuerza en una sola bóveda. No es un oro mejor. Es lo que el oro, por más que quisiéramos, nunca pudo llegar a ser.'),
        ('Ya sabemos, entonces, cuál es el dinero que dice la verdad, y por qué. Pero queda la pregunta más dura, la que de verdad importa. No cuál dinero elegir —eso ya está resuelto—, sino qué le ha hecho al mundo el dinero que no elegimos a conciencia y sin embargo gobierna nuestras vidas: el que se crea de la nada, el que miente en cada señal. A rastrear las huellas que esa falsificación ha dejado en el mundo real —en los bosques, en la comida, en las guerras, en el alma misma de la gente— dedicaremos todo lo que viene.'),
    ]),
]

# CSS extra para recuadros y cita (no existe en el esqueleto)
EXTRA_CSS = """
/* ===== Recuadros (apartados de datos, no se narran) y cita destacada ===== */
.prose .recuadro {
  margin: 2.4rem 0; padding: 1.4rem 1.6rem;
  background: var(--surface); border: 1px solid var(--rule);
  border-left: 3px solid var(--verde); border-radius: 8px;
  font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
}
.prose .recuadro .recuadro-tag {
  display: block; font-size: 0.7rem; letter-spacing: 0.16em;
  text-transform: uppercase; color: var(--verde); margin-bottom: 0.9rem;
}
.prose .recuadro p {
  font-size: 0.92rem; line-height: 1.62; color: var(--ink-soft); margin: 0 0 0.7rem;
}
.prose .recuadro p:last-child { margin-bottom: 0; }
.prose .recuadro em { font-style: italic; color: var(--ink); }
.prose .recuadro strong { color: var(--ink); font-weight: 600; }

.prose .pull-quote {
  margin: 2.8rem 0; padding: 0.2rem 0 0.2rem 1.6rem;
  border-left: 3px solid var(--verde);
}
.prose .pull-quote p {
  font-size: 1.24rem; font-style: italic; line-height: 1.5; color: var(--ink); margin: 0 0 0.8rem;
}
.prose .pull-quote cite {
  display: block; font-style: normal; font-size: 0.84rem; letter-spacing: 0.02em;
  color: var(--ink-soft); font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
}
.prose .pull-quote cite em { font-style: italic; }
@media (max-width: 640px) {
  .prose .recuadro { padding: 1.1rem 1.2rem; }
  .prose .pull-quote p { font-size: 1.1rem; }
}
"""

# ---- Construir el HTML del article ----
parts = ['<article class="page">\n',
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
        elif it[0] == "recuadro":
            _, label, paras = it
            parts.append('\n    <aside class="recuadro no-audio">\n')
            parts.append(f'      <span class="recuadro-tag">{label}</span>\n')
            for pp in paras:
                parts.append(f'      <p>{pp}</p>\n')
            parts.append('    </aside>\n\n')
        elif it[0] == "quote":
            _, qtext, cite = it
            parts.append('\n    <blockquote class="pull-quote no-audio">\n')
            parts.append(f'      <p>{qtext}</p>\n')
            parts.append(f'      <cite>{cite}</cite>\n')
            parts.append('    </blockquote>\n\n')
parts.append('\n  </div>\n\n</article>')
article = ''.join(parts)

# ---- Esqueleto del cap 3 ----
sk = open('tres-regimenes.html', encoding='utf-8').read()
out = sk
out = re.sub(r'<title>.*?</title>',
             '<title>¿Y por qué no volver al oro? — Arregla el dinero, arregla el mundo</title>',
             out, count=1, flags=re.DOTALL)
out = re.sub(r'<article class="page">.*?</article>', lambda _m: article, out, count=1, flags=re.DOTALL)
# nav-foot: prev=auditabilidad, sin next (deforestación aún no existe)
new_nav = '<nav class="nav-foot"><a class="prev" href="auditabilidad.html">La auditabilidad del dinero</a><a class="idx" href="index.html">Índice</a><span></span></nav>'
out = re.sub(r'<nav class="nav-foot">.*?</nav>', lambda _m: new_nav, out, count=1, flags=re.DOTALL)
# CSS extra antes de </style>
out = out.replace('</style>', EXTRA_CSS + '</style>', 1)
# identificadores de audio
out = out.replace('audio/tres-regimenes.mp3', 'audio/por-que-no-volver-al-oro.mp3')
out = out.replace('audio/tres-regimenes.alignment.json', 'audio/por-que-no-volver-al-oro.alignment.json')
out = out.replace('data-storage-key="tres-regimenes"', 'data-storage-key="por-que-no-volver-al-oro"')

open('por-que-no-volver-al-oro.html', 'w', encoding='utf-8').write(out)
n_par = sum(1 for s, items in CONTENT for it in items if isinstance(it, str) or it[0] == "lead")
n_box = sum(1 for s, items in CONTENT for it in items if isinstance(it, tuple) and it[0] in ("recuadro", "quote"))
print("por-que-no-volver-al-oro.html creado")
print(f"párrafos narrados: {n_par} | cajas no-audio: {n_box} | secciones: {sum(1 for s,_ in CONTENT if s)}")
