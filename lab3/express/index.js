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
app.post('/eventos', (request, response) => {
    console.log(request.body)
    const {i, j} = request.body
    
    console.log(i)
    console.log(j)
    /*fs.writeFile('./eventos/mynewfile1.txt', 'desc', function (err) {
        if (err) throw err;
        console.log('Saved!');
    });*/
})