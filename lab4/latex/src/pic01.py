import colors
from colors import *

class Picture:
    def __init__(self, img):
        self.img = img;

    def __eq__(self, other):
        return self.img == other.img

    def _invColor(self, color):
        if color not in inverter:
            return color
        return inverter[color]

    def verticalMirror(self):
        """ Devuelve el espejo vertical de la imagen """
        vertical = []
        for value in self.img:
            vertical.append(value[::-1])
        return vertical

    def horizontalMirror(self):
        """ Devuelve el espejo horizontal de la imagen """
        horizontal = self.img[::-1]
        return horizontal

    def negative(self):
        """ Devuelve un negativo de la imagen """
        neg = []
        for fila in self.img:
            cadena = ""
            for color in fila:
                cadena += self._invColor(color)
            neg.append(cadena)
        return Picture(neg)

    def join(self, p):
        """ Devuelve una nueva figura poniendo la figura del argumento
            al lado derecho de la figura actual """
        juntos = []
        for i in range(len(self.img)):
            juntos.append(self.img[i] + p.img[i])
        return Picture(juntos)
    def under(self, p):
        """ Devuelve una nueva figura poniendo la figura p sobre la
                figura actual """
        return Picture(self.img[::] + p.img[::])
