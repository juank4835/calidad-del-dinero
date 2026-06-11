#!/usr/bin/env python3
"""Construye el cap 12 «El robo sin ladrón» (Bloque III, sexta pieza).

Reescritura desde una HTML hecha a mano. El título pasa a humano:
«El robo sin ladrón» (técnico revelable en el índice: «El poder
adquisitivo del dinero»). El slug se mantiene: poder-adquisitivo.html

Cambios respecto a la versión hecha a mano:
- Título humano + técnico revelable.
- Subtítulo nuevo: «Cómo se esfuma el trabajo de una vida sin que
  nadie meta la mano en su bolsillo» — explicita la pregunta del cap.
- Párrafo 8 (el balde) expandido: ahora dice explícitamente que
  «el balde no tiene ningún agujero», que «nadie tocó lo suyo» y
  remata con «por eso no hay ladrón que atrapar». Esa frase es la
  que conecta con el nuevo título «El robo sin ladrón».
- Mini-fix tipográfico en cierre de «Recoja la forma»: tenía un
  doble em-dash «tiene——» que ahora queda como «tiene—».

Estructura:
- Header: eyebrow «Sexta pieza · gravedad media» + h1 «El robo sin
  ladrón» + subtítulo.
- Prosa corrida sin secciones.
- 2 citas Rothbard (El hombre/economía/Estado, ¿Qué ha hecho...?).
"""
import re

EYEBROW = "Sexta pieza · gravedad media"
TITLE = "El robo sin ladrón"
TITLE_TECNICO = "El poder adquisitivo del dinero"
SUBTITLE = "Cómo se esfuma el trabajo de una vida sin que nadie meta la mano en su bolsillo"

CONTENT = [
    ("lead",
     'Tal vez usted conozca esta historia, porque en América Latina casi todos la conocemos. Una persona trabaja toda su vida —cuarenta, cincuenta años de levantarse temprano—, y va guardando. No despilfarra: ahorra, con la disciplina de quien sabe lo que cuesta cada peso. Guarda pensando en la vejez, en dejarles algo a los hijos, en no ser una carga. Y un día, ya viejo, va a contar lo que juntó en toda una vida de esfuerzo… y descubre que no alcanza para casi nada. El número en la libreta es grande, más grande que nunca. Pero lo que ese número compra se ha encogido hasta volverse casi nada.'),

    'Lo desconcertante es que esa persona no hizo nada malo. No perdió el dinero, no se lo robaron de la casa, no lo apostó. Hizo exactamente lo que se supone que uno debe hacer: trabajar y ahorrar. Y aun así, el fruto de toda una vida se evaporó mientras estaba guardado, quieto, donde debía estar seguro. ¿Cómo se esfuma una vida de trabajo sin que nadie meta la mano en el bolsillo, sin un ladrón, sin un robo que denunciar?',

    'Esa es la pregunta de este capítulo. Y la respuesta es la pieza del dinero que el ciudadano de a pie siente más de cerca —la única que no necesita que nadie se la explique, porque la vive—: si el dinero conserva, o no, el valor de lo que uno mete en él.',

    'Pongámosle nombre a lo que esa persona perdió. No perdió pesos —los pesos siguen ahí, en la libreta, más numerosos que nunca—. Perdió poder adquisitivo: la capacidad de su dinero para comprar cosas reales. Y esa es la medida que de verdad importa, porque a nadie le sirve el dinero por el dinero mismo; le sirve por lo que puede cambiar por él —un techo, comida, la educación de un hijo, descanso al final de la vida—. El poder adquisitivo es eso: cuánto mundo real cabe dentro de lo que usted tiene guardado.',

    'Es, si quiere, la otra cara de la pieza anterior. Allá nos preguntábamos si la unidad de medida conservaría su tamaño hacia el futuro, para poder planear. Aquí la pregunta es más inmediata: lo que usted ya guardó, ¿sigue valiendo lo que valía? No mira hacia el futuro que quiere construir, sino hacia el pasado que ya construyó y puso a salvo.',

    'Y conviene ver con claridad qué es lo que se mide, porque es fácil confundirse. El poder adquisitivo no se mide en el número —ese puede crecer y crecer mientras lo que compra se desploma—. Se mide en cosas: cuántos panes, cuántos litros de leche, cuántos metros de techo compra una unidad de su dinero. Cuando ese poder baja, usted es más pobre, aunque el número de su cuenta sea idéntico o mayor. La riqueza nunca estuvo en los números: estuvo siempre en lo que los números pueden comprar.',

    'Entonces, ¿qué le pasó a la persona que ahorró toda una vida? No le subieron los precios por arte de magia. Pasó algo más concreto, y lo venimos viendo desde el principio del libro: mientras ella guardaba, alguien estuvo creando dinero nuevo de la nada. Y cada unidad nueva que aparece no añade riqueza —no hay más panes, ni más techos, ni más trabajo en el mundo por el hecho de imprimir—; lo único que hace es repartir el mismo valor entre más unidades. Cada peso nuevo que se crea le resta un poco de valor a todos los pesos que ya existían —incluidos los que ella tenía guardados—. Su dinero no se movió de la cuenta; pero el valor se le fue saliendo por debajo, diluido por cada unidad que se fabricó mientras dormía.',

    'Es importante ver por qué esto solo puede pasar con cierto tipo de dinero. Con dinero honesto —ese que nadie puede crear por decreto— lo que usted guarda se queda quieto en valor, o incluso vale más con el tiempo: si la sociedad produce más cosas y la cantidad de dinero no se infla, cada unidad compra más, no menos. Ahorrar, bajo dinero honesto, es guardar el fruto del trabajo tal cual, sin que se derrita. Pero con dinero que se crea de la nada, ahorrar se siente como llenar un balde con una fuga en el fondo: usted echa agua —trabaja, guarda—, y el nivel baja igual. Solo que fíjese bien, porque aquí está la trampa del crimen perfecto: el balde no tiene ningún agujero. Nadie le saca una gota de su agua —sus pesos siguen ahí, completos, contables—. Lo que hacen es agrandar el balde: crean más unidades, y su agua, la misma de siempre, pasa a llenar una fracción cada vez menor. Por eso no hay ladrón que atrapar: nadie tocó lo suyo. Tocaron el tamaño de todo lo demás.',

    'Y aquí está lo que vuelve este saqueo distinto de cualquier otro: es un robo que no deja huellas. Cuando suben un impuesto, usted lo ve: hay una ley, un debate, un porcentaje con nombre, alguien a quien reclamarle. Cuando le roban la casa, hay un delito, una víctima, una denuncia. Pero cuando le diluyen el ahorro creando dinero, no hay ley que usted haya votado, no hay una cifra que le hayan cobrado, no hay un culpable señalado, no hay siquiera un momento exacto en que ocurrió —fue gota a gota, todos los días, durante años—. Por eso es el saqueo perfecto: empobrece a millones sin que ninguno pueda señalar el instante en que le quitaron algo. Es un impuesto que nadie aprobó, que no aparece en ninguna factura, y que recae con más fuerza sobre quien menos puede defenderse: el que ahorra en efectivo, el que no tiene cómo poner su dinero a salvo, el viejo de nuestra historia.',

    'No es una metáfora llamarlo impuesto. Es, literalmente, la forma de recaudar más antigua y más cómoda para quien manda, porque no requiere aprobar nada ni dar la cara. Rothbard lo nombra sin eufemismos —y señala quién termina pagándolo—:',

    ("quote",
     '"El impacto de la inflación es especialmente grave sobre los grupos de ingreso relativamente \'fijo\', cuyas pérdidas terminan después de un período largo o no terminan nunca."',
     'Rothbard, <em>El hombre, la economía y el Estado</em>, cap. 12'),

    'Los grupos de ingreso fijo: los pensionados, los que viven de una renta, los que ahorraron en efectivo para la vejez. El viejo de nuestra historia no es una excepción desafortunada —es el blanco estructural de este impuesto que nadie votó—.',

    'Hay una consecuencia de esto que va más hondo que el robo mismo. Piense en lo que el dinero que se diluye le enseña a la gente: que ahorrar es de tontos, que guardar el fruto del trabajo es verlo derretirse, que el prudente —el que se aguanta, el que posterga, el que junta para el futuro— es castigado, mientras el que gasta todo de inmediato al menos no pierde. El dinero malo invierte el premio y el castigo: vuelve insensato lo que siempre fue sensato. Rothbard lo dijo en una línea:',

    ("quote",
     '"La inflación penaliza la austeridad y favorece el endeudamiento... El incentivo, entonces, es endeudarse y pagar después en vez de ahorrar y prestar."',
     'Rothbard, <em>¿Qué ha hecho el gobierno de nuestro dinero?</em>'),

    'Y la gente no es tonta: aprende. Si guardar pierde, la respuesta racional es no guardar —gastar ya, mientras el dinero todavía compra, o lanzarse a inversiones cada vez más arriesgadas, no por audacia sino por defensa—. La virtud del ahorro, que cualquiera podía practicar, se vuelve un lujo de expertos: bajo dinero honesto el camino seguro de una familia común era trabajar, guardar, esperar; bajo dinero que se diluye, ese camino se cierra.',

    'Es la inversión completa: un buen dinero premia la paciencia y hace del ahorro el camino natural de cualquiera; un dinero que se diluye premia la impaciencia y empuja a todos a vivir el corto plazo. No es solo que le roben a usted sus ahorros: es que le enseñan a usted, y a todos, a no ahorrar. Y eso —lo que el dinero malo le hace, a la larga, a la paciencia de un pueblo entero— es quizá la consecuencia más honda de todas; pero tiene su propio lugar más adelante en el libro. Por ahora basta con ver que el saqueo no termina en el bolsillo: también toca el carácter.',

    'Y ahora la pregunta de siempre: ¿de qué depende que el dinero conserve el valor de lo que usted guarda, o se lo diluya? Depende, como todo en este libro, de si se puede crear de la nada. El dinero fiat puede —y por eso diluye—: cada unidad nueva que el comité decide imprimir es un poco de valor que sale, sin aviso, de todo lo que ya estaba guardado. Es el único de los tres regímenes que saquea por esta vía, y lo hace por diseño.',

    'Frente a él, los dos dineros honestos se comportan igual, y por eso aquí vuelven a ir del brazo. Ni el oro ni Bitcoin se pueden crear por decreto, y por eso ninguno de los dos diluye lo que usted guarda: lo que ahorra en ellos conserva su valor, porque nadie puede fabricar unidades nuevas para licuar las suyas. En la pieza anterior —la predecibilidad— los separamos, porque mirando al futuro no son idénticos. Pero en esta, la de preservar el valor de lo ya guardado frente a la dilución, están del mismo lado: los dos protegen el fruto del trabajo, mientras que el fiat lo derrite. Lo que ahorró aquella persona se habría salvado en cualquiera de los dos; lo que la arruinó fue el único de los tres que se puede imprimir.',

    'Recoja la forma, que es la de siempre. La causa es la misma de todo el libro: el trabajo guardado, el ahorro de quien prefirió esperar. La pieza de este capítulo no es una señal sobre el mundo, sino una propiedad del dinero mismo: el poder adquisitivo —cuánto vale, en cosas reales, lo que usted tiene—. La lectura es tan directa que no necesita teoría: usted abre la billetera y ve qué alcanza. Y el desenlace depende, como siempre, del dinero: si es honesto, lo guardado se conserva y el trabajo de una vida sigue siendo el trabajo de una vida; si se puede crear de la nada, lo guardado se diluye y el trabajo de una vida se evapora sin que nadie lo toque.',

    'De todas las piezas que hemos recorrido, esta es la que cualquiera puede comprobar sin saber una palabra de economía: basta con haber visto a un abuelo contar lo que juntó, o con recordar lo que costaba el pan hace diez años. Y por eso mismo es la más reveladora. Un dinero honesto es el único que le devuelve, intacto, el trabajo que usted le confió —no se lo multiplica por arte de magia, pero tampoco se lo roba en silencio—. Guardar en él es guardar de verdad: lo que usted metió es lo que encontrará, esperándolo, cuando lo necesite. Eso, que debería ser lo mínimo que se le pide a un dinero, resulta ser un privilegio que solo el dinero honesto concede.',

    'Hasta aquí hemos visto el saqueo por el lado del que guarda: el ahorro que se diluye. Pero hay otra mano en el mismo bolsillo, y mira al otro lado del mostrador —no a quien guarda el dinero, sino a quien lo recibe nuevo—. Porque el dinero que se crea de la nada no se reparte por igual ni llega a todos: alguien decide a quién se le presta primero, y ese alguien no es un mercado ciego, sino una banca que favorece a los suyos. Quién tiene acceso al dinero nuevo y quién no —quién está adentro y quién toca una puerta que no se abre— es la siguiente pieza, y revela que el dinero malo no solo empobrece a quien ahorra: también escoge, de antemano, a quién enriquece.',
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
                 '<title>El robo sin ladrón — Arregla el dinero, arregla el mundo</title>',
                 out, count=1, flags=re.DOTALL)
    out = re.sub(r'<article class="page"[^>]*>.*?</article>',
                 lambda _m: article, out, count=1, flags=re.DOTALL)
    new_nav = ('<nav class="nav-foot">'
               '<a class="prev" href="predictibilidad-estructural.html">La cinta métrica</a>'
               '<a class="idx" href="index.html">Índice</a>'
               '<a class="next" href="asignacion-credito.html">La asignación del crédito</a></nav>')
    out = re.sub(r'<nav class="nav-foot">.*?</nav>',
                 lambda _m: new_nav, out, count=1, flags=re.DOTALL)
    out = out.replace('audio/tres-regimenes.mp3', 'audio/poder-adquisitivo.mp3')
    out = out.replace('audio/tres-regimenes.alignment.json',
                      'audio/poder-adquisitivo.alignment.json')
    out = out.replace('data-storage-key="tres-regimenes"',
                      'data-storage-key="poder-adquisitivo"')

    open('poder-adquisitivo.html', 'w', encoding='utf-8').write(out)
    n_par = sum(1 for it in CONTENT if isinstance(it, str) or (isinstance(it, tuple) and it[0] == "lead"))
    n_q = sum(1 for it in CONTENT if isinstance(it, tuple) and it[0] == "quote")
    print(f"poder-adquisitivo.html regenerado: {n_par} párrafos, {n_q} citas")


if __name__ == "__main__":
    main()
