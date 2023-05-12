var numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0];
function carga(){
    for (var i = 0; i < numeros.length; i++) {
        document.getElementById(i).innerHTML = numeros[i]
    }
}
function teclear(i){
    var num =document.getElementById("boton"+i).innerText
    console.log(num)
}

