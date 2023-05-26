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
const agenda = path.join(__dirname, 'agenda');
app.post('/borrar', (request, res) => {
  console.log(request.body)
  const { date,time } = request.body;
  const filePath2 = path.join(agenda, date,`${time}.txt`);

  fs.unlink(filePath2, (err) => {
    if (err) {
      res.status(500).json({ error: 'Error al borrar evento' });
    } else {
      res.sendStatus(200);
    }
  });
});
app.post('/eventos/', (request, res) => {
    console.log(request.body)
    const {title,desc,fecha,hora} = request.body
    const filePath = path.join(agenda, fecha,`${hora}.txt`);
    const texto = title+"\n\n"+desc
    console.log(title)
    console.log(desc)
    fs.access(filePath, fs.constants.F_OK, (err) => {
        if (err) {
          const content = texto;
          fs.mkdir(path.join(agenda, fecha), { recursive: true }, (err) => {
            if (err) {
              res.status(500).json({ error: 'Falla al crear evento' });
            } else {
              fs.writeFile(filePath, content, (err) => {
                if (err) {
                  res.status(500).json({ error: 'Falla al crear evento' });
                } else {
                  res.sendStatus(200);
                }
              });
            }
          });
        } else {
          res.status(409).json({ error: 'Evento ya existe' });
        }
      });
})
app.get('/eventos', (req, res) => {
    const agenda = readAgenda();
    res.json(agenda);
  });
  app.get('/delete', (req, res) => {
    res.sendFile(path.resolve(__dirname, 'index.html'))
});
function readAgenda() {
    const agendaArr = [];
    fs.readdirSync(agenda).forEach((date) => {
      const datePath = path.join(agenda, date);
      const events = fs.readdirSync(datePath).map((file) => {
        const time = path.basename(file, '.txt');
        return { time };
      });
      agendaArr.push({ date, events });
    });
    return agendaArr;
  }
  