const fs = require('fs')
const path = require('path')
const express = require('express')
app.use(express.static('./'))
app.listen(3000, () => {
    console.log("Escuchando en: http://localhost:3000")
});
const index = 'index.html'

app.get('/', (request, response) => {
    response.sendFile(path.resolve(__dirname, index))
})

