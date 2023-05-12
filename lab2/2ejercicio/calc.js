function carga(){
    for (var i = 0; i < 10; i++) {
        document.getElementById(i).innerHTML = i
    }
}
function teclear(i){
    var num =document.getElementById("boton"+i).innerText
    document.getElementById("resultado").value += num
}