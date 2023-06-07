from colors import *
class Picture:
  def __init__(self, img):
    self.img = img;
def horizontalMirror(self):
    """ Devuelve el espejo horizontal de la imagen """
    horizontal = self.img[::-1]
    return Picture(horizontal)


def negative(self):
    """ Devuelve un negativo de la imagen """
    neg = []
    for fila in self.img:
        cadena = ""
        for color in fila:
            cadena += self._invColor(color)
        neg.append(cadena)
    return Picture(neg)