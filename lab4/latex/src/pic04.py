from colors import *
class Picture:
  def __init__(self, img):
    self.img = img;
  def up(self, p):
    sobre = []
    for i in range(len(self.img)):
      linea = []
      for j in range(len(self.img[i])):
        if p.img[i][j] != ' ':
          linea.append(p.img[i][j])
        else:
          linea.append(self.img[i][j])
      sobre.append(linea)
    return Picture(sobre)