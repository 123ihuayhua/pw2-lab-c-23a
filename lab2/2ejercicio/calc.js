let memorias = []
let answer
let guardando = true
function carga(){
    for (var i = 0; i < 10; i++) {
        document.getElementById(i).innerHTML = i
    }
    document.getElementById("del").innerHTML = "<="
    document.getElementById("del").setAttribute("style", "background-color: red;")
    document.getElementById("igual").setAttribute("style", "background-color: green;")
    document.getElementById("m1").setAttribute("style", "background-color: skyblue;")
    document.getElementById("m2").setAttribute("style", "background-color: skyblue;")
    document.getElementById("c").setAttribute("style", "background-color: orange;")
    document.getElementById("ans").setAttribute("style", "background-color: orange;")
}
function teclear(i){
    var num =document.getElementById(i).innerText
    document.getElementById("resultado").value += num
}
function calcular(){
    let resul = eval(document.getElementById("resultado").value)
    answer = resul
    document.getElementById("resultado").value = resul
}
function ans(){
    document.getElementById("resultado").value += answer
}
function agregar(simbolo){
    var op = document.getElementById("resultado").value
    if(simbolo=="("|simbolo==")"|simbolo=="*"){
        if(op.substring(op.length-2, op.length)!="**"){
            document.getElementById("resultado").value += simbolo
        }
    }else{
        if(op.charAt(op.length-1)!=simbolo){
            document.getElementById("resultado").value += simbolo
        }
    }
}
function limpiar() {
    actualInput = "";
    document.getElementById("resultado").value = "";
    
}
function memoria(i){
    if(guardando & !memorias[i]){
        memorias[i] =document.getElementById("resultado").value
        guardando=false
    }else{
        document.getElementById("resultado").value = memorias[i]
        memorias[i]=null
        guardando = true
    }
}
function del(){
    var op = document.getElementById("resultado").value+""
    console.log(op)
    var cadena = op.substring(0,op.length-1)
    document.getElementById("resultado").value = cadena
}