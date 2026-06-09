#!/usr/bin/env python3
"""Construye el cap 5 «Lo que la espera libera» (Segundo cimiento, Bloque II).

Reescritura completa del cap 5. Reemplaza el contenido actual de
ahorro-real.html con una versión que arranca por la pregunta «¿qué
acaba de hacer cuando ahorró?» y construye el ahorro como liberación
de recursos reales (no como número en una pantalla), preparando la
señal-mensajero que se desarrolla en el resto del libro.

Estructura:
- Header: eyebrow «Segundo cimiento» + h1 «Lo que la espera libera» +
  subtítulo.
- Prosa corrida (sin secciones), sin citas en bloque.
- Algunos términos clave en cursiva (<em>): «no consumió», «más
  dinero», «mintiendo».
"""
import re

EYEBROW = "Segundo cimiento"
TITLE = "Lo que la espera libera"
SUBTITLE = "Por qué ahorrar no es guardar dinero, sino liberar pedazos del mundo"

CONTENT = [
    ("lead",
     'Este mes le sobró algo. No mucho —una parte del sueldo que, en lugar de gastarla, decidió apartar—. La dejó en la cuenta, no la tocó, y siguió con su vida. Hagámonos una pregunta que parece tonta de tan obvia: ¿qué acaba de hacer?'),

    '"Guardé dinero", dirá usted. "Ahorré." Y no se equivoca. Pero esa respuesta mira el lado de adentro —el número en la pantalla, el saldo que sube— y se pierde el otro lado, el que de verdad importa: el del mundo de las cosas. Porque al no gastar ese dinero, usted dejó sin reclamar cosas reales que habría consumido —una comida, un viaje, unas cosas de la tienda—, y todas ellas quedaron ahí afuera, libres, disponibles para otra cosa. Eso, y no el saldo quieto en su cuenta, es lo que de verdad acaba de hacer.',

    'Suena a un detalle sin importancia —¿qué más da mirarlo de un lado o del otro, si el dinero es el mismo?—. Pero en esa diferencia, la de mirar el número o mirar las cosas, está escondido casi todo lo que este libro necesita que usted vea. Empezando por algo que en América Latina muchos han vivido en carne propia: cómo se puede guardar dinero con disciplina, durante toda una vida, y llegar al final con las manos casi vacías.',

    'Eso que usted acaba de hacer al apartar parte de su sueldo, hagámoslo ahora con alguien a quien ya conoce. Vuelva a Juan, el del capítulo anterior —el que apartaba una parte de lo que ganaba en lugar de gastárselo todo—. Con usted solo, el ahorro se veía a medias: vimos las cosas que quedaron libres, pero no a dónde fueron a parar. Con Juan y alguien más podremos seguirlas hasta el final, y ahí se ve entero lo que el ahorro de verdad es.',

    'Empecemos por Juan, que hace exactamente lo que hizo usted. Al no gastar una parte de su sueldo, Juan <em>no consumió</em> cosas que habría consumido: no se comió ciertos alimentos, no llenó el tanque con cierta gasolina, no se llevó de la tienda la ropa o las cosas que se le antojaban. Nada de eso desapareció porque Juan no lo usara. Quedó ahí, intacto, disponible, esperando que alguien lo reclamara. Eso es lo que Juan hizo de verdad al ahorrar: no metió un número en una pantalla, sino que dejó libres unos pedazos del mundo real que, de haberlos gastado, ya no estarían.',

    'Y aquí viene la pregunta que con usted solo no podíamos hacer: esos pedazos del mundo que Juan dejó libres, ¿para quién quedaron disponibles?',

    'La respuesta es la otra mitad de la historia, y sin ella el ahorro no se entiende. Esos pedazos del mundo que Juan dejó libres son, exactamente, lo que necesita alguien que quiere construir algo. Vuelva a Hernando, que quiere montar un taller: tiene el plan, la destreza, las ganas. Pero con ganas no se levanta un taller. Hace falta cemento, acero, herramientas, una bodega donde instalarlo. Y todo eso tiene que salir de algún lado —no se crea de la nada en el momento en que Hernando decide construir—.',

    '¿De dónde sale, entonces? De ahí: de las cosas que Juan, y otros como él, decidieron no consumir. El cemento que Hernando usa pudo fabricarse porque había materiales y energía que no se gastaron en otra cosa; pudo comprarlo porque esos recursos estaban libres, esperando. El ahorro de Juan no fue un número que se quedó quieto: fue el material con que Hernando construye. Lo que uno dejó de consumir es, literalmente, lo que el otro usa para edificar.',

    'Y fíjese en el papel que jugó el dinero en todo esto: ninguno, salvo el de mensajero. El dinero le avisó a Hernando que había recursos libres y le dio el derecho a reclamarlos; pero el taller no se levanta con billetes, se levanta con cemento y acero. El dinero solo conectó una cosa con la otra —le pasó a Hernando el aviso de que Juan había dejado algo disponible—. Fue el que llevó el mensaje entre el que ahorró y el que construye. Importante, pero nada más que eso.',

    'Y aquí aparece la grieta de la que cuelga el resto del libro. Conviene verla despacio, porque es sencilla y lo cambia todo. Acabamos de decir que el dinero es el mensajero: lo que de verdad importa son los recursos reales que el ahorro dejó libres, y el dinero solo los representa, los cuenta, los pasa de mano en mano. Pues bien: el mensajero se puede fabricar. Los recursos, no.',

    'Piénselo un momento, porque la asimetría es el corazón del asunto. Imprimir un billete toma un segundo. Pero no se imprime el saco de cemento, ni el litro de gasolina, ni el alimento que ese billete promete —esos hay que producirlos, y producirlos toma tiempo, esfuerzo, recursos que alguien tuvo que dejar libres—. El mensajero es fácil de crear; lo que el mensajero anuncia, no.',

    'Mire entonces los dos casos, uno al lado del otro. Cuando el dinero nace del ahorro de verdad —cuando Juan efectivamente dejó de consumir—, cada billete que llega a Hernando tiene detrás un pedazo del mundo esperándolo: el cemento existe, el acero existe, alguien los liberó. El mensajero dice la verdad. Pero cuando el dinero simplemente se imprime, aparecen billetes nuevos sin que nadie haya dejado nada libre. El mensajero llega igual, anunciando recursos disponibles —pero esta vez no hay nada detrás—. Trae un aviso de cemento que nadie produjo.',

    'Y fíjese en lo que esto significa, porque no es lo que parece. El problema no es que haya <em>más dinero</em> —como si el daño fuera una cuestión de cantidad, de que ahora circulan más billetes—. El problema es que el dinero está <em>mintiendo</em>. Si el dinero es lo que le avisa a la sociedad cuántos recursos hay libres para construir, entonces imprimir billetes sin ahorro detrás no crea recursos: crea avisos falsos sobre recursos que no existen. Es la segunda puerta del capítulo tres, vista ahora por dentro.',

    'Y alguien le cree. Vuelva a Hernando una última vez. Recibe el dinero impreso, lee el aviso que siempre supo leer —"hay cemento, hay acero, adelante con tu taller"— y hace lo que haría cualquiera: empieza a construir. Compra lo que puede, levanta los muros, y a mitad de obra descubre que los materiales no alcanzan, que cada cosa cuesta más de lo que esperaba, que algo no cuadra. No fue mala suerte ni mal cálculo. Fue que el aviso mentía: le prometieron un cemento que nadie había producido. Hernando hizo todo bien; construyó sobre un mundo que solo existía en el mensaje.',

    'Eso es lo que un dinero deshonesto le hace a una sociedad entera —no a un Hernando, sino a millones a la vez—: les promete recursos que no están, y los pone a construir sobre el vacío. A entender cómo ocurre eso, pieza por pieza, y qué señales se corrompen en el camino, dedicaremos lo que viene. Porque el dinero, ya lo vio, no es un número en una pantalla. Es un mensaje. Y de que ese mensaje diga la verdad depende que lo que una sociedad construye se sostenga, o se derrumbe.',
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

    # Esqueleto del cap 3 (tres-regimenes.html)
    sk = open('tres-regimenes.html', encoding='utf-8').read()
    out = sk
    out = re.sub(r'<title>.*?</title>',
                 '<title>Lo que la espera libera — Arregla el dinero, arregla el mundo</title>',
                 out, count=1, flags=re.DOTALL)
    out = re.sub(r'<article class="page"[^>]*>.*?</article>',
                 lambda _m: article, out, count=1, flags=re.DOTALL)
    new_nav = ('<nav class="nav-foot">'
               '<a class="prev" href="preferencia-temporal.html">Saber esperar</a>'
               '<a class="idx" href="index.html">Índice</a>'
               '<a class="next" href="cuando-un-precio-dice-la-verdad.html">¿Cuándo un precio dice la verdad?</a></nav>')
    out = re.sub(r'<nav class="nav-foot">.*?</nav>',
                 lambda _m: new_nav, out, count=1, flags=re.DOTALL)
    out = out.replace('audio/tres-regimenes.mp3', 'audio/ahorro-real.mp3')
    out = out.replace('audio/tres-regimenes.alignment.json',
                      'audio/ahorro-real.alignment.json')
    out = out.replace('data-storage-key="tres-regimenes"',
                      'data-storage-key="ahorro-real"')

    open('ahorro-real.html', 'w', encoding='utf-8').write(out)
    n_par = sum(1 for it in CONTENT if isinstance(it, str) or it[0] == "lead")
    n_q = sum(1 for it in CONTENT if isinstance(it, tuple) and it[0] == "quote")
    print(f"ahorro-real.html regenerado: {n_par} párrafos, {n_q} citas")


if __name__ == "__main__":
    main()
