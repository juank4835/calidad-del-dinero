#!/usr/bin/env python3
"""Construye el cap 9 «El dolor que avisa» (Bloque III, tercera pieza).

Reescritura completa. Título nuevo humano «El dolor que avisa» —
título técnico «La detección de la mala inversión» queda revelable
al hover en el índice.

El slug del archivo NO cambia: sigue siendo deteccion-mala-inversion.html
para preservar URLs y nav-foots.

Hilo central del cap:
- Cómo una sociedad descubre que se equivocó (el hambre en la aldea
  / las pérdidas y ganancias en la economía real).
- Las pérdidas no son solo daño: son INFORMACIÓN. Sin pérdidas, nadie
  sabría que se equivocó.
- La doble falsificación del dinero deshonesto en este capítulo:
  primero CREÓ el error (cap 7-8); ahora IMPIDE que se descubra,
  anestesiando la señal con rescates.
- Imagen del narcótico: el rescate como droga que pospone el dolor.

Estructura:
- Header: eyebrow «Tercera pieza · gravedad alta» + h1 «El dolor que
  avisa» + subtítulo «Cómo una sociedad descubre que se equivocó —y
  cómo se la puede cegar—».
- Prosa corrida sin secciones.
- 4 citas en bloque: Mises (2) + Rothbard (2).
- Todas las atribuciones con cite class='no-audio'.
"""
import re

EYEBROW = "Tercera pieza · gravedad alta"
TITLE = "El dolor que avisa"
SUBTITLE = "Cómo una sociedad descubre que se equivocó —y cómo se la puede cegar—"

CONTENT = [
    ("lead",
     'Dejamos a la aldea en mitad de un error. Había bajado la tasa sin que nadie ahorrara, los pescadores habían abandonado el mar para levantar un astillero, y nosotros —que mirábamos desde afuera— sabíamos que ese astillero no se podía terminar, porque no había pescado guardado para alimentar a quienes lo construían. Pero los pescadores no lo sabían. Seguían trabajando, convencidos de que iban por buen camino. Y aquí aparece la pregunta que dejamos abierta: ¿cómo se enteran <em>ellos</em>? ¿Qué les avisa que se equivocaron?'),

    'La respuesta es brutal en su sencillez: el hambre. Llega el día en que las reservas se agotan, no hay pescado que repartir, y el estómago vacío anuncia lo que ningún discurso habría hecho creer —que el astillero fue un error, que se dejó de pescar de más, que la aldea construyó algo que no podía sostener—. El hambre no opina ni discute: informa. Es el mensajero que trae, por fin, la verdad que la tasa falsa había ocultado.',

    'Fíjese en lo que el hambre <em>es</em>, en el fondo: una pérdida. La aldea invirtió esfuerzo —semanas de trabajo, redes sin tejer, pescado sin sacar— en algo que no rindió. El hambre es la forma en que esa pérdida se hace sentir, imposible de ignorar. Y esa es la idea de este capítulo: que las pérdidas no son solo un daño. Son información —la más valiosa que una economía produce—, porque son la única forma que tiene una sociedad de descubrir que se equivocó y corregir el rumbo.',

    'En el capítulo anterior vimos cómo nace una mala inversión: una señal falsa engaña a quien construye. Pero una mala inversión que nadie detecta se vuelve eterna —se sigue alimentando, se sigue agrandando, consumiendo recursos que harían falta en otra parte—. Tiene que haber un mecanismo que la descubra y la detenga. Ese mecanismo existe, y es tan importante como la señal que lo desató. Este capítulo trata de él: de cómo una sociedad se entera de sus errores. Y de cómo el dinero deshonesto puede, también aquí, romper el aviso.',

    'Salgamos un momento de la aldea para verlo en la economía que usted conoce, la de empresas y dinero. Cuando alguien monta un negocio, está haciendo una apuesta sobre el futuro: cree que lo que produce valdrá, para los demás, más que los recursos que gasta en producirlo. Si acierta, gana. Si se equivoca —si gasta en cuero, mano de obra y máquinas para fabricar algo que nadie quiere lo suficiente—, pierde. Y esa pérdida no es un accidente molesto: es el sistema avisándole que esos recursos estaban mal empleados, que el cuero y el trabajo que consumió habrían servido más en otra parte. Mises lo expresó con una claridad que no ha sido superada:',

    ("quote",
     '"Las pérdidas y las ganancias son los resortes gracias a los cuales el imperio de los consumidores gobierna el mercado... es esa conducta la que hace que la propiedad de los medios de producción pase de las personas menos eficientes a las más eficientes."',
     'Mises, <em>La acción humana</em>, cap. XV'),

    'Lea eso despacio, porque dice algo más profundo de lo que parece. Las pérdidas y ganancias no solo premian o castigan: <em>mueven los recursos</em>. El que acierta gana, y con la ganancia consigue más medios para seguir produciendo lo que la gente quiere. El que se equivoca pierde, y la pérdida le va quitando los recursos que estaba malgastando, para que pasen a manos de quien sabrá usarlos mejor. Es un mecanismo de corrección que funciona solo, sin que nadie lo dirija —la economía aprendiendo de sus errores, caso por caso—. Y Mises remató la idea con una frase que es, exactamente, el corazón de este capítulo:',

    ("quote",
     '"Si no hubiera ni pérdidas ni ganancias, los empresarios ignorarían las más urgentes necesidades de los consumidores."',
     'Mises, <em>La acción humana</em>, cap. XV'),

    ("aja",
     'Sin pérdidas, nadie sabría que se equivocó. Esa es la función de la pérdida: es el hambre de la aldea, traducida al lenguaje del dinero. Le dice a quien invirtió mal —y a toda la sociedad que observa— "esto no servía, deténgase, mueva los recursos a otra parte". Una economía sin pérdidas sería como un cuerpo que no siente dolor: seguiría apoyándose en el hueso roto hasta destruirse, porque nada le avisaría del daño. El dolor es desagradable, pero es información que salva. La pérdida también.'),

    'Y aquí llega la falsificación propia de este capítulo —distinta de la que ya vimos, y en cierto modo más perversa—. Porque hasta ahora el dinero deshonesto <em>creaba</em> el error, falsificando la tasa. Lo que hace ahora es algo peor: esconder el error una vez cometido, silenciando la señal que lo delataría.',

    'Volvamos a la aldea para verlo. La mala inversión ya está hecha: el astillero a medio construir, las reservas agotándose, el hambre asomando. El hambre está a punto de cumplir su función —avisar que hay que parar, abandonar el astillero, volver a pescar—. Pero imagine que, justo entonces, alguien aparece y, para que nadie sienta el hambre, reparte las últimas reservas de la aldea: el pescado que quedaba apartado para tejer las redes, para los viejos, para el invierno. No trajo comida nueva —no la hay—; solo desvió hacia el astillero lo poco que quedaba para todo lo demás. La aldea, aliviada, sigue construyendo. El aviso se silenció. Y el error, en lugar de corregirse, se agranda: ahora se hunden todavía más semanas, más trabajo, más recursos en algo que sigue sin poder terminarse. Cuando esas últimas reservas se acaben —y se acabarán, porque nadie está pescando—, el hambre volverá, pero peor: la aldea ya no tendrá ni el astillero, ni las redes, ni el pescado del invierno, y estará aún más lejos del mar.',

    'Eso es exactamente lo que el dinero deshonesto hace en la economía real. Cuando las malas inversiones del auge empiezan a revelarse —las empresas que no son rentables, los proyectos que no se sostienen—, las pérdidas deberían hacer su trabajo: quebrar lo inviable, liberar los recursos atrapados, corregir el rumbo. Ese ajuste doloroso es lo que llamamos crisis, recesión, depresión —tres nombres para el mismo momento: el de la verdad llegando a cobrarse—. Pero el banco central puede impedirlo, inyectando más crédito barato: rescata a los bancos que prestaron mal, sostiene con dinero nuevo a las empresas que deberían cerrar, mantiene vivo lo que el mercado quería liquidar. La pérdida que iba a informar se tapa. El error que iba a corregirse se prolonga. Rothbard fue tajante sobre lo que esto significa:',

    ("quote",
     '"Toda interferencia gubernamental en el proceso de depresión solamente lo prolonga... toda detención o desaceleración impide que el reajuste ocurra."',
     'Rothbard, <em>El hombre, la economía y el Estado</em>, cap. 12'),

    'Y fíjese en lo que hace posible esa anestesia, porque es la raíz de todo: el rescate se paga con dinero que se crea de la nada —y el dinero creado, ya lo sabe, no fabrica recursos: solo desvía hacia lo inviable lo poco que quedaba para lo demás, igual que las últimas reservas de la aldea—. Ahí está, otra vez, la línea que parte todo el libro. Con dinero duro —ese que nadie puede fabricar por decreto— no habría con qué financiar el rescate perpetuo: cuando una empresa quiebra, quiebra, porque no existe una fábrica de dinero que la sostenga indefinidamente. La señal de la pérdida suena y se obedece, porque nadie puede pagar para silenciarla. Solo cuando el dinero se puede crear de la nada aparece la posibilidad de tapar la pérdida con dinero nuevo —de comprarle silencio al mensajero—. La quiebra que sanea y el rescate que enferma no son dos políticas entre las que una sociedad elige libremente: la segunda solo está disponible si el dinero es de los que se imprimen. El dinero honesto no es que prefiera dejar caer a las empresas; es que no le da a nadie el poder de impedirlo a costa de todos.',

    'Lo que para casi todos es "ayuda" —rescatar, estimular, evitar las quiebras— es, visto de cerca, lo contrario: la mano que tapa la boca del mensajero. Porque la quiebra, que asusta tanto, no es la enfermedad: es la curación. Es el momento en que los recursos atrapados en proyectos imposibles se liberan para volver a algo útil. Impedirla no salva nada —solo congela el error en su sitio, consumiendo recursos que harían falta en otra parte—. Rothbard lo dice sin rodeos: la depresión es',

    ("quote",
     '"un proceso doloroso pero ineludible mediante el cual el mercado se libera de los excesos y errores del auge y restaura el funcionamiento eficiente de la economía."',
     'Rothbard, <em>Hacia una nueva libertad</em>'),

    'Hay una imagen que Rothbard rescató de los economistas del siglo XIX y que captura esto mejor que ninguna otra: la del narcótico. El crédito nuevo que sostiene el auge actúa como una droga —alivia el dolor un rato, hace sentir que todo va bien, pero no cura nada; solo pospone el ajuste y agrava la enfermedad de fondo—. Cada dosis para evitar el dolor exige la siguiente, más grande. Y el día en que ya no se puede inyectar más, el derrumbe es mucho peor de lo que habría sido si se hubiera sentido el dolor a tiempo. Llevado al extremo, ese camino ni siquiera termina en un derrumbe más grande: termina en la muerte del paciente —la destrucción de la moneda misma, cuando las dosis se vuelven tan enormes que el dinero deja de valer y deja de servir—. Por eso el dinero deshonesto es doblemente dañino en este capítulo: primero creó el error falsificando la tasa, y ahora impide que se descubra, anestesiando la señal que lo delataba.',

    'Recoja la forma de lo que acaba de ver, porque es la misma de siempre, ahora aplicada a una señal nueva. La causa sigue siendo la preferencia temporal de la sociedad; su consecuencia física, el ahorro real disponible. Pero la señal de este capítulo no es la tasa: son las pérdidas y ganancias, el mecanismo que detecta si los recursos se emplearon bien o mal. Cuando el dinero es honesto, esa señal funciona —las pérdidas avisan, los errores se corrigen, los recursos vuelven a buen uso—. Cuando el dinero se crea de la nada, la señal puede silenciarse: se rescata lo que debía quebrar, se sostiene lo que debía caer, y el error se vuelve crónico. Una sociedad que no puede sentir sus pérdidas es una sociedad que no puede corregir sus errores.',

    'Hasta aquí hemos seguido el error en el tiempo: cómo nace (la tasa falsa), qué destruye (la estructura), cómo se detecta o se oculta (las pérdidas). Pero la falsificación del dinero no solo desordena el <em>cuándo</em> de la economía —qué se construye para hoy y qué para mañana—. También desordena el <em>quién</em>: quién recibe el dinero nuevo primero, y quién lo recibe cuando ya no vale lo mismo. Hay un reparto oculto en toda falsificación monetaria, una transferencia silenciosa de riqueza de unos a otros, y casi nadie la ve porque ocurre en el lenguaje mudo de los precios. Esa es la señal que sigue.',
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
                 '<title>El dolor que avisa — Arregla el dinero, arregla el mundo</title>',
                 out, count=1, flags=re.DOTALL)
    out = re.sub(r'<article class="page"[^>]*>.*?</article>',
                 lambda _m: article, out, count=1, flags=re.DOTALL)
    new_nav = ('<nav class="nav-foot">'
               '<a class="prev" href="asignacion-intertemporal.html">La longitud de la cadena</a>'
               '<a class="idx" href="index.html">Índice</a>'
               '<a class="next" href="precios-relativos.html">Los primeros y los últimos</a></nav>')
    out = re.sub(r'<nav class="nav-foot">.*?</nav>',
                 lambda _m: new_nav, out, count=1, flags=re.DOTALL)
    out = out.replace('audio/tres-regimenes.mp3', 'audio/deteccion-mala-inversion.mp3')
    out = out.replace('audio/tres-regimenes.alignment.json',
                      'audio/deteccion-mala-inversion.alignment.json')
    out = out.replace('data-storage-key="tres-regimenes"',
                      'data-storage-key="deteccion-mala-inversion"')

    open('deteccion-mala-inversion.html', 'w', encoding='utf-8').write(out)
    n_par = sum(1 for it in CONTENT if isinstance(it, str) or (isinstance(it, tuple) and it[0] == "lead"))
    n_q = sum(1 for it in CONTENT if isinstance(it, tuple) and it[0] == "quote")
    print(f"deteccion-mala-inversion.html regenerado: {n_par} párrafos, {n_q} citas")


if __name__ == "__main__":
    main()
