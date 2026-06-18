#!/usr/bin/env python3
"""Construye el cap 16 «Comerse la semilla» (Bloque IV, segunda consecuencia).

Estructura: prosa corrida, sin secciones, sin citas en bloque.
El ajá está en el párrafo «No hizo falta ningún villano…» — el momento
en que el capítulo nombra explícitamente su tesis política: no hace
falta corromper a la gente, basta con corromper su dinero.
"""
import re

EYEBROW = "Segunda consecuencia · lo más visible"
TITLE = "Comerse la semilla"
SUBTITLE = "Por qué un hombre que ama su bosque termina talándolo —y no por maldad"

CONTENT = [
    ("lead",
     'Hay una imagen que todos llevamos puesta sin pensarla: la deforestación es obra de gente avara. Empresas que ven un bosque y ven dinero, taladores que arrasan por codicia, gobiernos que venden la selva al mejor postor. Donde hay un árbol caído, buscamos un culpable —alguien a quien le importó poco la naturaleza y mucho la ganancia—. Esa imagen es cómoda porque reparte el mundo en buenos y malos, y nos deja a nosotros del lado bueno. Y como casi todas las imágenes cómodas, esconde lo que de verdad importa.'),

    'Porque la mayor parte de los bosques del mundo no los talan villanos. Los talan personas que harían exactamente lo mismo que usted haría en su lugar, haciendo exactamente la cuenta que usted haría. Para ver eso hay que dejar de mirar al talador y empezar a mirar la cuenta que tiene delante. Y esa cuenta, como todo en este libro, está escrita en dinero.',

    'Imagine a un hombre del mismo pueblo donde Juan apartaba su sueldo —llamémoslo Francisco— con un nogal en el fondo de su terreno. Lo plantó su padre, y desde hace años el árbol le da cada otoño una cosecha de nueces que Francisco vende en la plaza. No es una fortuna, pero es un ingreso fiel: llega todos los años, sin falta, como llegan los otoños.',

    'Un día se aparece un comprador de madera. El nogal es viejo y la madera es buena; el hombre le ofrece, por el árbol entero, lo que Francisco sacaría de unas quince cosechas de nueces. Una suma considerable, de golpe, hoy.',

    'Francisco hace la cuenta. Y aquí conviene mirar por encima de su hombro, porque la cuenta que hace es exactamente la que usted haría. Tiene dos opciones. Una: quedarse el árbol y seguir cobrando nueces cada otoño, año tras año, como hasta ahora —y dejárselo a sus hijos, que seguirán cobrando cuando él ya no esté—. Otra: cortarlo, cobrar de una vez el equivalente a quince cosechas, y quedarse sin árbol para siempre.',

    'Si Francisco confía en el futuro —si cree que habrá otoños, que sus nueces seguirán valiendo, que sus hijos heredarán un árbol vivo y no un tocón— la cuenta es fácil: no vende. Quince cosechas cobradas de a poco, más todas las que vendrán después, más la herencia, valen muchísimo más que la madera de una sola vez. El árbol vivo es un manantial; la madera, un balde. Nadie cambia un manantial por un balde si confía en que el manantial seguirá manando.',

    'Fíjese bien en lo que sostiene esa decisión. No es el amor de Francisco por los árboles, aunque lo tenga. No es conciencia ecológica, ni virtud, ni una ley que lo obligue. Es una cuenta —y una cuenta que sale a favor de conservar solo si Francisco puede confiar en que el futuro llegará y se parecerá al presente—. La conservación del bosque, aquí, no es un acto moral. Es el resultado frío de un cálculo que premia la espera. Francisco guarda el árbol por la misma razón por la que Juan, allá en el capítulo cinco, guardaba parte de su sueldo: porque el futuro le parece lo bastante firme como para que valga la pena esperarlo.',

    'Ahora no le toque nada a Francisco. Déjele su amor por el árbol, su inteligencia, su prudencia, su cariño por los hijos que lo heredarán. No lo vuelva avaro ni tonto. Cámbiele una sola cosa, y la más invisible de todas: el dinero con que cobra las nueces.',

    'Hasta ahora cobraba en dinero honesto, del que no se puede fabricar de la nada. Cada peso que apartaba seguía valiendo el año siguiente, y el siguiente —así que, sin pensarlo, Francisco tenía un colchón—. Lo que le sobraba de las cosechas buenas lo guardaba para las malas; tenía con qué aguantar una enfermedad, un techo que se cae, un año flaco. Y porque tenía con qué aguantar, podía esperar. El nogal le daba de a poco, año tras año, y a él le bastaba con eso, porque tenía un respaldo debajo.',

    'Cámbiele ese dinero por uno que se diluye cada año. Y mire lo primero que desaparece: el colchón. Ahora lo que Francisco aparta se le derrite en las manos —guardar es perder—, así que deja de guardar. No por imprudente: porque ahorrar dejó de servir de nada. Lo vio usted entero en el capítulo del ahorro real: con dinero que no preserva valor, el ahorro ya no guarda pedazos del mundo para después; no guarda nada. Y un hombre que no puede ahorrar es un hombre que no puede esperar —porque esperar quince años de cosechas exige tener con qué vivir mientras llegan, y eso es precisamente lo que ya no tiene—.',

    'Aquí es donde la sensación se vuelve física, y conviene que la sienta usted también. Francisco tiene un nogal que es un manantial, sí: le dará nueces durante quince otoños. Pero hoy le llegó la cuenta del médico, o se le cayó media casa, o simplemente no alcanzó el mes. Y no hay colchón debajo, porque el dinero se lo comió. El manantial no sirve para hoy —el manantial da de a gotas, año tras año—. Lo que la urgencia exige es un balde lleno, ahora. Y resulta que Francisco tiene un balde a la mano: el árbol entero, vendido como madera, pagado de golpe. El nogal, que era su futuro, es de pronto lo único líquido que le queda. Es la reserva que no pudo tener en ninguna otra forma, porque el dinero le impidió tenerla.',

    'Francisco levanta el hacha. No porque dejó de querer el árbol, sino porque el dinero le quitó toda otra forma de aguantar el presente —y cuando el presente aprieta y no hay colchón, hasta el manantial se vende por un balde—.',

    'Y la cuenta fría, encima, lo empuja en la misma dirección: las quince cosechas le llegarían en un dinero que para entonces no valdrá casi nada, mientras la madera se la pagan hoy, en dinero que todavía vale. Pero esa aritmética es el agravante, no el corazón. El corazón es más simple y más humano: un hombre sin ahorros no elige el futuro, porque no llega a él. Lo alcanza apenas el presente.',

    '¿Vio lo que hizo Francisco sin saber que lo hacía? Comparó. Puso de un lado las nueces de muchos años, que llegan despacio; del otro, la madera de una vez, que llega hoy. Y para elegir entre las dos tuvo que hacer lo que usted hace cada vez que decide si espera o no: le puso un precio a la espera. Cuánto vale aguantar. Eso —ni más ni menos— es la tasa de interés. No la que anuncia un banco: la de verdad, la que cada uno lleva por dentro y no es otra cosa que la paciencia vuelta número.',

    'Cuando el dinero es honesto, ese número dice la verdad, y la verdad casi siempre premia esperar: el manantial gana. Cuando el dinero se corrompe, el número miente —le susurra a Francisco que el futuro no vale, que tome el balde—. Es la misma mentira que recorrió todo este libro, ahora con un hacha en la mano. Y no le hizo falta engañar a Francisco con palabras: le bastó con tocarle el dinero, porque el dinero es el número con que cuenta.',

    ("aja",
     'No hizo falta ningún villano. No hizo falta que a nadie le importara menos la naturaleza. Bastó con corromper el dinero, que es lo mismo que corromper la cuenta, que es lo mismo que acortarle a todo el mundo el horizonte a la vez. Multiplique a Francisco por millones de dueños de bosques, de tierras, de pesquerías, de suelos —cada uno haciendo su cuenta privada y prudente, cada uno descontando un futuro que el dinero volvió incierto— y tiene usted la deforestación de un continente, sin un solo malvado en la escena.'),

    'Cuando cae el árbol, se ve el árbol caído. Se ve al talador, se ve la madera cargada en el camión, se ve el tocón. Todo lo visible apunta al hombre del hacha, y por eso a él dirigimos la indignación, las campañas, las leyes que prohíben talar.',

    'Lo que no se ve es la cuenta. No se ve la cifra falsificada que volvió racional el hacha. No se ve que Francisco, antes de cortar, hizo la aritmética de cualquier hombre prudente y le salió talar —porque el dinero con que calculaba le había borrado el futuro—. Prohibirle a Francisco que tale, sin tocar el dinero, es pelear con el síntoma: es pedirle que actúe contra su propia cuenta, esperar que la virtud de unos cuantos venza a la aritmética de todos. Algunos resistirán por amor a la tierra. La mayoría hará la cuenta. Siempre, en todas partes, la mayoría hace la cuenta.',

    'Y no crea que el hacha de Francisco cae solo sobre los árboles. La misma cuenta, el mismo dinero que le susurró "tome el balde", está sonando en el oído de cualquiera que tenga, en vez de un nogal, un pedazo de mundo que mana despacio.',

    'Vaya al campo de al lado. Su dueño tiene tierra —tierra que su padre le dejó viva, que da cosecha tras cosecha si se la cuida: si se la deja descansar, si se alternan las siembras, si el ganado vuelve a pisarla y abonarla—. Una tierra cuidada es, igual que el nogal, un manantial: da de a poco, todos los años, para siempre. Pero exige lo mismo que exigía el árbol —paciencia, la disposición a no exprimirla hoy para que rinda mañana—. Y al dueño le pasó lo mismo que a Francisco: el dinero en que cobra sus cosechas dejó de guardar valor, su colchón se derritió, y la espera se le volvió un lujo que ya no puede pagar.',

    'Así que hace con su tierra lo que Francisco hizo con su árbol: la trata como un balde. Le exige tres cosechas donde debería sacar una, no la deja descansar, le quita el ganado que rendía lento. Y cuando la tierra, agotada, empieza a dar menos, no la deja sanar: le echa fertilizante comprado para forzarla a seguir pariendo sobre un suelo que por dentro ya está muerto. El campo sigue verde por fuera. Por dentro es el mismo balde casi vacío del que hablábamos —solo que ahora se le echa agua de afuera para que parezca lleno—.',

    'Es la misma escena, con otro disfraz. Donde Francisco tenía un manantial de nueces, este dueño tiene un manantial de tierra fértil; donde Francisco lo cambió por la madera de una vez, este lo cambia por las cosechas forzadas de unos pocos años. Los dos liquidaron, por la misma cuenta torcida, lo que debía durar generaciones. No hizo falta volverlos malos. Bastó con tocarles el dinero.',

    'Y aquí el daño da un paso más, hasta un lugar donde usted lo toca sin saberlo: su propia mesa. Porque esa tierra forzada a parir sobre un suelo muerto no deja de producir —produce, mientras le echen fertilizante—. Pero produce distinto. La planta crece rápida, grande, abundante; solo que crece sobre una tierra que ya casi no tiene nada que pasarle. Sale comida con la forma de siempre y, por dentro, cada vez menos de lo que hacía que esa comida alimentara. Abundante por fuera, vacía por dentro —igual que el suelo del que vino, igual que el dinero con que se cobró—.',

    'Repare en lo que se repite, peldaño por peldaño: el dinero que abulta el número y vacía el valor; el suelo que abulta la cosecha y vacía la sustancia; la mesa que abulta la abundancia y vacía el alimento. Es la misma figura, bajando de la moneda al campo y del campo al plato. No es que el dinero blando le enferme la comida por una cadena oscura de causas —no le pido que crea eso—. Es algo más simple de ver: la misma cuenta que empujó a liquidar el manantial empuja a vaciar el suelo, y un suelo vaciado da, sin misterio, una cosecha más pobre de lo que daría uno cuidado. Su mesa de esta noche puede tener más que nunca y sostener menos que nunca, y la raíz de esa paradoja no está en su cocina: está en una cuenta torcida, muchos pasos atrás, que nadie le mostró.',

    'Detengámonos a ver lo que tienen en común el árbol, la tierra y el plato, porque es una sola cosa. En los tres, alguien tenía un manantial —algo que daba de a poco y para siempre, mientras se lo cuidara— y lo cambió por un balde: todo de una vez, y después nada. Francisco con su nogal, el vecino con su campo, y al final del camino su mesa, más llena y menos nutrida que la de sus abuelos. Ninguno fue avaro. Ninguno dejó de amar lo que liquidó. A cada uno, el mismo dinero le hizo la misma cuenta, y la cuenta dijo siempre lo mismo: el futuro no compensa, tome lo de hoy. Liquidar el manantial no fue su pecado; fue su aritmética.',

    'Y conviene decir con cuidado lo que este capítulo afirma y lo que no. No digo que el dinero blando sea la única causa de que caigan los bosques o se agoten los suelos. Hay otras, y son reales —la tierra sin dueño que todos corren a saquear, el subsidio que premia la tala, el vecino que se lleva lo que uno no cobre primero—. Por eso le di a Francisco un árbol que era suyo sin disputa, en su terreno, sin subsidio ni rival. Le quité todas las demás causas para dejar una sola sobre la mesa. Y aun así, con la propiedad asegurada y nadie que lo empujara, levantó el hacha —en cuanto le tocamos el dinero, y solo por eso—. Eso es lo que el capítulo quería mostrar: no que el dinero explique cada manantial vaciado, sino que basta con corromperlo para que hombres buenos liquiden lo que aman.',

    'Pero fíjese en algo que estos tres casos comparten, y que es la frontera de lo que hemos visto hasta aquí: en todos, el que liquida el manantial es su dueño, y el que paga el precio es él mismo —o, a lo sumo, sus hijos—. Francisco se queda sin árbol; el vecino, sin tierra; usted, con una mesa más pobre. Es un daño que cada uno se hace a sí mismo, engañado por una cuenta torcida. Por terrible que sea, hay en él una especie de justicia triste: quien levanta el hacha es quien pierde el bosque.',

    'Lo que viene rompe esa frontera. Porque hay un daño mayor, donde el que decide y el que paga ya no son la misma persona —donde alguien hace la cuenta y otro, que nunca la vio, carga con el balde vacío—. Hasta aquí el dinero falso le mintió a cada uno sobre lo suyo. Ahora vamos a ver qué pasa cuando le permite a unos pocos disponer del trabajo de todos. El manantial que se liquida ya no será de quien empuña el hacha. Será el suyo, y nadie le habrá preguntado.',
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
        elif it[0] == "aja":
            parts.append(f'    <p class="aja">{it[1]}</p>\n')
    parts.append('\n  </div>\n\n</article>')
    article = ''.join(parts)

    sk = open('tres-regimenes.html', encoding='utf-8').read()
    out = sk
    out = re.sub(r'<title>.*?</title>',
                 '<title>Comerse la semilla — Arregla el dinero, arregla el mundo</title>',
                 out, count=1, flags=re.DOTALL)
    out = re.sub(r'<article class="page"[^>]*>.*?</article>',
                 lambda _m: article, out, count=1, flags=re.DOTALL)
    new_nav = ('<nav class="nav-foot">'
               '<a class="prev" href="el-horizonte-se-acorta.html">El horizonte se acorta</a>'
               '<a class="idx" href="index.html">Índice</a>'
               '<span></span></nav>')
    out = re.sub(r'<nav class="nav-foot">.*?</nav>',
                 lambda _m: new_nav, out, count=1, flags=re.DOTALL)
    out = out.replace('audio/tres-regimenes.mp3', 'audio/comerse-la-semilla.mp3')
    out = out.replace('audio/tres-regimenes.alignment.json',
                      'audio/comerse-la-semilla.alignment.json')
    out = out.replace('data-storage-key="tres-regimenes"',
                      'data-storage-key="comerse-la-semilla"')

    open('comerse-la-semilla.html', 'w', encoding='utf-8').write(out)
    n_par = sum(1 for it in CONTENT if isinstance(it, str) or (isinstance(it, tuple) and it[0] == "lead"))
    n_aja = sum(1 for it in CONTENT if isinstance(it, tuple) and it[0] == "aja")
    print(f"comerse-la-semilla.html regenerado: {n_par} párrafos, {n_aja} ajá")


if __name__ == "__main__":
    main()
