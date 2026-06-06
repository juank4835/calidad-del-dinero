#!/usr/bin/env python3
"""Construye el capítulo «La deforestación» (Bloque IV · cap 14) usando el
esqueleto del cap 3. Prosa con 4 subtítulos de sección, sin citas en bloque."""
import re

EYEBROW = "Primera consecuencia · lo más visible"
TITLE = "La deforestación"
SUBTITLE = "Por qué un hombre que ama su bosque termina talándolo —y no por maldad"

# (section_title or None, [items])
# items: ("lead", txt) | "texto"
CONTENT = [
    (None, [
        ("lead", 'Hay una imagen que todos llevamos puesta sin pensarla: la deforestación es obra de gente avara. Empresas que ven un bosque y ven dinero, taladores que arrasan por codicia, gobiernos que venden la selva al mejor postor. Donde hay un árbol caído, buscamos un culpable —alguien a quien le importó poco la naturaleza y mucho la ganancia—. Esa imagen es cómoda porque reparte el mundo en buenos y malos, y nos deja a nosotros del lado bueno. Y como casi todas las imágenes cómodas, esconde lo que de verdad importa.'),
        'Porque la mayor parte de los bosques del mundo no los talan villanos. Los talan personas que harían exactamente lo mismo que usted haría en su lugar, haciendo exactamente la cuenta que usted haría. Para ver eso hay que dejar de mirar al talador y empezar a mirar la cuenta que tiene delante. Y esa cuenta, como todo en este libro, está escrita en dinero.',
    ]),
    ("El hombre del nogal", [
        'Imagine a un hombre del mismo pueblo donde Juan apartaba su sueldo —llamémoslo Francisco— con un nogal en el fondo de su terreno. Lo plantó su padre, y desde hace años el árbol le da cada otoño una cosecha de nueces que Francisco vende en la plaza. No es una fortuna, pero es un ingreso fiel: llega todos los años, sin falta, como llegan los otoños.',
        'Un día se aparece un comprador de madera. El nogal es viejo y la madera es buena; el hombre le ofrece, por el árbol entero, lo que Francisco sacaría de unas quince cosechas de nueces. Una suma considerable, de golpe, hoy.',
        'Francisco hace la cuenta. Y aquí conviene mirar por encima de su hombro, porque la cuenta que hace es exactamente la que usted haría. Tiene dos opciones. Una: quedarse el árbol y seguir cobrando nueces cada otoño, año tras año, como hasta ahora —y dejárselo a sus hijos, que seguirán cobrando cuando él ya no esté—. Otra: cortarlo, cobrar de una vez el equivalente a quince cosechas, y quedarse sin árbol para siempre.',
        'Si Francisco confía en el futuro —si cree que habrá otoños, que sus nueces seguirán valiendo, que sus hijos heredarán un árbol vivo y no un tocón— la cuenta es fácil: no vende. Quince cosechas cobradas de a poco, más todas las que vendrán después, más la herencia, valen muchísimo más que la madera de una sola vez. El árbol vivo es un manantial; la madera, un balde. Nadie cambia un manantial por un balde si confía en que el manantial seguirá manando.',
        'Fíjese bien en lo que sostiene esa decisión. No es el amor de Francisco por los árboles, aunque lo tenga. No es conciencia ecológica, ni virtud, ni una ley que lo obligue. Es una cuenta —y una cuenta que sale a favor de conservar solo si Francisco puede confiar en que el futuro llegará y se parecerá al presente—. La conservación del bosque, aquí, no es un acto moral. Es el resultado frío de un cálculo que premia la espera. Francisco guarda el árbol por la misma razón por la que Juan, allá en el capítulo cinco, guardaba parte de su sueldo: porque el futuro le parece lo bastante firme como para que valga la pena esperarlo.',
    ]),
    ("Cámbiele una sola cosa", [
        'Ahora no le toque nada a Francisco. Déjele su amor por el árbol, su inteligencia, su prudencia, su cariño por los hijos que lo heredarán. No lo vuelva avaro ni tonto. Cámbiele una sola cosa, y la más invisible de todas: el dinero con que cobra las nueces.',
        'Hasta ahora cobraba en dinero honesto, del que no se puede fabricar de la nada. Cada peso que apartaba seguía valiendo el año siguiente, y el siguiente —así que, sin pensarlo, Francisco tenía un colchón—. Lo que le sobraba de las cosechas buenas lo guardaba para las malas; tenía con qué aguantar una enfermedad, un techo que se cae, un año flaco. Y porque tenía con qué aguantar, podía esperar. El nogal le daba de a poco, año tras año, y a él le bastaba con eso, porque tenía un respaldo debajo.',
        'Cámbiele ese dinero por uno que se diluye cada año. Y mire lo primero que desaparece: el colchón. Ahora lo que Francisco aparta se le derrite en las manos —guardar es perder—, así que deja de guardar. No por imprudente: porque ahorrar dejó de servir de nada. Lo vio usted entero en el capítulo del ahorro real: con dinero que no preserva valor, el ahorro ya no guarda pedazos del mundo para después; no guarda nada. Y un hombre que no puede ahorrar es un hombre que no puede esperar —porque esperar quince años de cosechas exige tener con qué vivir mientras llegan, y eso es precisamente lo que ya no tiene—.',
        'Aquí es donde la sensación se vuelve física, y conviene que la sienta usted también. Francisco tiene un nogal que es un manantial, sí: le dará nueces durante quince otoños. Pero hoy le llegó la cuenta del médico, o se le cayó media casa, o simplemente no alcanzó el mes. Y no hay colchón debajo, porque el dinero se lo comió. El manantial no sirve para hoy —el manantial da de a gotas, año tras año—. Lo que la urgencia exige es un balde lleno, ahora. Y resulta que Francisco tiene un balde a la mano: el árbol entero, vendido como madera, pagado de golpe. El nogal, que era su futuro, es de pronto lo único líquido que le queda. Es la reserva que no pudo tener en ninguna otra forma, porque el dinero le impidió tenerla.',
        'Francisco levanta el hacha. No porque dejó de querer el árbol, sino porque el dinero le quitó toda otra forma de aguantar el presente —y cuando el presente aprieta y no hay colchón, hasta el manantial se vende por un balde—.',
        'Y la cuenta fría, encima, lo empuja en la misma dirección: las quince cosechas le llegarían en un dinero que para entonces no valdrá casi nada, mientras la madera se la pagan hoy, en dinero que todavía vale. Pero esa aritmética es el agravante, no el corazón. El corazón es más simple y más humano: un hombre sin ahorros no elige el futuro, porque no llega a él. Lo alcanza apenas el presente.',
    ]),
    ("La cifra falsificada", [
        '¿Vio lo que hizo Francisco sin saber que lo hacía? Comparó. Puso de un lado las nueces de muchos años, que llegan despacio; del otro, la madera de una vez, que llega hoy. Y para elegir entre las dos tuvo que hacer lo que usted hace cada vez que decide si espera o no: le puso un precio a la espera. Cuánto vale aguantar. Eso —ni más ni menos— es la tasa de interés. No la que anuncia un banco: la de verdad, la que cada uno lleva por dentro y no es otra cosa que la paciencia vuelta número.',
        'Cuando el dinero es honesto, ese número dice la verdad, y la verdad casi siempre premia esperar: el manantial gana. Cuando el dinero se corrompe, el número miente —le susurra a Francisco que el futuro no vale, que tome el balde—. Es la misma mentira que recorrió todo este libro, ahora con un hacha en la mano. Y no le hizo falta engañar a Francisco con palabras: le bastó con tocarle el dinero, porque el dinero es el número con que cuenta.',
        'No hizo falta ningún villano. No hizo falta que a nadie le importara menos la naturaleza. Bastó con corromper el dinero, que es lo mismo que corromper la cuenta, que es lo mismo que acortarle a todo el mundo el horizonte a la vez. Multiplique a Francisco por millones de dueños de bosques, de tierras, de pesquerías, de suelos —cada uno haciendo su cuenta privada y prudente, cada uno descontando un futuro que el dinero volvió incierto— y tiene usted la deforestación de un continente, sin un solo malvado en la escena.',
    ]),
    ("Lo que se ve y lo que no se ve", [
        'Cuando cae el árbol, se ve el árbol caído. Se ve al talador, se ve la madera cargada en el camión, se ve el tocón. Todo lo visible apunta al hombre del hacha, y por eso a él dirigimos la indignación, las campañas, las leyes que prohíben talar.',
        'Lo que no se ve es la cuenta. No se ve la cifra falsificada que volvió racional el hacha. No se ve que Francisco, antes de cortar, hizo la aritmética de cualquier hombre prudente y le salió talar —porque el dinero con que calculaba le había borrado el futuro—. Prohibirle a Francisco que tale, sin tocar el dinero, es pelear con el síntoma: es pedirle que actúe contra su propia cuenta, esperar que la virtud de unos cuantos venza a la aritmética de todos. Algunos resistirán por amor a la tierra. La mayoría hará la cuenta. Siempre, en todas partes, la mayoría hace la cuenta.',
        'Y conviene decir con cuidado lo que este capítulo afirma y lo que no. No digo que el dinero blando sea la única causa de que caigan los bosques. Francisco podía talar también por otras razones —porque no fuera dueño del árbol y otro pudiera robárselo, porque un subsidio premiara la tala, porque la tierra no tuviera dueño y todos corrieran a llevarse lo que pudieran antes que el vecino—. Esas otras causas existen y son reales. Por eso le di a Francisco un árbol que era indiscutiblemente suyo, en su propio terreno, sin subsidio ni vecino que se lo dispute. Le quité todas las demás causas para dejar una sola sobre la mesa. Y aun así, con la propiedad segura y nadie que lo empuje, Francisco levantó el hacha —en cuanto le cambiamos el dinero, y solo por eso—.',
        'Eso es lo que este capítulo quería mostrar. No que el dinero explique todo bosque caído, sino que basta con corromperlo para que hombres buenos, con propiedad segura y sin más presión que la de su propia cuenta, talen lo que aman. El dinero honesto no garantiza que ningún árbol caiga. Pero el dinero falsificado garantiza que caerán los que no debían —porque le miente, a cada dueño de cada manantial, sobre cuánto vale esperar.',
        'El bosque no es la primera víctima del dinero blando ni la última. Es solo la más visible, porque un árbol que cae se ve a kilómetros. Las que vienen —lo que comemos, las guerras que se financian, la paciencia entera de una especie— se ven peor, pero salen de la misma cuenta falseada. Empezamos por el bosque porque es donde la mentira deja una marca que cualquiera puede tocar: un tocón donde había un manantial.',
    ]),
]

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
parts.append('\n  </div>\n\n</article>')
article = ''.join(parts)

# ---- Esqueleto del cap 3 ----
sk = open('tres-regimenes.html', encoding='utf-8').read()
out = sk
out = re.sub(r'<title>.*?</title>',
             '<title>La deforestación — Arregla el dinero, arregla el mundo</title>',
             out, count=1, flags=re.DOTALL)
out = re.sub(r'<article class="page"[^>]*>.*?</article>', lambda _m: article, out, count=1, flags=re.DOTALL)
# nav-foot: prev = bisagra del oro; next vacío (cap 15 aún no existe)
new_nav = ('<nav class="nav-foot">'
           '<a class="prev" href="por-que-no-volver-al-oro.html">¿Y por qué no volver al oro?</a>'
           '<a class="idx" href="index.html">Índice</a>'
           '<span></span></nav>')
out = re.sub(r'<nav class="nav-foot">.*?</nav>', lambda _m: new_nav, out, count=1, flags=re.DOTALL)
# identificadores de audio
out = out.replace('audio/tres-regimenes.mp3', 'audio/deforestacion.mp3')
out = out.replace('audio/tres-regimenes.alignment.json', 'audio/deforestacion.alignment.json')
out = out.replace('data-storage-key="tres-regimenes"', 'data-storage-key="deforestacion"')

open('deforestacion.html', 'w', encoding='utf-8').write(out)
n_par = sum(1 for s, items in CONTENT for it in items if isinstance(it, str) or it[0] == "lead")
n_sec = sum(1 for s, _ in CONTENT if s)
print("deforestacion.html creado")
print(f"párrafos: {n_par} | secciones: {n_sec}")
