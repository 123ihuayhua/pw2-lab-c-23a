function carga(){
    for (var i = 0; i < 10; i++) {
        document.getElementById(i).innerHTML = i
    }
    document.getElementById("del").innerHTML = "<="
}
function teclear(i){
    var num =document.getElementById(i).innerText
    document.getElementById("resultado").value += num
}
function par(i){
    if(i==0){
        document.getElementById("resultado").value += "("
    }else{
        document.getElementById("resultado").value += ")"
    }
}
function calcular(){
    let resul = eval(document.getElementById("resultado").value)
    document.getElementById("resultado").value = resul
}
function agregar(simbolo){
    var op = document.getElementById("resultado").value
    if(simbolo=="("|simbolo==")"|simbolo=="*"){
        document.getElementById("resultado").value += simbolo
    }else{
        if(op.charAt(op.length-1)!=simbolo){
            document.getElementById("resultado").value += simbolo
        }
    }
}
function del(){
    var op = document.getElementById("resultado").value+""
    console.log(op)
    var cadena = op.substring(0,op.length-1)

    document.getElementById("resultado").value = cadena
}