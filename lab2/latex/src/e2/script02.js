var numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
desorden(numeros)
function carga(){
    for (var i = 0; i < numeros.length; i++) {
        document.getElementById(i).innerHTML = numeros[i]
    }
}
function teclear(i){
    var num =document.getElementById("boton"+i).innerText
    document.getElementById("resultado").value += num
}
function desorden(arreglo) {
    var indexActual = arreglo.length;
    var aux, random;
    while (0 !== indexActual) {
  
      random = Math.floor(Math.random() * indexActual)
      indexActual--
  
      aux = arreglo[indexActual]
      arreglo[indexActual] = arreglo[random]
      arreglo[random] = aux
    }
    return arreglo
  }