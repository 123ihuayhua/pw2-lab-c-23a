console.log("ingrese a script")
document.addEventListener('DOMContentLoaded', function () {
    const titulo = document.querySelector('#title')
    const desc = document.querySelector('#desc')
    /*document.querySelector('#form').onsubmit = () => {
        enviarDatos(titulo.value)
        enviarDatos(desc.value)
        const title = titulo.value
        const descrip = desc.value
      const eventData = {i:title,j:descrip}
      console.log(eventData)
      /*fetch('/eventos', {
        mode:"cors",
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(eventData)
      })
        .then(response => {
            if (response.ok) {
                // La solicitud se completó correctamente
                console.log('Evento creado exitosamente');
              } else {
                // Ocurrió un error al crear el evento
                console.error('Error al crear el evento');
              }
            })
            .catch((error) => {
              console.error(error);
            });
        return false;
    }*/
    
})
function enviarDatos(texto){
        console.log(texto)
    }

function mostrar(){
    console.log("hola")
    const url = 'http://localhost:3000/agenda'
    fetch(url).then(
        response => response.json()
    ).then(
        data => {
            console.log(data.text)
            document.querySelector("#prueba").innerHTML = data.text
        }
    )
}