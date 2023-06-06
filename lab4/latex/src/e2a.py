from interpreter import draw
from chessPictures import *

draw(knight.join(knight.negative()).under(knight.negative().join(knight)))