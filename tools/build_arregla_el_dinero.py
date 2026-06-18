#!/usr/bin/env python3
"""Construye el umbral de cierre «Arregla el dinero, arregla el mundo».

No es un capítulo numerado: es el remate del libro, el lugar donde se
nombra por fin la respuesta que el camino entero fue ganando. Aparece
en el índice dentro de un <div class="bisagra cierre">, no en un cap
numerado.

Estructura: 26 párrafos en 4 secciones, separadas por 3 ornamentos
partidores (• • •).
  1. Recapitulación de los protagonistas (Hernando, Francisco, el viejo…)
     — para no olvidar a quiénes se les debe la respuesta.
  2. La respuesta: Bitcoin es honesto Y ejercible sin permiso. El
     oro nunca pudo serlo.
  3. El mundo después del dinero arreglado: cada herida del libro,
     desactivada en su raíz.
  4. Cómo se opta por algo mejor: persona a persona, salida silenciosa.

Ajá marcado en «Por eso este libro no termina en una denuncia, sino
en una puerta abierta…» — el clic histórico que junta el predicamento
de siglos con la salida actual.
"""
import re

EYEBROW = "El remate · La respuesta ganada"
TITLE = "Arregla el dinero, arregla el mundo"
SUBTITLE = "Cómo se opta por algo mejor"

CONTENT = [
    # ===== Sección 1: la deuda =====
    ("lead",
     'Antes de decir la respuesta, vuelva a verlos a todos. Porque la respuesta no significará nada si no recuerda, primero, a quiénes se les debe.'),

    'Vuelva a Hernando, que leyó una tasa baja y entendió lo que esa señal siempre quiso decir —"hay recursos, adelante"—, y construyó su taller sobre un ahorro que nadie había hecho. No fue ingenuo. Leyó bien una cifra que mentía.',

    'Vuelva al pescador, que dejó las manos y se puso a levantar un astillero porque la señal decía que la aldea podía permitírselo, y se quedó a mitad de obra, sin astillero y sin pescado, porque las reservas que lo sostendrían no existían. No fue imprudente. Confió en un mensaje que el mundo no podía respaldar.',

    'Vuelva al que llegó último a la fila —el asalariado, el pensionado—, que cobró su dinero cuando los precios ya habían subido, y descubrió que su sueldo, idéntico al del año pasado, compraba menos. No perdió ninguna carrera por lento. Lo pusieron a correr una que estaba arreglada de antemano.',

    'Vuelva al viejo que ahorró toda su vida, peso a peso, con la disciplina del que sabe lo que cuesta cada uno, y llegó a la vejez a contar lo juntado y encontró que no alcanzaba para casi nada. No despilfarró. Guardó su trabajo en un balde al que, mientras dormía, le agrandaban el tamaño.',

    'Vuelva a Francisco, que amaba su nogal y lo taló. Al vecino, que tenía tierra viva y la dejó muerta. A usted, en su propia mesa, comiendo más que nunca y nutriéndose menos. Y vuelva, por fin, a usted otra vez, trabajando más que su padre para llegar a menos, sosteniendo sin saberlo guerras que no votó, un aparato que no eligió, deudas firmadas a nombre de nietos que no han nacido.',

    'Ninguno de ellos fue tonto. Ninguno fue avaro. Ninguno fue imprudente. Todos hicieron exactamente lo que hace una persona sensata: mirar las señales y decidir en consecuencia. Y a todos los traicionó lo mismo —no un villano, no una mala política, no un mal gobierno—: un dinero que se podía fabricar de la nada, y que por eso mentía en cada señal que tocaba.',

    'Esa es la deuda. Ahora la respuesta.',

    ("ornament",),

    # ===== Sección 2: la respuesta =====
    'A lo largo de este libro nos negamos a anunciarla. La fuimos ganando, eslabón por eslabón, sin nombrarla, porque una respuesta que se anuncia en la portada no se cree: se sospecha. Pero ya hicimos el camino entero. Ya tenemos la vara —la calidad de la información—, ya sabemos leer una señal, ya vimos las tres formas de organizar el dinero y supimos que solo dos resultados importan: o la señal dice la verdad, o miente. Ya seguimos la mentira por todas sus piezas y por todas sus consecuencias. Y al final del camino quedó una sola pregunta, la del capítulo anterior: ¿existe un dinero que ninguna mano pueda fabricar, que ninguna emergencia pueda doblar, que ningún comité pueda empujar, que no haya que confiarle a nadie?',

    'Existe. Y para decir su nombre con todo el peso que merece, hay que despejar primero al otro candidato —porque no es el único dinero honesto que hemos encontrado—.',

    'Durante casi todo el libro, el oro y Bitcoin viajaron juntos. Los llamamos, a los dos, dinero duro, dinero honesto, y con razón: ninguno se fabrica por decreto, ninguno miente sobre cuánto hay. Para la pregunta que vertebró cada capítulo —¿deja este dinero que la señal diga la verdad?— los dos están del mismo lado, el lado limpio. Si lo único que quisiéramos fuera un dinero que no mienta, podríamos detenernos aquí y decir: vuelva al oro. Ya lo conocemos, sostuvo el comercio del mundo durante milenios, y es honesto.',

    'Pero ya vimos por qué no alcanza. El oro es honesto, sí —y sin embargo, para usarlo, siempre hubo que entregárselo a alguien—. No se podía partir para el café, ni cruzar con él una frontera, ni meterlo por un cable, ni verificarlo sin un experto. Cada una de esas grietas terminaba en el mismo gesto: poner el oro en manos de otro —un banco, un custodio, un Estado—. Y un dinero que solo se usa en manos de otros termina, por su propia naturaleza, amontonado en pocas manos; y de esas manos llenas nacieron los recibos, y de los recibos el fraude, y del fraude todo lo que este libro denunció. El oro no nos traicionó por mala suerte. Nos entregó al dinero falso porque sus grietas nos obligaban a delegar, y delegar fue siempre el primer paso de la falsificación.',

    'Ahí está la diferencia que lo decide todo, y conviene decirla con precisión, porque no es la que se suele decir. La ventaja de Bitcoin sobre el oro no es que sea más cómodo —eso suena a capricho de la época, a preferir lo digital por moda—. Es algo mucho más hondo: el oro es honesto pero no se puede ejercer su honestidad sin delegarla, y al delegarla, se pierde. Bitcoin es la primera vez en la historia en que un dinero es honesto y, además, se puede ejercer esa honestidad sin pedirle permiso a nadie. No hay que partirlo en manos de un banco para gastarlo: se divide hasta lo infinitesimal, solo. No hay que entregarlo en una aduana para cruzarlo: viaja en una frase guardada en la memoria. No hay que confiar en la bóveda de un custodio: cada unidad está a la vista en un libro que cualquiera verifica desde su casa. No hay que creerle al emisor: no hay emisor.',

    'Por eso las ventajas prácticas de Bitcoin —que se divide, que viaja, que se verifica, que no se puede confiscar de un solo golpe— no son comodidades. Son las condiciones de que su honestidad sea ejercible. De nada sirve un dinero que no miente si, para usarlo, hay que ponerlo en manos de alguien que sí puede mentir. La honestidad que hay que delegar no es honestidad ejercida: es honestidad prestada, y lo prestado se puede no devolver. El oro ofrecía la honestidad y le cobraba, como precio de usarla, la delegación que la deshacía. Bitcoin es honesto sin esa letra pequeña.',

    'Y hay una segunda virtud, la que los separó en el capítulo de la cinta métrica. El oro es honesto pero no del todo predecible: nadie sabe cuánto vendrá, porque una veta nueva o un mejor método de extracción pueden sorprender. Bitcoin cierra esa última rendija: veintiún millones, ni uno más, en un calendario escrito que cualquiera puede leer hasta la última unidad que se emitirá dentro de más de un siglo. Honesto como el oro, y además predecible como el oro nunca pudo ser. Las dos virtudes que este libro buscó —que la señal diga la verdad, y que la cinta con que se mide el futuro no cambie de tamaño— por primera vez en la historia, en un solo dinero, y ejercibles sin permiso.',

    ("ornament",),

    # ===== Sección 3: el mundo después del dinero arreglado =====
    'Ahora vuelva a mirar todo el daño del libro, pero con esto en la mano.',

    'La tasa de interés mentía porque alguien podía bajarla fabricando dinero. Con un dinero que no se puede fabricar, la tasa vuelve a decir la verdad: refleja la paciencia que de verdad hay, los recursos que de verdad se liberaron. Hernando lee una señal que no miente, y construye sobre suelo firme.',

    'El ahorro se diluía porque alguien creaba unidades nuevas que licuaban las suyas. Con un dinero de cantidad fija, lo que el viejo guardó es lo que encuentra: su trabajo no se evapora mientras duerme. Ahorrar vuelve a ser lo que siempre debió ser —guardar el fruto del esfuerzo, intacto, hasta que haga falta—.',

    'El crédito fluía al privilegio porque había dinero fabricado para repartir entre los de adentro. Sin grifo que abrir, el banco vuelve a prestar lo que alguien ahorró de verdad, y el crédito busca el mérito, no la cercanía. La puerta que no se abría se abre para quien tiene un buen proyecto, tenga o no padrinos.',

    'Y el horizonte —la herida más honda— vuelve a estirarse. Un dinero que premia la espera, en vez de castigarla, le devuelve a la gente la razón para mirar lejos: para plantar el árbol, criar con paciencia, construir lo que tarda. Francisco no necesita talar el nogal que ama, porque el dinero ya no le borra el mañana. El Estado no encuentra la palanca, porque la palanca no existe —y lo que no puede financiarse sin pedir permiso, hay que pedir permiso para financiarlo—.',

    'Esa es la promesa entera del título, y ahora se entiende por completo. No es una consigna. Es una cadena de causa y efecto que usted ya recorrió: arregle el dinero, y arregla las señales; arregle las señales, y la sociedad vuelve a coordinarse sobre la verdad; y una sociedad que se coordina sobre la verdad construye un mundo distinto —uno donde el talento fluye a donde de verdad hace falta, donde el ahorro sostiene lo que dura, donde el futuro vuelve a pesar lo que debe pesar—. No porque alguien lo ordene desde arriba. Porque cada uno, leyendo señales que por fin dicen la verdad, decide bien sin necesidad de que nadie lo dirija. Arregla el dinero, arregla el mundo.',

    ("ornament",),

    # ===== Sección 4: cómo se opta =====
    'Queda lo más importante, y es lo más simple. ¿Cómo se opta por algo mejor?',

    'No con una revolución, no con una ley, no esperando a que los que tienen la imprenta decidan soltarla —no la soltarán—. Se opta por algo mejor de la única forma en que un dinero honesto se ha impuesto jamás: una persona a la vez, eligiendo guardar su trabajo en algo que no se le puede diluir, mentir ni confiscar. No hay que convencer a un gobierno. No hay que ganar una elección. Cada quien que mueve una parte de su esfuerzo a un dinero que no miente está, en silencio, votando con lo único que el falsificador no puede ignorar: su salida.',

    ("aja",
     'Por eso este libro no termina en una denuncia, sino en una puerta abierta. Durante siglos, la humanidad tuvo que elegir entre un dinero honesto que no podía ejercer y un dinero cómodo que la traicionaba. Era una elección imposible, y la resolvió mal cada vez. Por primera vez no hay que elegir. Existe un dinero que es honesto y ejercible, honesto y predecible, honesto y verificable por uno mismo —un dinero que no hay que confiarle a nadie, porque nadie puede mentir con él—.'),

    'El viejo no habría visto evaporarse su vida. Hernando no habría construido sobre el vacío. Francisco no habría levantado el hacha. Ninguno de ellos eligió el dinero con que lo engañaron —lo heredaron, como se hereda el aire que se respira, sin saber que podía ser de otro modo—. Usted ya sabe que puede ser de otro modo. Esa es la única diferencia entre usted y todos ellos. Y es toda la diferencia.',

    'Arregle el dinero. Lo demás viene solo.',
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
                 '<title>Arregla el dinero, arregla el mundo — Arregla el dinero, arregla el mundo</title>',
                 out, count=1, flags=re.DOTALL)
    out = re.sub(r'<article class="page"[^>]*>.*?</article>',
                 lambda _m: article, out, count=1, flags=re.DOTALL)
    # Cierre del libro: prev = cap 17, next vacío (no hay nada más después).
    new_nav = ('<nav class="nav-foot">'
               '<a class="prev" href="el-estado-sin-freno.html">El Estado sin freno</a>'
               '<a class="idx" href="index.html">Índice</a>'
               '<span></span></nav>')
    out = re.sub(r'<nav class="nav-foot">.*?</nav>',
                 lambda _m: new_nav, out, count=1, flags=re.DOTALL)
    out = out.replace('audio/tres-regimenes.mp3', 'audio/arregla-el-dinero-arregla-el-mundo.mp3')
    out = out.replace('audio/tres-regimenes.alignment.json',
                      'audio/arregla-el-dinero-arregla-el-mundo.alignment.json')
    out = out.replace('data-storage-key="tres-regimenes"',
                      'data-storage-key="arregla-el-dinero-arregla-el-mundo"')

    open('arregla-el-dinero-arregla-el-mundo.html', 'w', encoding='utf-8').write(out)
    n_par = sum(1 for it in CONTENT if isinstance(it, str) or (isinstance(it, tuple) and it[0] == "lead"))
    n_aja = sum(1 for it in CONTENT if isinstance(it, tuple) and it[0] == "aja")
    n_orn = sum(1 for it in CONTENT if isinstance(it, tuple) and it[0] == "ornament")
    print(f"arregla-el-dinero-arregla-el-mundo.html regenerado: {n_par} párrafos, {n_aja} ajá, {n_orn} ornamentos partidores")


if __name__ == "__main__":
    main()
