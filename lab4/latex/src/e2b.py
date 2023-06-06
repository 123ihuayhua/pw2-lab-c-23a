from interpreter import draw
from chessPictures import *

draw(knight.join(knight.negative()).under(knight.negative().verticalMirror().join(knight.verticalMirror())))