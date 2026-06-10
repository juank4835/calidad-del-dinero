#!/usr/bin/env python3
"""Construye el cap 7 «La tasa de interés» (Bloque III, primera pieza).

Reescritura completa del cap 7. Reemplaza el contenido actual de
tasa-de-interes.html con una versión que arranca desde el «pedir
prestado» cotidiano (fiado, tarjeta, cuotas), levanta el concepto
de la tasa como condensación de la paciencia social, distingue
señal honesta de señal falsificada, y cierra con el ciclo austríaco
de auge y depresión.

Estructura:
- Header: eyebrow «Bloque III · La anatomía de la falsificación» +
  h1 «La tasa de interés» + subtítulo «La paciencia de una sociedad,
  vuelta información».
- Prosa corrida sin secciones.
- 1 máxima destacada (blockquote.lema) sobre el precio del tiempo.
- 6 citas en bloque: Hayek (3), Mises (2), Rothbard (1).
- Todas las atribuciones <cite class="no-audio"> — el párrafo previo
  nombra al autor en cada caso.
"""
import re

EYEBROW = "Bloque III · La anatomía de la falsificación"
TITLE = "La tasa de interés"
SUBTITLE = "La paciencia de una sociedad, vuelta información"

CONTENT = [
    ("lead",
     'Alguna vez usted pidió prestado, y se sintió bien. Quizá le fiaron en la tienda de la esquina. "Lléveselo, me paga el viernes". Quizá compró el televisor, la moto o la nevera en cuotas tan pequeñas que parecían no importar. Quizá pasó la tarjeta sintiendo que el problema quedaba para después. Quizá tocó la puerta del que presta en el barrio, el que no pide papeles y entrega el dinero el mismo día. O quizá no fue un gusto sino una urgencia: algo que había que resolver hoy, sin más.'),

    'Las historias cambian. Cambian las personas, los lugares y las razones. Pero casi todas tienen el mismo comienzo: el dinero aparece antes que el esfuerzo necesario para ganarlo. Y eso alivia. Porque recibir es inmediato. El alivio llega hoy; el problema queda para mañana.',

    'Lo difícil viene después. Llega el viernes. Llega la cuota. Llega la factura. Llega el mensaje de cobro. Y entonces aparece una pregunta que estaba escondida desde el principio: ¿cuánto cuesta traer al presente un dinero que todavía no se ha ganado?',

    'Ese costo tiene un nombre que usted ha escuchado toda la vida: la tasa de interés. La escucha en las noticias. "El banco central subió las tasas". "El banco central las bajó". Suena como algo lejano, propio de economistas, banqueros y funcionarios de corbata. Pero es exactamente la misma idea que estaba detrás del fiado, de la tarjeta, del crédito para la moto o del préstamo del barrio. La tasa de interés es el precio del tiempo: lo que alguien exige para entregarle hoy algo que, de otro modo, usted solo tendría mañana.',

    'Y para la mayoría de las personas la historia termina ahí. La tasa simplemente existe. Aparece en la cuota, en el extracto, en el contrato —un número decidido por otros, en algún lugar lejano—. Pero pocos se hacen la pregunta que de verdad importa: ¿quién decide cuánto vale esperar?',

    'Esa es, justamente, la imagen que vamos a desmontar. Porque la tasa como una perilla que alguien ajusta a su criterio es casi lo contrario de lo que la tasa realmente es. Lo que usted ha conocido toda su vida no es la tasa de interés: es una versión intervenida de ella, una señal a la que le torcieron el brazo. Y para ver hasta qué punto le han mostrado una falsificación, primero hay que ver el original —qué sería la tasa de interés si nadie la manipulara, si ningún comité la fijara, si simplemente la dejaran decir la verdad—.',

    'Porque la tasa existía mucho antes de que existieran los bancos centrales. Antes de que hubiera un edificio con funcionarios decidiendo nada, ya había gente que ahorraba y gente que pedía prestado, y entre ellas surgía un número. Ese número —el original, el no manipulado— no es una palanca que alguien mueve. Es un mensajero. Y carga un mensaje que ninguna autoridad podría averiguar por su cuenta.',

    'Imagine que pudiera ver, en un solo dato, cuánta gente en su país está dispuesta a esperar. Cuántos ahorran pensando en diez años y cuántos gastan todo el viernes. Cuánta paciencia hay disponible, en este momento, para emprender cosas que tardan en dar fruto. No existe ninguna encuesta que capture eso —nadie va casa por casa preguntando "¿cuánto está usted dispuesto a esperar?"—. Y sin embargo ese dato existe, se actualiza solo, y está a la vista de todos. Es la tasa de interés: el original, antes de que nadie le pusiera la mano encima.',

    'Esa es su función, y es asombrosa cuando se la entiende: la tasa de interés condensa en un número la preferencia temporal de millones de personas que no se conocen entre sí, que jamás se pusieron de acuerdo, y que ni siquiera saben que están aportando un dato. Cada persona que decide ahorrar en vez de gastar, o pedir prestado en vez de esperar, empuja levemente ese número. El resultado de todos esos empujones es una cifra que le revela a cualquiera que sepa leerla algo que ninguna autoridad podría averiguar por su cuenta: cuánto futuro está dispuesta a financiar esta sociedad, hoy.',

    'Conviene separar dos cosas que esa cifra hace a la vez. La tasa de interés <em>es</em> información —un hecho verdadero sobre cuánta paciencia hay en una sociedad—. Y es, al mismo tiempo, la señal que lleva esa información hasta quienes deciden construir: el empresario que evalúa si levantar una fábrica, la familia que considera una hipoteca, el gobierno que sopesa una obra. El hecho y su transmisión. La distinción importará más adelante: cuando lleguemos a la falsificación, veremos que el fraude corrompe las dos cosas a la vez —ensucia el hecho y engaña al que lo recibe—.',

    'Veámoslo con las personas que ya conocemos. Juan, como recordará, es de los que apartan parte del sueldo; Luisa también ahorra; Carlos vive al día y gasta todo. Y Hernando es aquel que quería montar su taller y necesitaba recursos que no tenía hoy. Pongámoslos a todos en la misma economía.',

    'Fíjese en lo que acaba de aparecer sin que nadie lo organizara. Por un lado, hay ahorro disponible: lo que Juan y Luisa apartaron y no van a usar por ahora. Por otro, hay alguien que quiere construir algo que tarda en dar fruto y necesita esos recursos antes de tiempo: Hernando y su taller. Entre ellos puede haber un trato. Juan y Luisa entregan hoy lo que tienen guardado; Hernando lo usa para sus máquinas y, cuando el taller produzca, devuelve más de lo que recibió. Ese "más" es el interés: lo que Hernando paga por usar antes de tiempo un futuro que todavía no había llegado.',

    'Visto desde los dos lados del trato, ese "más" tiene dos caras. Para Hernando, que pide, es el precio de adelantar —lo que paga por traer al presente un dinero del futuro—. Para Juan y Luisa, que prestan, es la recompensa por esperar —lo que reciben por entregar hoy lo suyo y aguardar—. El mismo número: un costo por un lado, una recompensa por el otro, porque el trato tiene dos extremos y la tasa es donde se tocan.',

    ("lema",
     'La tasa de interés es el precio del tiempo: para el que pide, el precio de adelantar; para el que presta, la recompensa por esperar.'),

    'Esto es preferencia temporal en acción, a escala social. Suponga que mucha gente se vuelve paciente —que no solo Juan y Luisa, sino Carlos y miles más empiezan a ahorrar—. De pronto hay una montaña de ahorro buscando en qué emplearse. Cuando algo abunda, su precio baja: con tanto ahorro disponible, quienes lo prestan compiten por colocarlo, y se conforman con menos a cambio. La tasa de interés baja. Y al revés: si casi nadie ahorra, los pocos ahorros disponibles son disputados, y el interés sube. La tasa de interés no es más que el precio de la paciencia disponible —baja cuando hay mucha, alta cuando hay poca—.',

    'Pero "paciencia" suena a un estado de ánimo, y conviene aterrizarlo, porque debajo de esa palabra hay algo muy físico. Cuando Juan ahorra, no está solo "sintiéndose paciente": está dejando de consumir cosas reales —no se compró el carro, no salió de viaje, no usó esos recursos—. Y al no consumirlos, los libera: el acero, el trabajo, los materiales que habrían ido a su carro quedan disponibles para otra cosa. Eso es lo que de verdad recibe Hernando cuando le prestan el ahorro de Juan: no un fajo de billetes, sino el acceso a recursos reales que alguien dejó libres al no consumirlos. Por eso la tasa baja dice, en el fondo, algo material: "hay recursos liberados, sin usar, disponibles para construir". Y la tasa alta dice lo contrario: "los recursos están ocupados en el consumo de hoy; queda poco libre para comprometer en lo que tarda". La paciencia y los recursos liberados no son dos cosas distintas: son la misma, vista por dentro (la disposición a esperar) y por fuera (los recursos que esa espera deja libres).',

    'Y aquí está lo que su descenso le dice a Hernando, y a todos los que como él quieren construir. Una tasa baja es un mensaje: "hay recursos liberados, hay paciencia de sobra; la sociedad dejó libre lo que hace falta para sostener proyectos largos hasta que maduren; adelante". Una tasa alta dice lo contrario: "los recursos están ocupados, hay poca paciencia; no comprometa en cosas que tardan, porque la gente va a querer esos recursos de vuelta pronto". El empresario no necesita conocer a Juan ni a Luisa ni saber cuánto ahorró cada uno. Le basta con leer la tasa. En ese número está condensada la decisión de todos ellos.',

    'Detengámonos en lo que esto significa, porque es la misma maravilla del primer capítulo, ahora aplicada al precio más importante de todos. Recuerde lo que dijimos del precio del café: que resume, en una cifra, una información que nadie posee entera. La tasa de interés hace exactamente eso, pero con una información todavía más difícil de reunir: cuánta paciencia hay en una sociedad. Juan ahorra para la vejez; Luisa para la educación de un hijo; miles de personas más apartan o gastan por motivos que solo ellas conocen. Nadie podría encuestar ese sentir colectivo —cambia cada día, vive en millones de cabezas, y la mayoría ni sabría explicarlo—. Y sin embargo, la tasa lo recoge.',

    'Fíjese en algo que es fácil pasar por alto: los que ahorran y los que quieren construir casi nunca se encuentran. Juan no conoce a Hernando. No se sientan a negociar. Hayek lo señaló con precisión al estudiar cómo se forma la tasa:',

    ("quote",
     '"Las personas que ahorran dinero y las que quieren utilizarlo en la producción sólo coinciden en casos comparativamente muy raros... La cuestión de quién va a usar los fondos adicionales disponibles para la inversión será decidida en el mercado de préstamos."',
     'Hayek, <em>Precios y producción</em>'),

    'Ese es el prodigio. La paciencia de Juan y la urgencia de Hernando, que jamás se cruzarían, se encuentran traducidas a un número. La tasa es el punto donde la decisión de millones de ahorradores se convierte en una señal que millones de constructores pueden leer, sin que unos y otros se conozcan ni se hablen. Es coordinación sin coordinador —lo mismo que el precio del café, pero ahora sobre el tiempo mismo—.',

    'Y por eso ninguna autoridad puede fijar la tasa "correcta" desde un escritorio: porque la información que la tasa recoge no está en ningún escritorio. Está repartida en millones de decisiones que solo el mercado reúne. Hayek fue tajante en este punto:',

    ("quote",
     '"El tipo de interés, como cualquier otro precio, debería registrar los efectos agregados de miles de circunstancias que afectan a la oferta y demanda de préstamos y que una sola institución no puede conocer."',
     'Hayek, <em>La desnacionalización del dinero</em> (1976)'),

    'Y de aquí se sigue algo grave. Si la tasa es un número que recoge una verdad que nadie posee entera —cuánta paciencia hay en la sociedad, cuántos recursos quedaron libres—, entonces fijarla por decreto no es ajustar un dato: es <em>borrar</em> el único instrumento capaz de leer esa verdad, y reemplazarlo por la corazonada de un comité. Lo que sigue es lo que ocurre cuando alguien hace precisamente eso: cuando se obliga a la tasa a decir lo que no es.',

    'Volvamos a la tasa con la que abrimos: la que usted conoce, la de las noticias y la de su crédito. Quedó pendiente conectarla con la señal de fondo que acabamos de describir —porque no son lo mismo—.',

    'La tasa que usted paga por su tarjeta lleva varias cosas montadas encima. El riesgo de que no pague —por eso a unos les cobran más que a otros—. La ganancia del banco. Sus costos. Póngale números, aunque sean de ejemplo. El banco central fija una referencia: digamos, 5%. Sobre ella, su banco le presta al 12% para una hipoteca —que tiene la casa como garantía— y al 30% en la tarjeta —que no tiene ninguna—.',

    'Esa diferencia, del 5% al 30%, no es un abuso ni el tema de este libro. Es el riesgo, el costo y el margen: las capas comerciales que cada crédito carga según lo que el banco arriesga. Quíteselas todas. Debajo de las tres tasas late una sola cosa: el precio del tiempo —la paciencia de la sociedad, los recursos que de verdad quedaron libres—. Esa es la señal de fondo. Las capas de encima cambian de un crédito a otro; la señal de fondo es la misma para todos, porque es el suelo sobre el que se paran todas las tasas.',

    'Falta la mecánica que conecta esa señal de fondo con su cuota mensual. Dijimos en la apertura que el banco central no crea la tasa, la empuja. Así es como el empujón lo alcanza: el banco central fija una tasa de referencia, y como los bancos comerciales se montan sobre esa referencia para prestarle a usted, el empujón baja —escalón por escalón— hasta la cuota de su tarjeta. De arriba hacia abajo: el banco central empuja, el banco comercial traslada, usted paga. Por eso usted sí siente el empujón, aunque venga de muy arriba —y por eso creyó, toda la vida, que la tasa <em>era</em> esa palanca de arriba, cuando en realidad la palanca solo estaba deformando una señal que nacía mucho más abajo, entre la gente que ahorra y la que construye—.',

    'De modo que hay dos tasas que conviene no confundir. Está la tasa que <em>diría la verdad</em> —la que reflejaría la paciencia real de la sociedad, el ahorro que de verdad existe—. Y está la tasa que <em>efectivamente rige</em> —la que resulta después de que el banco central la empujó—. Mientras las dos coinciden, la señal es honesta. El problema empieza cuando el banco central separa la segunda de la primera: cuando empuja la tasa que rige por debajo de la que diría la verdad. Hayek lo describió con precisión:',

    ("quote",
     '"Si los bancos reducen el tipo monetario por debajo del de equilibrio, lo que pueden hacer si prestan más de lo que les ha sido confiado, es decir, si aumentan la circulación, esto debe tender a elevar los precios."',
     'Hayek, <em>Precios y producción</em>'),

    'Vale la pena traducir esa frase. "El tipo de equilibrio" es la tasa que diría la verdad: la que corresponde al ahorro que de verdad hay. Y el banco central puede empujar la tasa que rige por debajo de ella "prestando más de lo que le ha sido confiado" —es decir, prestando un ahorro que nadie hizo, dinero creado de la nada, el mismo truco del capítulo 3—. Aquí las dos mitades del libro se encuentran: el dinero que se fabrica de la nada entra en la economía <em>bajando la tasa</em>. Esa es la forma concreta en que la falsificación del dinero se convierte en falsificación de la señal más importante.',

    'Y ahora la pregunta que importa: ¿qué le pasa a Hernando? Porque Hernando no sabe nada de esto. Él solo lee la tasa, como siempre. La ve baja y entiende lo que una tasa baja siempre quiso decir: "hay recursos liberados, hay ahorro disponible, adelante con el proyecto largo". Confía en la señal, como debe. Pide el préstamo, compra las máquinas, levanta el taller —convencido de que detrás de esa tasa baja hay un Juan y una Luisa que dejaron de consumir para liberar los recursos que su taller necesitará—. Pero no los hay. La tasa bajó sin que nadie ahorrara. Y aquí está lo crucial: lo que falta no es un estado de ánimo, no es "paciencia" en abstracto. Lo que falta es físico —el acero, los materiales, el trabajo que solo habrían quedado libres si alguien de verdad hubiera dejado de consumirlos—. El dinero que Hernando recibió salió de una imprenta, y un billete nuevo no libera ningún recurso: solo le da a Hernando el derecho de pujar por unos recursos que ya están ocupados. Hernando construye sobre un material que creía disponible y que no existe.',

    'Mises lo explicó con una precisión que no ha sido superada: el interés rebajado por decreto no informa, engaña al que calcula.',

    ("quote",
     '"La baja del interés viene a falsear el cálculo empresarial... Los cálculos hacen que parezcan rentables y practicables negocios que no lo serían si el tipo de interés no se hubiera rebajado artificialmente mediante la expansión crediticia."',
     'Mises, <em>La acción humana</em>, cap. XX'),

    'Hernando no fue imprudente ni ingenuo. Hizo exactamente lo que debe hacer un buen empresario: leyó la señal y actuó en consecuencia. El problema es que la señal mentía. Y cuando la herramienta con la que uno calcula está adulterada, el error no es del que calcula —es de quien adulteró la herramienta—.',

    'Multiplique a Hernando por miles. Miles de empresarios, leyendo la misma señal falsa, emprenden a la vez proyectos largos que la sociedad no tiene cómo sostener —porque el ahorro real que haría falta para terminarlos no está—. Durante un tiempo, todo parece ir de maravilla: hay obras por todas partes, empleo, optimismo, auge. La mentira todavía no se ha cobrado. Pero el momento llega, y tiene un nombre.',

    'El auge no es la salud: es el síntoma. Mientras dura, la economía está construyendo cosas que no se pueden terminar, comprometiendo recursos que no alcanzan, alargando procesos que el ahorro real no puede cubrir. El error ya se cometió —se cometió cuando la tasa falsa dijo "hay con qué" y no lo había—. Lo que viene después no es el error: es el <em>descubrimiento</em> del error. Llega el día en que los proyectos largos necesitan los recursos reales para completarse, y esos recursos no aparecen, porque nunca existieron. Las obras se detienen. Los proyectos se revelan inviables. Las empresas que invirtieron sobre la señal falsa quiebran. A eso lo llamamos crisis, recesión, depresión —y lo vivimos como una catástrofe que cae sobre una economía sana—.',

    'Pero aquí está la inversión que conviene entender, y es contraria a todo lo que se suele decir. La depresión no es la enfermedad. Es la cura. Es el momento en que la economía, por fin, deja de fingir: liquida lo que no debió construirse, libera los recursos atrapados en proyectos imposibles, y vuelve a alinear lo que se produce con lo que de verdad hay. Rothbard lo dijo sin rodeos:',

    ("quote",
     '"La fase de depresión es en realidad la fase de recuperación... las fases de crisis y depresión constituyen el necesario período de reajuste, el momento en que se liquidan las malas inversiones."',
     'Rothbard, <em>El hombre, la economía y el Estado</em>, cap. 12'),

    'Léalo otra vez, porque es contraintuitivo y central: lo doloroso —las quiebras, el desempleo, las obras paradas— no es el mal. Es el cuerpo expulsando el veneno. El mal fue el auge, cuando la señal falsa indujo a miles a construir sobre nada. La depresión es solo la factura de esa mentira, llegando por fin a cobrarse. Y por eso los intentos de "estimular" la economía para salir de la depresión —bajando otra vez la tasa, inyectando más dinero— no curan: posponen. Vuelven a falsificar la señal para que la factura no llegue todavía, y al hacerlo siembran la próxima crisis, más grande. Se puede aplazar el ajuste, pero cada aplazamiento lo agranda.',

    'Mises fue tajante sobre por qué este final es inevitable, y no un accidente que mejor política podría evitar. El auge no descansa sobre nada real:',

    ("quote",
     '"El auge de la expansión crediticia se apoya en las arenas movedizas del papel moneda y el dinero bancario; por eso, al final, se viene abajo."',
     'Mises, <em>La acción humana</em>, cap. XX'),

    'Y advirtió contra la tentación de prolongarlo: si los bancos, asustados por la crisis que asoma, inyectan otra dosis de crédito para sostener el auge, solo aplazan el ajuste y lo agravan. Llevado al extremo, ese camino no evita el derrumbe —lo convierte en algo peor, la destrucción de la moneda misma—. No hay forma de hacer permanente un auge construido sobre una mentira. Solo se puede elegir entre detenerlo ahora, o detenerlo más tarde habiendo hecho el daño mayor.',

    'Y aquí se cierra el círculo que abrimos al principio del capítulo. Dijimos que la tasa de interés es información —la paciencia de millones, condensada en un número— y que esa información puede falsificarse. Ahora vemos el precio de falsificarla. No es un precio abstracto: son fábricas a medio construir, ahorros de toda una vida evaporados, gente que quedó sin empleo porque trabajaba en un proyecto que nunca debió empezar. Todo porque una señal dijo lo que no era, y millones de personas honestas —Hernando entre ellas— le creyeron. La tasa falsa no engaña con palabras. Engaña con cifras, y las cifras se obedecen sin sospechar.',

    'De todas las distorsiones que produce el dinero deshonesto, esta es la más profunda, porque no tuerce <em>qué</em> compramos hoy, sino <em>qué construimos para mañana</em>. Cuando el banco central empuja la tasa, miente sobre las dos caras de una misma moneda: dice que la sociedad está dispuesta a esperar cuando no lo está, y dice que hay recursos reales liberados cuando siguen ocupados. Una sola cifra, dos mentiras enlazadas —porque la paciencia y los recursos liberados nunca van por separado—. Falsificar la tasa es falsificar el futuro: empujar a una sociedad entera a edificar lo que no podrá habitar, con un material que creyó libre y no estaba. En el próximo capítulo veremos en detalle esa distorsión —cómo el capital se dirige a los lugares equivocados, y qué forma toma el daño cuando la mentira se reparte por toda la estructura productiva—.',
]

# CSS local del lema (vive en el <style> de cada cap que lo use)
EXTRA_CSS = """
/* ===== Máxima del autor ===== */
blockquote.lema {
  margin: 2.8rem 0; padding: 1.4rem 1rem;
  border-left: none;
  border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule);
  text-align: center; font-style: italic;
  font-size: 1.18rem; line-height: 1.5; color: var(--ink);
}
"""


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
        elif it[0] == "lema":
            parts.append(f'    <blockquote class="lema">{it[1]}</blockquote>\n')
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
                 '<title>La tasa de interés — Arregla el dinero, arregla el mundo</title>',
                 out, count=1, flags=re.DOTALL)
    out = re.sub(r'<article class="page"[^>]*>.*?</article>',
                 lambda _m: article, out, count=1, flags=re.DOTALL)
    new_nav = ('<nav class="nav-foot">'
               '<a class="prev" href="ahorro-real.html">Lo que la espera libera</a>'
               '<a class="idx" href="index.html">Índice</a>'
               '<a class="next" href="asignacion-intertemporal.html">La asignación intertemporal</a></nav>')
    out = re.sub(r'<nav class="nav-foot">.*?</nav>',
                 lambda _m: new_nav, out, count=1, flags=re.DOTALL)
    out = out.replace('</style>', EXTRA_CSS + '</style>', 1)
    out = out.replace('audio/tres-regimenes.mp3', 'audio/tasa-de-interes.mp3')
    out = out.replace('audio/tres-regimenes.alignment.json',
                      'audio/tasa-de-interes.alignment.json')
    out = out.replace('data-storage-key="tres-regimenes"',
                      'data-storage-key="tasa-de-interes"')

    open('tasa-de-interes.html', 'w', encoding='utf-8').write(out)
    n_par = sum(1 for it in CONTENT if isinstance(it, str) or (isinstance(it, tuple) and it[0] == "lead"))
    n_q = sum(1 for it in CONTENT if isinstance(it, tuple) and it[0] == "quote")
    n_l = sum(1 for it in CONTENT if isinstance(it, tuple) and it[0] == "lema")
    print(f"tasa-de-interes.html regenerado: {n_par} párrafos, {n_l} lema, {n_q} citas")


if __name__ == "__main__":
    main()
