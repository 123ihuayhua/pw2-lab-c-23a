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

app.get('/agenda', (request, response) => {
    fs.readFile(path.resolve(__dirname, 'agenda/poema.txt'), 'utf8',
        (err, data) => {
            if (err) {
                console.error(err)
                response.status(500).json({
                    error: 'message'
                })
                return
            }
            response.json({
                text: data.replace(/\n/g, '<br>')
            })
        })
    //
})
const eventos = path.join(__dirname, 'eventos');
app.post('/eventos/', (request, res) => {
    console.log(request.body)
    const {title,desc,fecha,hora} = request.body
    const filePath = path.join(eventos,fecha, `${hora}.txt`);
    const texto = title+"\n\n"+desc
    console.log(title)
    console.log(desc)
    fs.access(filePath, fs.constants.F_OK, (err) => {
        if (err) {
          const content = `${title}\n${texto}`;
          fs.mkdir(path.join(eventos, fecha), { recursive: true }, (err) => {
            if (err) {
              res.status(500).json({ error: 'Failed to create event.' });
            } else {
              fs.writeFile(filePath, content, (err) => {
                if (err) {
                  res.status(500).json({ error: 'Failed to create event.' });
                } else {
                  res.sendStatus(200);
                }
              });
            }
          });
        } else {
          res.status(409).json({ error: 'Event already exists.' });
        }
      });
    /*fs.writeFile(filePath, texto, function (err) {
        if (err) throw err;
        console.log('Saved!');
    });*/
})