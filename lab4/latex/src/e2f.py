from interpreter import draw
from chessPictures import *
draw((((square.join(square.negative())).verticalRepeat(4)).
      under((square.negative().join(square)).
            verticalRepeat(4))).horizontalRepeat(2))