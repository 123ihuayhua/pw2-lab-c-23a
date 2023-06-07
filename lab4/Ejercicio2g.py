from interpreter import draw
from chessPictures import *
derecha = square.up(rock).join(square.negative().up(knight)).join(square.up(bishop))
#centro = (square.up(queen)).join(square.up(king))
izquierda = derecha.verticalMirror()
peonesBlancos = (square.up(pawn).join(square.negative().up(pawn))).verticalRepeat(4)
pNegros = peonesBlancos.negative()
medio = (((square.join(square.negative())).verticalRepeat(4)).under((square.negative().join(square)).verticalRepeat(4))).horizontalRepeat(2)
#draw(pNegros.under(medio).under(peonesBlancos))
#fila = derecha.join(izquierda)
draw(derecha)