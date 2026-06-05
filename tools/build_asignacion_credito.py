#!/usr/bin/env python3
"""Reconstruye el capítulo «La asignación del crédito» con la estructura del
libro, usando el esqueleto del cap 3 (toda la maquinaria). El cuerpo es prosa
corrida (sin subtítulos de sección) con tres citas en bloque (Rothbard, Mises,
Rothbard).

Las citas se narran (el texto de la cita SÍ se lee), pero la referencia
bibliográfica (<cite class="no-audio">) NO se narra: las abreviaturas y los
números romanos suenan mal, y el narrador ya nombra al autor justo antes."""
import re

EYEBROW = "Séptima pieza · gravedad media"
TITLE = "La asignación del crédito"
SUBTITLE = "Quién recibe el crédito —y por qué casi nunca es usted"

# Items (sin secciones):
#   ("lead", texto)        → primer párrafo con capital
#   "texto"                → párrafo normal (se narra)
#   ("quote", texto, cita) → cita en bloque; el texto se narra, la cita no
CONTENT = [
    ("lead", 'Dos personas entran al banco el mismo día a pedir un crédito. La primera es una empresa grande, conocida, con cuentas abiertas en esa entidad desde hace años y un gerente que almuerza con el director. La segunda es Juan, con un proyecto sólido —ha hecho los números, el negocio se sostiene— pero sin más respaldo que su trabajo y una idea buena. Usted ya sabe cómo termina la historia: a la empresa le aprueban el crédito esa misma semana, a una tasa baja; a Juan le piden garantías que no tiene, le ofrecen una tasa más alta, o simplemente le dicen que no. Y aquí está lo que importa: no es porque el proyecto de Juan sea peor. Es porque Juan está lejos, y la empresa está cerca.'),

    '¿Cerca de qué? De la fuente del dinero. Y para entender qué significa eso —y por qué decide quién prospera y quién no en una economía entera— hay que mirar de frente algo que casi todos malentienden: de dónde sale, en realidad, el dinero que el banco presta.',

    'La creencia común es que el banco es un intermediario: recoge los ahorros de unos y se los presta a otros, como un puente entre el que guarda y el que necesita. Si así fuera, el banco solo podría prestar lo que alguien ahorró de verdad, y este capítulo no existiría. Pero no es así, y lo vimos al principio del libro: el banco no presta el ahorro que tiene; presta dinero que crea en el momento de prestar. Bajo reserva fraccionaria, por cada peso que de verdad guarda, presta varios que no existían hasta que firmó el préstamo. El banco comercial no mueve dinero ajeno: fabrica dinero nuevo.',

    'Y aquí hay que detenerse en algo que cambia toda la lógica del negocio bancario, porque es la raíz de lo que sigue. Cuando un banco presta dinero que fabrica, el solo acto de prestarlo ya es su ganancia —antes y al margen de que el proyecto rinda—. Rothbard lo dice sin anestesia:',

    ("quote",
     'las grandes ganancias que se originan en la inflación provienen de que el que emite pone en circulación nuevo dinero. Prácticamente todo es ganancia, puesto que, mientras todas las demás personas tienen que o bien vender bienes y servicios o extraer oro, el gobierno y los bancos comerciales literalmente crean dinero de la nada. No tienen que comprarlo. Toda utilidad que se obtenga con el uso de ese dinero mágico es una clara ganancia para los que lo emiten.',
     'Rothbard, <em>El hombre, la economía y el Estado</em>, cap. 12'),

    'Guarde esa frase —“dinero mágico”, “prácticamente todo es ganancia”—, porque es la llave de por qué Juan pierde. Un banco que vive de fabricar dinero no vive de acertar con los proyectos. Vive de emitir.',

    'Esto cambia por completo quién es el protagonista de esta historia. Solemos imaginar que la fábrica del dinero es el banco central —el edificio imponente, el comité, la imprenta—. Y es verdad que el banco central está en el origen: pone la base, respalda el sistema, rescata a quien tropieza, coordina a todos para que inflen al mismo ritmo. Pero el que de verdad crea la mayor parte del dinero nuevo, el que lo fabrica peso a peso cada vez que aprueba un préstamo, es el banco comercial —el de la esquina, el de la fila donde están Juan y la empresa—. El banco central habilita y respalda; los bancos comerciales fabrican. Están enchufados a él —por eso pueden crear sin miedo, sabiendo que si fallan habrá quien los sostenga—, pero son ellos los que están en la cabeza de la cadena: la mano que abre el grifo del dinero nuevo, y que decide hacia dónde corre.',

    'Y ese “hacia dónde” es todo el asunto. Pero antes de seguirlo, hay que responder la pregunta que la fila del principio dejó en el aire y que casi nunca se responde de verdad: ¿por qué el banco elige a la empresa y no a Juan? Decir “porque la empresa está cerca” no explica nada —cerca era justo lo que había que entender—. Así que mirémoslo de frente.',

    'Empecemos por lo que sí entendemos de cualquier banco, fabrique dinero o no. Póngase en la silla del banquero: tiene enfrente dos carpetas. La de la empresa la conoce de memoria —años de cuentas, un historial que lee de un vistazo—; la de Juan está casi en blanco, una idea y un nombre que nunca vio. La empresa trae con qué responder: activos embargables si algo falla. Juan trae su trabajo y una promesa. La empresa pide un préstamo grande, de una firma, que deja buena comisión; Juan pide uno pequeño, uno entre cien que habría que estudiar uno por uno. Y a la empresa la respalda alguien adentro: el gerente que almuerza con el director. Juan es una carpeta más en la pila.',

    'Ahí está, sin misterio, qué significa “estar cerca”: la empresa es el cliente cómodo —conocido, con respaldo, grande, con quien la defienda—, y Juan es el trabajo difícil. Cuatro razones concretas, ninguna inventada, todas humanas. Y aquí viene lo decisivo: esas cuatro razones no cambian con el tipo de dinero. Con dinero honesto o con dinero fabricado, la empresa sigue siendo igual de conocida, igual de grande, igual de respaldada. El dinero no toca ninguna de las cuatro. Un banco que prestara oro de verdad también las tendría enfrente. De modo que si el problema fuera solo que la empresa es más cómoda, no habría capítulo: la comodidad pesa lo mismo siempre.',

    'Imagine entonces una balanza. De un lado, el peso de la empresa: las cuatro comodidades, que pesan igual en cualquier mundo. Del otro lado, lo único que puede inclinar la decisión hacia Juan: el premio de descubrir un buen proyecto y el castigo de dejarlo escapar. Toda la diferencia entre un sistema sano y uno corrompido está en ese segundo lado —no en el de la empresa, que no se mueve, sino en el de Juan, que se carga o se vacía según de dónde salga el dinero—.',

    'Con dinero honesto —el que no se puede fabricar—, ese lado pesa, y pesa mucho. El banco presta un ahorro real, escaso, que alguien produjo y le confió; si lo coloca mal, lo pierde, y duele. Su ganancia entera depende de una sola cosa: que el proyecto al que prestó de verdad rinda. No hay otra forma de ganar. Y por eso Mises insiste en que quien arriesga su patrimonio no se refugia en lo cómodo, sino que persigue el mayor rendimiento:',

    ("quote",
     'Ninguna inversión es segura. Si los empresarios procedieran como la fábula del riesgo supone y buscaran siempre las inversiones seguras, su propio actuar las transformaría en inseguras. […] El capitalista nunca busca la inversión menos arriesgada. Persigue, por el contrario, aquella que, dadas las circunstancias, estima que ha de proporcionarle el mayor beneficio neto.',
     'Mises, <em>La Acción Humana</em>, cap. XV, secc. 9'),

    'Ese premio y ese castigo son un contrapeso feroz: obligan al banco a hacer el trabajo difícil, a abrir la carpeta de Juan, a estudiar al desconocido a pesar de que las cuatro comodidades empujan para el otro lado. Las comodidades siguen ahí —nadie las quita—, pero el banco tiene que vencerlas con esfuerzo, porque su única fuente de ganancia es acertar. La balanza puede inclinarse hacia Juan. Y se inclina cada vez que su proyecto, mirado con cuidado, resulta el mejor. El crédito encuentra al capaz aunque sea desconocido, porque al banco le conviene encontrarlo.',

    'Cuando el dinero se fabrica, ese lado de la balanza se vacía. Y aquí está la clave, la que tardamos en ver: no se vacía porque la empresa pese más —pesa igual—, sino porque el banco ya no necesita acertar para ganar. Su ganancia, recuerde la frase de Rothbard, viene del solo hecho de emitir: el dinero mágico que fabrica con la firma ya es utilidad. Acertar con el proyecto deja de ser su negocio. Y si acertar deja de ser el negocio, el premio de descubrir a Juan y el castigo de dejarlo pasar —lo único que cargaba ese lado de la balanza— se apagan. Una balanza con un solo lado cargado no es una balanza: es una caída. Las cuatro comodidades ganan, no porque hayan crecido, sino porque se quedaron sin rival. El banco le presta a la empresa no porque la sopesó contra Juan y ganó, sino porque ya nada lo obliga a sopesar.',

    'Detengámonos en lo que está en juego, porque es una señal más, de las que venimos siguiendo todo el libro. El crédito, bien entendido, es una de las señales más importantes de una economía: dice hacia dónde debe fluir el capital —qué proyectos merecen recursos, cuáles no—. En un sistema honesto, donde solo se presta lo ahorrado, esa señal funciona: el ahorro fluye hacia quien promete devolverlo con el mayor rendimiento, es decir, hacia donde será más productivo. El crédito dirige el capital de la sociedad hacia sus mejores usos, como una brújula que apunta al proyecto que más vale la pena. No importa si usted tiene padrinos: importa si su proyecto es bueno.',

    'Cuando el dinero se fabrica, esa brújula se desvía. El crédito ya no fluye hacia el mejor proyecto, sino hacia el más cercano a quien fabrica el dinero. Y la cercanía da una doble ventaja, porque —como vimos al hablar de los precios— el que recibe el dinero nuevo primero lo recibe cuando todavía vale, antes de que los precios suban. Rothbard nombra a los beneficiarios sin rodeos:',

    ("quote",
     'los prestatarios del banco, comerciantes o consumidores —su clientela—, se benefician con el nuevo dinero (por lo menos a corto plazo), ya que son quienes primero lo reciben.',
     'Rothbard, <em>El hombre, la economía y el Estado</em>, cap. 12'),

    'Su clientela: los de adentro. El de adentro recibe dinero fresco y barato para comprar el mundo a precios de ayer; el de afuera, si acaso recibe algo, lo recibe tarde, caro y devaluado. La señal que debía decir “este negocio es productivo” pasa a decir “este cliente es de los nuestros”. Y los Juanes —los que tienen buenas ideas pero no padrinos— quedan compitiendo en desventaja contra los de adentro, no porque sus proyectos sean peores, sino porque no están enchufados a la fuente.',

    'Aquí conviene apoyarse en una distinción que popularizó Milton Friedman —que no era de esta tradición, sino más bien un adversario de ella, lo que vuelve aún más revelador que su esquema ilumine tan bien el problema—. Friedman observó que hay cuatro maneras de gastar dinero, y que el cuidado con que se gasta depende de dos cosas: de quién es el dinero, y para quién es lo que se compra. Cuando uno gasta su dinero en sí mismo, cuida las dos puntas: que sea bueno y que no cueste de más. Cuando gasta su dinero en otro —un regalo—, cuida el precio pero afloja en la calidad. Cuando gasta el dinero de otro en sí mismo —una cena con cuenta ajena—, cuida la calidad pero no el precio. Y cuando gasta el dinero de otro en un tercero, no cuida ninguna de las dos: ni el precio, porque no es suyo, ni la calidad, porque no es para él. Es el cuadrante de la indiferencia total —y es, ni más ni menos, cómo se gasta el dinero de los impuestos—.',

    'Esa cuarta casilla es, exactamente, el lado vacío de la balanza con un nombre. Pregúntese de quién es el dinero que el banco reparte, y para quién: no es suyo —lo fabricó, no lo ahorró— y no es para él —es para el cliente—. Dinero ajeno gastado en un tercero: el cuadrante de la indiferencia. Y la indiferencia no es un defecto de carácter del banquero —no es que sea malo o perezoso por naturaleza—; es la posición estructural en la que lo pone el dinero fabricado. Quien no arriesga lo suyo y no necesita acertar para ganar no tiene, del otro lado de la balanza, nada que lo obligue a mirar bien. Por eso se queda con lo cómodo.',

    'Y hay un agravante contemporáneo que conviene marcar como lo que es —una extensión del argumento, no algo que Rothbard desarrollara en su tiempo, aunque él mismo dejó la semilla—. Hoy el banco que falla no siempre paga su error: existe un prestamista de última instancia, hay rescates, hay seguro de depósitos. El propio Rothbard advirtió, en una nota de este mismo capítulo, que desde la aparición del seguro de depósitos el freno natural a la imprudencia bancaria se debilita. Lleve esa observación a sus últimas consecuencias y verá que el incentivo a evaluar bien no solo se apaga porque el banco gane por emitir, sino que se apaga doblemente porque tampoco carga del todo con las pérdidas cuando se equivoca. Es el mismo diagnóstico, agravado por la red estatal moderna: si fabricar dinero ya quitaba la razón para buscar a Juan, la garantía de rescate remata lo que quedaba de prudencia.',

    'Esto responde, de paso, la objeción más seria que admite el capítulo —la que un lector con formación financiera tendría en la punta de la lengua—. “Un momento: ¿no es simplemente que prestarle a la empresa grande es menos riesgoso? Tiene activos, historial, con qué responder; Juan es un desconocido. Cualquier banco prudente prefiere al cliente seguro. Eso no es privilegio: es buena gestión del riesgo.” La objeción es legítima, y hay que concederla: evaluar el riesgo es sensato, y un banco honesto también prestaría con más cuidado a quien no tiene cómo responder. Pero fíjese en lo que la objeción da por sentado: un banquero prudente que arriesga lo propio. Ese banquero es precisamente el que el dinero honesto produce —el que, como no gana sino acertando, escarba hasta descubrir si Juan rinde— y el que el dinero fabricado destruye —el que, como gana por emitir y no paga del todo sus errores, se queda con el atajo cómodo—. “Prestarle al de siempre” no es la conclusión de un análisis cuidadoso del riesgo: es lo que queda cuando ya nada obliga a hacerlo.',

    'Hay todavía una vuelta de tuerca, por si quedara duda. ¿De dónde salieron los activos que vuelven “tan segura” a la empresa grande? En buena parte, de haber estado cerca del dinero nuevo antes: compró barato, con crédito previo, lo que hoy vale más y le sirve de colateral. Su menor riesgo no es un dato caído del cielo —es, en parte, el premio acumulado de privilegios anteriores—. El sistema fabrica el colateral que luego invoca para justificar prestarle más al mismo. De modo que “es menos riesgoso” no siempre describe un mérito: a veces describe la ventaja heredada de quien lleva tiempo cerca del grifo.',

    'Y esto no es un episodio aislado: es un sesgo que se repite en cada ciclo de crédito, año tras año, y por eso sus efectos se acumulan. Cada vez que se fabrica dinero, los de adentro reciben primero y se afianzan; los de afuera quedan un paso atrás. El que ya tenía acceso al crédito barato crece, compra, se expande; el que no, se queda. Con el tiempo, la economía no se organiza según quién produce mejor, sino según quién estuvo más cerca de la fuente del dinero. El capital deja de fluir hacia el mérito y fluye hacia el privilegio —y como el privilegio, una vez ganado, compra más privilegio, la distancia entre los de adentro y los de afuera se ensancha sola—. No es que el sistema falle en repartir bien: es que reparte exactamente según la cercanía al grifo, una y otra vez, hasta que la estructura entera de la economía lleva impresa la huella de quién tenía acceso al dinero nuevo y quién no.',

    'Y como siempre, todo esto depende de una sola cosa. Con dinero honesto —el que no se puede fabricar— el banco no tiene un grifo que abrir: solo puede prestar lo que alguien ahorró de verdad, y eso lo obliga a la disciplina. Cada préstamo arriesga un ahorro real, y como su única ganancia es acertar, conviene dirigirlo al mejor proyecto, no al amigo. La cercanía no da ninguna ventaja, porque no hay dinero nuevo que repartir antes que nadie: hay un ahorro escaso que hay que colocar bien. El crédito vuelve a fluir hacia el mérito, porque es la única forma de ganar. El reparto por cercanía no es un abuso que un buen banquero evitaría por decencia: es una posibilidad que solo existe cuando se puede fabricar dinero. Quítele al banco el grifo, y la fila del comienzo se ordena sola por la calidad de los proyectos, no por la cercanía de los clientes.',

    'Recoja la forma, que es la de siempre. La causa sigue siendo la misma raíz de todo el libro: el ahorro real, lo que una sociedad de verdad guardó para invertir. La señal de este capítulo es el crédito —hacia dónde fluye el capital—. El que la lee es el banco, que decide a quién prestar. Y el desenlace depende del dinero: si es honesto, el crédito fluye al mérito y la sociedad invierte en lo que de verdad rinde; si se fabrica, el crédito fluye al privilegio, y la economía se reorganiza alrededor de quién está cerca de la fuente, no de quién produce mejor. Una sociedad que reparte el crédito por cercanía termina premiando a los enchufados y castigando a los capaces —y lo hace en silencio, préstamo a préstamo, hasta que parece el orden natural de las cosas—.',

    'Hemos visto al dinero falso corromper señal tras señal: la tasa, la estructura productiva, las pérdidas, los precios, el cálculo a futuro, el ahorro guardado, y ahora el reparto del crédito. En todos los casos hubo algo que nos permitió ver el daño: pudimos rastrearlo, nombrarlo, seguir el hilo desde la fuente hasta la consecuencia. Pero eso fue posible solo porque, de algún modo, la información estaba ahí para quien supiera mirar. ¿Y si el propio dinero pudiera esconder sus movimientos? ¿Si fuera imposible saber cuánto se ha creado, o quién lo tiene, o si las cuentas cuadran? Esa es la pieza que sostiene a todas las demás —la posibilidad misma de auditar el dinero, de verificar que no nos engañan—, y es la que cierra este recorrido.',
]

# CSS de la cita: bloque alineado a la izquierda, sobrio (filete fino gris,
# cursiva serif, atribución gris). El tratamiento clásico de cita; NO centrado.
EXTRA_CSS = """
/* ===== Citas en bloque — alineadas a la izquierda, sobrias (filete fino) ===== */
.prose .pull-quote {
  margin: 2.4rem 0; padding: 0.3rem 0 0.3rem 1.5rem;
  border-left: 2px solid var(--rule);
}
.prose .pull-quote p {
  font-size: 1.06rem; font-style: italic; line-height: 1.7; color: var(--ink); margin: 0 0 0.7rem;
}
.prose .pull-quote cite {
  display: block; font-style: italic; font-size: 0.88rem; line-height: 1.5; color: var(--ink-soft);
}
"""

# ---- Construir el HTML del article ----
parts = ['<article class="page">\n',
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

# ---- Esqueleto del cap 3 ----
sk = open('tres-regimenes.html', encoding='utf-8').read()
out = sk
out = re.sub(r'<title>.*?</title>',
             '<title>La asignación del crédito — Arregla el dinero, arregla el mundo</title>',
             out, count=1, flags=re.DOTALL)
out = re.sub(r'<article class="page">.*?</article>', lambda _m: article, out, count=1, flags=re.DOTALL)
new_nav = ('<nav class="nav-foot">'
           '<a class="prev" href="poder-adquisitivo.html">El poder adquisitivo del dinero</a>'
           '<a class="idx" href="index.html">Índice</a>'
           '<a class="next" href="auditabilidad.html">La auditabilidad del dinero</a></nav>')
out = re.sub(r'<nav class="nav-foot">.*?</nav>', lambda _m: new_nav, out, count=1, flags=re.DOTALL)
out = out.replace('</style>', EXTRA_CSS + '</style>', 1)
out = out.replace('audio/tres-regimenes.mp3', 'audio/asignacion-credito.mp3')
out = out.replace('audio/tres-regimenes.alignment.json', 'audio/asignacion-credito.alignment.json')
out = out.replace('data-storage-key="tres-regimenes"', 'data-storage-key="asignacion-credito"')

open('asignacion-credito.html', 'w', encoding='utf-8').write(out)
n_par = sum(1 for it in CONTENT if isinstance(it, str) or it[0] == "lead")
n_q = sum(1 for it in CONTENT if isinstance(it, tuple) and it[0] == "quote")
print("asignacion-credito.html creado")
print(f"párrafos narrados: {n_par} | citas: {n_q}")
