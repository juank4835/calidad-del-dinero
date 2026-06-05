#!/usr/bin/env python3
"""Construye el capítulo bisagra «¿Y por qué no volver al oro?» con la
estructura del libro, usando el esqueleto del cap 3 (toda la maquinaria).
Deja los identificadores de audio apuntando a por-que-no-volver-al-oro;
el audio + spans se agregan después con el flujo normal."""
import re, html as html_mod

EYEBROW = "Antes de seguir · La pregunta inevitable"
TITLE = "¿Y por qué no volver al oro?"
SUBTITLE = "Por qué el dinero más honesto de la historia no alcanza"

# (section_title or None, [parrafos])
CONTENT = [
    (None, [
        ("lead", 'Llegamos a algo incómodo: el oro y Bitcoin son, los dos, dinero honesto —ninguno miente sobre su origen, ninguno se crea por decreto—. Y entonces la pregunta es inevitable, quizá ya la tiene en la punta de la lengua: si el oro es honesto, si funcionó durante milenios, ¿para qué Bitcoin? ¿Por qué no volver, sencillamente, al oro? En el capítulo de los tres regímenes prometí volver a una diferencia entre ambos que parecía práctica y resultaría ser de honestidad. Es hora. Y la mejor forma de responder no es con teoría: imagine que de verdad volvemos al oro, y veamos, situación por situación, qué gana y qué pierde.'),
    ]),
    ("El café", [
        ('Empecemos por lo más cotidiano. Vuelve el oro, y con él una regla escasa y firme para medir el valor —eso lo gana, y no es poco—. Ahora entre a una cafetería y pida un café. Llega el momento de pagar, y lo que tiene es oro: un café cuesta una fracción minúscula de un gramo. ¿Raspa una viruta del lingote sobre el mostrador? ¿Lleva una balanza de precisión para pesar lo que raspó? ¿Y el tendero, cómo sabe que eso que usted raspó es oro y no latón? El absurdo de la escena es el problema: el oro no se deja partir en pedazos lo bastante pequeños para la vida diaria.'),
        ('Por eso, en la práctica, nadie pagó nunca el café con oro. Se pagó con un papel —un recibo que decía "vale por un gramo"— que sí se podía partir, contar y pasar de mano en mano. Para usar el oro en lo cotidiano hubo que dejar de usar el oro y empezar a usar algo que lo representara. Guarde ese detalle: para gastarlo, tuvo que interponer un papel entre usted y el metal. Volveremos a él.'),
    ]),
    ("La huida", [
        ('Pasemos a algo más grave que un café. Imagine que tiene que irse. No de vacaciones: irse. Le ha pasado a millones de latinoamericanos en una sola generación —los que salieron de Venezuela cuando el dinero ya no compraba nada, los que salieron de Cuba décadas atrás, los que en cualquier país han tenido que empezar de cero en otra parte—. Usted fue previsor: no guardó su riqueza en una moneda que se derrite, la guardó en oro, la regla que no se deprecia. Hizo lo correcto. Ahora tiene que cruzar una frontera con ella.'),
        ('Y ahí el oro le falla, justo cuando más lo necesita. El oro es un cuerpo físico: pesa, se ve, se detecta. Para pasarlo tiene que llevarlo encima —y en una frontera, lo que se lleva encima se puede revisar, declarar, decomisar—. El que controla la salida controla su oro. Para evitarlo, solo le queda una salida: confiárselo a alguien que lo guarde o lo mueva por usted —un banco, un custodio del otro lado—. Otra vez, para proteger el oro, tuvo que ponerlo en manos de un tercero. Y un tercero es alguien en quien hay que confiar… y que puede fallar, congelar la cuenta, o entregar el oro a quien usted huía. Guarde también este detalle: para mover su oro a salvo, tuvo que entregárselo a alguien.'),
        ('Y ni siquiera hace falta cruzar una frontera para que el oro le falle. Quédese en su casa, abra el computador, y trate de pagar algo en una tienda de otro país, o de enviarle dinero a alguien al otro lado del mundo. ¿Cómo mete el oro por el cable? No puede. El oro no viaja por internet —y la economía entera, hoy, viaja por internet—. Para participar, tendría que volver a lo de siempre: un intermediario que tenga su oro guardado y mueva, en su nombre, un saldo digital que lo representa. Otra vez el papel, ahora vuelto número en una pantalla; otra vez el tercero en quien hay que confiar.'),
        ('Y esto no es un problema de comodidad —de no poder comprar en Amazon—. Es mucho más hondo. La riqueza de una sociedad nace de los intercambios: millones de personas que no se conocen, cada una haciendo lo que mejor sabe, comerciando entre sí. Mientras más intercambios fluyen, más se profundiza esa división del trabajo y más riqueza se crea. Un dinero que no puede moverse a la velocidad ni a la escala del mundo moderno no es solo incómodo: estrangula esos intercambios, y al estrangularlos, empobrece a todos. Volver al oro, en una era digital, sería amputar la circulación misma de la que vive la economía.'),
    ]),
    ("La pureza", [
        ('Hay una grieta más, y es la más silenciosa. Vuelva al lingote en su mano. ¿Cómo sabe que es oro? ¿Cómo lo sabe el que se lo vendió, el que se lo recibe, el que se lo guardará? A simple vista, un lingote de oro y un lingote de plomo bañado en oro son idénticos. Para estar seguro, alguien tiene que ensayarlo —perforarlo, pesarlo en agua, analizarlo con ácido o con rayos—. Es decir: para confiar en su propio oro, usted necesita a un experto que lo certifique. Y entonces ya no confía en el oro: confía en el experto. Cada vez que el oro cambia de manos, alguien tiene que volver a verificar, o todos tienen que confiar en el sello de alguien que lo verificó antes. La honestidad del oro existe —pero usted no la puede comprobar por sí mismo; tiene que delegar también eso.'),
    ]),
    ("El tiempo", [
        ('Y hay un costo más, el más silencioso de todos, porque no se ve hasta que se suma. Volver al oro significa volver a la fricción: ir a pagar, hacer fila, mover el metal o el papel que lo representa, esperar a que alguien lo cuente, lo pese, lo verifique. Cada pago de la luz, del agua, del arriendo, vuelto una diligencia. Y ese costo no se paga en dinero: se paga en tiempo —en horas de su vida que no vuelven—. Recuerde con qué empezó este libro: el tiempo, la paciencia, la disposición a esperar son la materia de todo lo que construimos. El tiempo es el único activo que de verdad no se puede fabricar ni recuperar. Un dinero que le devuelve fricción a cada intercambio le está cobrando en la moneda más cara que existe. El oro es escaso, sí; pero le hace derrochar lo único verdaderamente escaso, que son sus horas.'),
    ]),
    ("Todas las grietas llevan al mismo lugar", [
        ('Deténgase un momento y mire las escenas juntas. El café, la huida, el pago digital, la pureza, el tiempo: cada una parecía un inconveniente distinto, pero todas terminaron en el mismo punto. Para usar el oro —para dividirlo, moverlo, enviarlo, verificarlo— usted tuvo que entregárselo a un tercero. Y un dinero que tiene que vivir en manos de terceros termina, inevitablemente, concentrándose: en bóvedas, en bancos, en casas de custodia, en Estados. La centralización del oro no fue un accidente de la historia ni una maldad de alguien: fue su destino físico. El oro, por lo que es, tiende a juntarse donde alguien lo gestione.'),
        ('Y eso lo cambia todo, porque ya sabemos qué pasa cuando el dinero honesto se concentra en pocas manos. De esas bóvedas llenas de oro nacieron los papeles que lo representaban; de esos papeles, la tentación de emitir más de los que había oro detrás; de esa tentación, el dinero que se crea de la nada. Volver al oro no es volver a un refugio seguro: es volver a la rampa que, por su propia naturaleza, nos deslizó hacia el dinero falso la primera vez. El oro no nos traicionó por mala suerte. Nos llevó al fiat porque sus grietas obligaban a delegar, y delegar es el primer paso de la falsificación.'),
    ]),
    ("El dinero vuelve a ser lo que era", [
        ('Y mientras el oro se hunde en sus bóvedas, el mundo va hacia el lado contrario. Cada año los intercambios son más rápidos, más globales, más automáticos. Ya hay sistemas que se pagan entre sí sin que nadie apriete un botón —suscripciones que se liquidan solas, servicios que cobran al instante, máquinas que le pagan a otras máquinas por lo que consumen—. En ese mundo, el dinero se despoja de todo lo accesorio y vuelve a ser lo que este libro ha dicho desde la primera página que siempre fue: información que viaja. Valor que se transmite de un punto a otro.'),
        ('Y en esa forma pura, el oro no puede ni entrar. No hay manera de meter un gramo de oro por un cable, ni de que dos máquinas se pasen un lingote. El oro, en la era de la información, es un cuerpo demasiado pesado para un mundo que se volvió señal. Bitcoin, en cambio, es eso: información honesta que se transmite sin que nadie la toque, la pese, la guarde ni la apruebe. Verdad que viaja sin ruido y sin permiso. Lo que el oro solo podía ser delegando —en papeles, en custodios, en expertos—, Bitcoin lo es directamente.'),
        ('Aquí está, por fin, la respuesta a la pregunta. No volvemos al oro porque el oro nos pone ante una elección falsa: ser honesto pero imposible de ejercer sin entregárselo a alguien, o ser práctico entregándoselo —y perder, en esa entrega, la honestidad—. Durante siglos esa fue la única disyuntiva, y la humanidad la resolvió mal: eligió la comodidad del papel, y el papel la llevó al fraude. Bitcoin es la primera vez que no hay que elegir. Es honesto y se puede ejercer sin permiso. Honesto y divisible, transportable, verificable por uno mismo, imposible de concentrar a la fuerza. No es un oro mejor. Es lo que el oro nunca pudo ser.'),
        ('Y ahora que sabemos cuál es el dinero que dice la verdad —y por qué—, queda la pregunta más dura de todas. No la de qué dinero elegir, sino la de qué le ha hecho al mundo el dinero que elegimos: el que se crea de la nada, el que miente. A eso —a las huellas que la falsificación deja en el mundo real— dedicaremos lo que viene.'),
    ]),
]

# Construir el HTML del article
parts = ['<article class="page">\n',
         f'\n  <div class="chapter-eyebrow">{EYEBROW}</div>\n',
         f'  <h1 class="chapter-title">{TITLE}</h1>\n',
         f'  <p class="chapter-subtitle">{SUBTITLE}</p>\n',
         '\n  <div class="ornament">• • •</div>\n',
         '\n  <div class="prose">\n']
for sec_title, paras in CONTENT:
    if sec_title:
        parts.append(f'\n    <span class="section-num">{sec_title}</span>\n')
    for p in paras:
        if isinstance(p, tuple):  # lead
            parts.append(f'    <p class="{p[0]}">{p[1]}</p>\n')
        else:
            parts.append(f'    <p>{p}</p>\n')
parts.append('\n  </div>\n\n</article>')
article = ''.join(parts)

# Esqueleto del cap 3
sk = open('tres-regimenes.html', encoding='utf-8').read()
out = sk
out = re.sub(r'<title>.*?</title>',
             '<title>¿Y por qué no volver al oro? — Arregla el dinero, arregla el mundo</title>',
             out, count=1, flags=re.DOTALL)
out = re.sub(r'<article class="page">.*?</article>', lambda _m: article, out, count=1, flags=re.DOTALL)
# nav-foot: prev=auditabilidad, sin next (deforestación aún no existe)
new_nav = '<nav class="nav-foot"><a class="prev" href="auditabilidad.html">La auditabilidad del dinero</a><a class="idx" href="index.html">Índice</a><span></span></nav>'
out = re.sub(r'<nav class="nav-foot">.*?</nav>', lambda _m: new_nav, out, count=1, flags=re.DOTALL)
# identificadores de audio
out = out.replace('audio/tres-regimenes.mp3', 'audio/por-que-no-volver-al-oro.mp3')
out = out.replace('audio/tres-regimenes.alignment.json', 'audio/por-que-no-volver-al-oro.alignment.json')
out = out.replace('data-storage-key="tres-regimenes"', 'data-storage-key="por-que-no-volver-al-oro"')

open('por-que-no-volver-al-oro.html', 'w', encoding='utf-8').write(out)
print("por-que-no-volver-al-oro.html creado")
print("párrafos:", sum(len(p) for _, p in CONTENT), "| secciones:", sum(1 for s,_ in CONTENT if s))
