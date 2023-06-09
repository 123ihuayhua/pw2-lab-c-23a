from interpreter import draw
from chessPictures import *
derecha = square.negative().up(rock).join(square.up(knight)).join(square.negative().up(bishop))
centro = (square.up(queen)).join(square.negative().up(king))
izquierda = square.up(bishop).join(square.negative().up(knight)).join(square.up(rock))
filaAbajo = derecha.join(centro).join(izquierda)
filaArriba = filaAbajo.negative()
peonesBlancos = (square.up(pawn).join(square.negative().up(pawn))).verticalRepeat(4)
pNegros = peonesBlancos.negative()
superio = filaArriba.under(pNegros)
inferior = peonesBlancos.under(filaAbajo)
medio = (((square.join(square.negative())).verticalRepeat(4)).
        under((square.negative().join(square)).verticalRepeat(4))).horizontalRepeat(2)
draw(superio.under(medio).under(inferior))