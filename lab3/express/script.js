var seMuestaEventos = false
document.querySelector('#formCrear').onsubmit = () => {
  const desc = document.getElementById('desc').value
  const fecha = document.getElementById('fecha').value
  const hora = document.getElementById('hora').value
  agregar(desc,fecha,hora)
  document.querySelector('#formCrear').reset();
  if(seMuestaEventos){mostrar()}
  return false;
}
function agregar(desc, fecha, hora){
  const url = 'http://localhost:3000/eventos'
  const data = {
    desc: desc,
    fecha: fecha,
    hora: hora
  }
  const request = {
      method: 'POST', // Podría ser GET
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
  }
    fetch(url, request)
    .then(response => response.json())
    .then(data2 => {
      print(data2.text)
    })
    .catch(error => {
      console.error('Error:', error);
    });
}
var i =0
function mostrar() {
  i=0
  seMuestaEventos = true
  resetear()
    const url = 'http://localhost:3000/eventos';
    fetch(url, { mode: 'cors' })
      .then(response => response.json())
      .then(data => {
        const agenda = data;
        let html = '';    
        agenda.forEach(item => {
          html += `<h3>${item.date}</h3>`;
          html += '<ul>';
          item.events.forEach(event => {
              const salto = event.text.indexOf("\n")
              var titulo
              let descrip
              if(salto != -1){  
                titulo = event.text.substring(0,salto)
                descrip = event.text.substring(salto+1, event.text.length)
              }else{
                 titulo = event.text
                 descrip = 'No hay descripcion'
                } 
              descrip = descrip.replace(/\n/g,"<br>")
              const texto = event.text.replace(/\n/g,"<br>")
              i++
            html += `<form id="formBorrar${i}">
              <input type="button" value="${titulo}" onclick="print('${descrip}')">
              <input type="hidden"  id="date${i}" value="${item.date}">
              <input type="hidden" id="time${i}" value="${event.time}">
              <input type="button" value="editar" onclick="cargarEditor('${item.date}','${event.time}','${texto}')">
              <input type= "submit" value="eliminar"
              style="background-color: red;
              color: white;
              padding: 10px 20px;
              border: none;
              cursor: pointer;">
          </form><br>`//editar
          });
          html += '</ul>';
        });
        document.querySelector("#show").innerHTML = html;
        if(i!=0){sePuedeBorrar();}
        else{print("No hay eventos")}
      });
  }
  function sePuedeBorrar(){
      for (let index = 1; index <= i; index++) {
        let nombre = '#formBorrar'+index
        document.querySelector(nombre).onsubmit = () => {
          eliminar(i)
          return false;
        }
      }
  }
function print(texto){
    document.querySelector("#editar").innerHTML = texto;
}
function resetear(){
  document.querySelector("#editar").innerHTML = '';
}
function cargarEditor(date, time,texto){
    texto = texto.replace(/<br>/g,"\r\n")
    html = `<form id="formEditar">
            <input type="hidden"  id="dateE" value="${date}">
            <input type="hidden" id="timeE" value="${time}">
            <textarea id="descE" cols="30" rows="10" required>${texto}</textarea><br>
            <input type= "submit" value="confirmar">
        </form>`
        document.querySelector("#editar").innerHTML = html;
        cargoEditor();
        return false;
}//editar
function cargoEditor(){
document.querySelector('#formEditar').onsubmit = () => {
  const date = document.getElementById('dateE').value
  const time = document.getElementById('timeE').value
  const desc2 = document.getElementById('descE').value
  editar(date,time,desc2)
  mostrar()
  document.querySelector("#editar").innerHTML = '';
  return false;
}}//borrar
function eliminar(i){
  const date = document.getElementById('date'+i).value
  const time = document.getElementById('time'+i).value
  borrar(date,time)
  mostrar()
  return false;
}
function borrar(date,time){
  const url = 'http://localhost:3000/borrar'
  const data = {
    date: date,
    time:time
  }
  const request = {
      method: 'POST', // Podría ser GET
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
  }
    fetch(url, request)
    .then(response => response.json())
    .then(data2 => {
      document.querySelector("#editar").innerHTML = data2.text;
    });
}
  function editar(date,time,desc){
  const url = 'http://localhost:3000/editar'
  const data = {
    date: date,
    time:time,
    desc: desc
  }
  const request = {
      method: 'POST', // Podría ser GET
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
  }
    fetch(url, request)
    .then(response => response.json())
    .then(data2 => {
      //document.querySelector("#show").innerHTML = data2.text;
      print(data2.text)
    });
}
