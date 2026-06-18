#!/usr/bin/env python3
"""Construye el cap 17 «El Estado sin freno» (Bloque IV, tercera consecuencia).

Cap especial: cierra el Bloque IV Y el libro entero. La primera mitad
es la consecuencia política del dinero blando —el impuesto invisible,
la guerra/aparato/deuda que la imprenta vuelve posibles—. La segunda
mitad, después del ornamento partidor, es el cierre del libro: la
escalera completa, la tesis dicha por fin, y la última pregunta que
abre el camino a la respuesta del libro.

El ajá está en el párrafo «Y suba al último peldaño…» — donde el cap
crystaliza su patrón estructural: el que decide y el que paga, cada
vez más lejos el uno del otro.

NOTA EDITORIAL (autor): el texto fuente traía un placeholder
"[CITA HAYEK — verificar en Camino de servidumbre al rotar al corpus]"
que se quitó para esta publicación. Cuando se decida si se nombra la
obra o queda como referencia al concepto, se reincorpora con un
splice de audio + edit del builder.
"""
import re

EYEBROW = "Tercera consecuencia · el marco"
TITLE = "El Estado sin freno"
SUBTITLE = "El impuesto que nadie le puso enfrente para que lo aprobara"

CONTENT = [
    ("lead",
     'Haga una cuenta que casi nadie hace, porque incomoda. Su padre, con un solo sueldo, sostuvo una casa, una familia, quizá un carro, y le alcanzó para criarlo a usted y a sus hermanos. Usted trabaja más que él —más horas, más años de estudio encima, muchas veces dos ingresos en la casa en vez de uno— y, sin embargo, le cuesta llegar a lo mismo. No es una impresión: es una de las cosas más documentadas de las últimas décadas. Se produce más que nunca, se trabaja más que nunca, y al ciudadano común le queda, al final del mes, lo mismo o menos.'),

    '¿A dónde se fue la diferencia? Porque hay una diferencia. Entre lo que una sociedad produce hoy y lo que producía hace cincuenta años hay un abismo de riqueza —máquinas que multiplican el trabajo, tecnología que abarata todo, una productividad que sus abuelos no habrían soñado—. Esa riqueza existe; se creó. Pero no llegó a su bolsillo. Se fue a alguna parte. Y la pregunta de este capítulo es a dónde —porque la respuesta tiene un nombre, y no es el que primero viene a la mente—.',

    'La respuesta cómoda es "los impuestos". Y algo hay: usted ve lo que le descuentan, lo que paga en cada factura, lo que se lleva el recibo. Pero esos impuestos los ve —tienen un número, una ley, alguien a quien reclamarle—. Si todo lo que el Estado tomara fueran esos impuestos visibles, usted sabría exactamente cuánto sostiene, y podría, al menos en teoría, negarse —votar distinto, protestar, exigir que le rindan cuentas—. El impuesto que vamos a rastrear en este capítulo es otro: el que usted no ve, el que no aparece en ninguna factura, el que nadie le puso enfrente para que lo aprobara. Y es, de lejos, el más grande de los dos.',

    'Para verlo hay que volver a algo que usted ya entendió hace varios capítulos, solo que ahora con un protagonista nuevo. ¿Recuerda al que recibe el dinero nuevo primero —el que compra a precios de ayer, antes de que la marea de precios suba—? Vimos que ganaba a costa del que lo recibe último. Bueno: el que está más cerca de la imprenta, el primero de toda la fila, no es un banco ni una empresa. Es el que enciende la imprenta. Es el Estado.',

    'Piénselo despacio, porque es el corazón del capítulo. Un Estado tiene tres formas de conseguir lo que gasta. Puede cobrar impuestos —y entonces usted ve cuánto le quitan, y puede protestar—. Puede pedir prestado —y entonces alguien le presta de su voluntad, y habrá que devolverlo—. O puede, en el fondo, fabricar el dinero que necesita. Esta tercera es la favorita, y no por casualidad: es la única que le permite gastar sin pedirle permiso <em>a usted</em>.',

    'Y aquí conviene ser exacto, porque es fácil exagerar y perder la razón. No es que ese dinero se cree sin que nadie lo decida ni sin ningún control. Al contrario: hay un banco central, hay una junta, hay reuniones, actas, votaciones, incluso reglas que dicen hasta dónde se puede llegar. Formalmente, la decisión se aprueba. El problema es de quién es esa aprobación. El impuesto que se ve hay que pasarlo por donde usted, al menos en teoría, alcanza a mirar —un congreso que lo vota, una ley que se discute, funcionarios a los que puede echar en la próxima elección—. La imprenta se aprueba en otro cuarto: el de un puñado de funcionarios que usted no eligió, que no puede destituir, cuyas actas rara vez leerá, y que no le rinden cuentas a usted. No es que no haya freno. Es que el freno se trasladó a un lugar donde su voto no entra.',

    'Pero hay algo peor que un freno fuera de su alcance, y es un freno que cede. Porque esas reglas que dicen "hasta aquí" existen —topes de déficit, límites de deuda, mandatos de no financiar al gobierno—, y sin embargo, una y otra vez, se saltan. ¿Con qué excusa? Siempre la misma, y siempre razonable en el momento: <em>la situación lo amerita</em>. La pandemia lo ameritaba. La crisis financiera lo ameritaba. La guerra, la recesión, el desastre: cada uno, en su hora, ameritaba saltarse el límite "solo esta vez". Y aquí está la trampa, la misma que Hayek describió hace ochenta años: el Estado no derriba sus frenos de un golpe, como un tirano. Los va doblando, excepción por excepción, cada una con su buena razón —hasta que el límite sigue escrito en la ley pero ya no limita nada—. El dinero blando es lo que vuelve esto posible, porque con él la emergencia <em>siempre</em> encuentra con qué financiarse. Con dinero que no se puede fabricar, cuando se acaba, se acabó: ninguna emergencia crea oro de la nada, y el freno aguanta porque no hay forma de saltárselo. Con imprenta, no hay emergencia que no se pueda pagar —y por tanto no hay freno que no se pueda doblar—.',

    'Ahí está el impuesto, escondido a plena vista. Cuando el Estado fabrica dinero y lo gasta, ese dinero nuevo no representa nada que se haya producido: es la segunda puerta del capítulo tres, abierta por el que tiene la llave maestra. Sale a comprar —armas, obras, nóminas, favores— a los precios de hoy, que aún no han subido. Pero al gastarlo, empuja los precios hacia arriba, y para cuando esa marea llega a su sueldo, a sus ahorros, al precio de su mercado, el Estado ya compró lo que quería con dinero que todavía valía. Usted paga la diferencia. No en una factura: en que su dinero, el mismo de siempre, ahora compra menos. El Estado se llevó un pedazo de su trabajo, y el recibo de ese cobro fue el alza de precios que usted maldijo sin saber que era la cuenta.',

    'Por eso es un impuesto, aunque no lo parezca. Es exactamente lo que vimos en <em>El robo sin ladrón</em>, pero ahora con su destino a la vista: aquel capítulo mostró que el ahorro se diluía; este muestra hacia dónde se fue lo diluido. No se evaporó. Cambió de manos. De las suyas a las del que enciende la imprenta.',

    '¿Y en qué se gasta ese dinero que entró sin pedir permiso? En lo que sea que el que manda quiera, y esa es justamente la cuestión —porque lo que un Estado hace cuando puede gastar sin que usted lo frene dice mucho de por qué el freno importaba—. Vale la pena ver tres destinos, porque suben, uno tras otro, en una misma escala: la de cuán lejos está, del que paga, el que decidió el gasto.',

    'Empiece por el más antiguo y más brutal: la guerra. Una guerra cuesta más de lo que ningún pueblo aceptaría pagar de su bolsillo —ya lo dijimos en la primera página de este libro—. Si hubiera que cobrarla de frente, en efectivo, con un impuesto visible que cada quien viera salir de su sueldo, muchas guerras se apagarían por falta de fondos: la gente se negaría a financiarlas. Por eso no se cobran así. Se imprimen. El Estado fabrica el dinero, paga las armas a precios de hoy, y reparte la cuenta —callada, diluida en el precio de todo— sobre una población que jamás la aprobó y que muchas veces ni sabrá que la pagó. La guerra es el primer escalón: el que paga no la votó, pero al menos está vivo para sufrirla.',

    'Suba un peldaño, a algo menos espectacular pero más constante: el aparato que crece. Un Estado que puede financiarse sin pedir permiso tiende, sencillamente, a agrandarse —más programas, más nóminas, más dependencias, más de todo—, no por un plan maligno, sino porque le quitaron lo único que antes lo contenía: tener que cobrarle de frente al ciudadano cada peso que gasta. Cuando crecer no cuesta votos, se crece. Y cada año el ciudadano sostiene una maquinaria un poco más grande que el año anterior, sin que nadie le haya preguntado si la quería más grande. No la eligió. Le llegó, como le llegó el alza de precios: por debajo, sin recibo.',

    ("aja",
     'Y suba al último peldaño, el más injusto de todos, porque el que paga ni siquiera está aquí para protestar: la deuda. Cuando ni la imprenta ni los impuestos alcanzan, el Estado pide prestado —y esa cuenta no la paga quien la contrae—. La firma una generación y la cobran las siguientes: hijos y nietos que cargarán, en impuestos y en dinero diluido, el gasto de un presente en el que no tuvieron voz porque todavía no existían. Es el extremo de la misma lógica que recorre el capítulo: la guerra se la cobran al que no la votó; el aparato, al que no lo eligió; la deuda, al que ni siquiera ha nacido. Tres destinos, una sola dirección —el que decide y el que paga, cada vez más lejos el uno del otro, hasta que el que paga ya no puede ni quejarse, porque no llegó a tiempo para hacerlo—.'),

    ("ornament",),

    'Y aquí, donde termina el recorrido por las consecuencias, conviene detenerse a mirar hacia atrás el camino entero, porque las piezas que parecían sueltas son una sola.',

    'Vinimos bajando una escalera. Arriba estaba la herida más callada: el horizonte que se encoge, la cuenta del futuro que se tuerce en millones de cabezas a la vez, sin que nadie lo decida. Un peldaño más abajo, esa cuenta torcida puesta a trabajar sobre lo que cada uno tenía: el bosque vendido, la tierra exprimida, el manantial cambiado por el balde —el hombre que liquida lo suyo porque el dinero le borró el mañana—. Y al fondo, el último peldaño: el que ya no se hace daño a sí mismo, sino que se lo hacen —el trabajo que se va, callado, hacia guerras que no votó, hacia un aparato que no eligió, hacia deudas que pagarán los que aún no nacen—.',

    'Parecían cosas distintas: ecología, economía, política. No lo son. En cada peldaño estaba la misma mano, haciendo siempre lo mismo: tomar una señal que debía decir la verdad y torcerla, hasta que millones de personas honestas, leyendo bien una cifra que mentía, decidieron mal sin saberlo. El leñador, el campesino, el ahorrador, el ciudadano que ve evaporarse su sueldo —ninguno fue imprudente, ninguno fue avaro—. Todos hicieron la cuenta. Y la cuenta estaba envenenada en la raíz, porque el dinero con que se hace toda cuenta se podía fabricar de la nada.',

    'Esa es la tesis entera de este libro, dicha por fin completa. No hay seis problemas con seis culpables. Hay un dinero que miente, y un mundo entero construido sobre sus mentiras —los bosques que caen, la comida que no nutre, el horizonte que se acorta, el Estado que no encuentra freno—. Arregle el dinero, y no arregla una de esas cosas: las desactiva todas en su raíz, porque le quita a la mentira el lugar por donde entraba.',

    'Y aquí es donde el libro tendría que ofrecerle el consuelo de siempre —elija mejores gobernantes, exija mejores políticas, vote distinto—. No se lo voy a ofrecer, porque sería mentirle. Usted ya vio por qué. El problema no es quién enciende la imprenta: es que la imprenta exista, y que quien la tenga —cualquiera que sea, con la mejor de las intenciones— termine, tarde o temprano, empujado por la misma lógica a usarla. No se trata de poner a la persona correcta frente a la palanca. Se trata de que mientras haya palanca, habrá mano que la accione, y cuenta envenenada, y mundo torcido.',

    'Entonces queda una sola pregunta, y es la que ha estado esperando al final de todo el camino. Si el problema no es quién controla el dinero, sino que el dinero pueda fabricarse —si ni el mejor gobierno, ni la mejor ley, ni la mejor intención cierran esa puerta mientras la puerta exista—, entonces, ¿cómo se opta por algo mejor? ¿Existe siquiera un dinero que ninguna mano pueda fabricar, que ninguna emergencia pueda doblar, que ningún comité pueda empujar? ¿Un dinero que no haya que confiarle a nadie, porque nadie pueda mentir con él?',

    'La respuesta es lo que queda de este libro.',
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
        elif it[0] == "ornament":
            parts.append('    <div class="ornament">• • •</div>\n')
    parts.append('\n  </div>\n\n</article>')
    article = ''.join(parts)

    sk = open('tres-regimenes.html', encoding='utf-8').read()
    out = sk
    out = re.sub(r'<title>.*?</title>',
                 '<title>El Estado sin freno — Arregla el dinero, arregla el mundo</title>',
                 out, count=1, flags=re.DOTALL)
    out = re.sub(r'<article class="page"[^>]*>.*?</article>',
                 lambda _m: article, out, count=1, flags=re.DOTALL)
    new_nav = ('<nav class="nav-foot">'
               '<a class="prev" href="comerse-la-semilla.html">Comerse la semilla</a>'
               '<a class="idx" href="index.html">Índice</a>'
               '<a class="next" href="arregla-el-dinero-arregla-el-mundo.html">Arregla el dinero, arregla el mundo</a></nav>')
    out = re.sub(r'<nav class="nav-foot">.*?</nav>',
                 lambda _m: new_nav, out, count=1, flags=re.DOTALL)
    out = out.replace('audio/tres-regimenes.mp3', 'audio/el-estado-sin-freno.mp3')
    out = out.replace('audio/tres-regimenes.alignment.json',
                      'audio/el-estado-sin-freno.alignment.json')
    out = out.replace('data-storage-key="tres-regimenes"',
                      'data-storage-key="el-estado-sin-freno"')

    open('el-estado-sin-freno.html', 'w', encoding='utf-8').write(out)
    n_par = sum(1 for it in CONTENT if isinstance(it, str) or (isinstance(it, tuple) and it[0] == "lead"))
    n_aja = sum(1 for it in CONTENT if isinstance(it, tuple) and it[0] == "aja")
    n_orn = sum(1 for it in CONTENT if isinstance(it, tuple) and it[0] == "ornament")
    print(f"el-estado-sin-freno.html regenerado: {n_par} párrafos, {n_aja} ajá, {n_orn} ornamento partidor")


if __name__ == "__main__":
    main()
