const fs = require('fs')
const path = require('path')
const express = require('express')
const cors = require('cors');
const app = express()
const bp = require('body-parser')
app.use(cors());
app.use(express.static('./'))

app.use(bp.urlencoded({
    extended: true
}))
app.use(express.urlencoded({
    extended : false
}))
app.listen(3000, () => {
    console.log("Escuchando en: http://localhost:3000")
});

app.get('/', (request, response) => {
    response.sendFile(path.resolve(__dirname, 'index.html'))
})
app.get('/borrar', (request, response) => {
  response.sendFile(path.resolve(__dirname, 'index.html'))
})
const agenda = path.join(__dirname, 'agenda');
var diaDir
app.post('/borrar', (request, response) => {
  console.log(request.body)
  const { date,time } = request.body;
  diaDir =  path.join(agenda, date);
  const filePath = path.join(diaDir,`${time}.txt`);
  fs.unlink(filePath, (err) => {
    if (err) {
      response.sendFile(path.resolve(__dirname, 'index.html'))
    } else {
      response.sendFile(path.resolve(__dirname, 'index.html'))
    }
  });  
});
function eliminar(dir){
  fs.readdir(dir, (err, files) => {
    if (err) {
      console.log(err);
    } else {
      console.log(files)
      if (files==''||files.length == 0) {//si cumple elimina
        console.log('La carpeta está vacía'+files.length);
        fs.rmdir(dir,{ recursive: true }, (err) => {
          if (err) {
            console.error(err);
          } else {
            console.log('La carpeta ha sido eliminada');
          }
        });
      } else {
        console.log('La carpeta no está vacía');
      }
    }
  });
}
app.post('/editar', (request, response) => {
  console.log(request.body)
  const { date,time,desc } = request.body;
  const filePath2 = path.join(agenda, date,`${time}.txt`);

  fs.writeFile(filePath2, desc, function (err) {
    if (err) throw err;
    console.log('Reemplazo orrecto!');
    response.sendFile(path.resolve(__dirname, 'index.html'))
  });
});
app.post('/eventos/', (request, response) => {
    console.log(request.body)
    const {desc,fecha,hora} = request.body
    console.log(hora)
    //9:9 -9-9
    const hora2 = hora.replace(':','-')
    console.log(hora2)
    const filePath = path.join(agenda, fecha,`${hora2}.txt`);
    if(desc != ''){
    fs.access(filePath, fs.constants.F_OK, (err) => {
        if (err) {
          const content = desc;
          fs.mkdir(path.join(agenda, fecha), { recursive: true }, (err) => {
            if (err) {
              response.sendFile(path.resolve(__dirname, 'index.html'))
              //res.status(500).json({ error: 'Falla al crear evento' });
            } else {
              fs.writeFile(filePath, content, (err) => {
                if (err) {
                  response.sendFile(path.resolve(__dirname, 'index.html'))
                  //res.status(500).json({ error: 'Falla al crear evento' });
                } else {
                  response.sendFile(path.resolve(__dirname, 'index.html'))
                  //res.sendStatus(200);
                }
              });
            }
          });
        } else {
          response.sendFile(path.resolve(__dirname, 'index.html'))
          //res.status(409).json({ error: 'Evento ya existe' });
        }
      });
    }else response.sendFile(path.resolve(__dirname, 'index.html'))
})
app.get('/eventos', (req, res) => {
  if(diaDir){
    eliminar(diaDir)
  }
  const agenda = readAgenda();
  res.json(agenda);
  });
function readAgenda() {
    const agendaArr = [];
    fs.readdirSync(agenda).forEach((date) => {
      const datePath = path.join(agenda, date);
      const events = fs.readdirSync(datePath).map((file) => {
        const time = path.basename(file, '.txt');
        const filePath = path.join(datePath, file);
        const text = fs.readFileSync(filePath, 'utf8');
        return { time, text };
      });
      agendaArr.push({ date, events });
    });
    return agendaArr;
  }
  