from colors import *
class Picture:
  def __init__(self, img):
    self.img = img;
  def horizontalRepeat(self, n):
    """ Devuelve una nueva figura repitiendo la figura actual al costado
        la cantidad de veces que indique el valor de n """
    return  Picture(self*n)

  def verticalRepeat(self, n):
    repet = []
    for i in range(len(self.img)):
      repet.append(self.img[i]*n)
    return Picture(repet)