const express = require('express');
const mongoose = require('mongoose');
const winston = require('winston');
const path = require('path');

const app = express();
const port = 5000;

// Configuración del logger
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.simple(),
  transports: [
    new winston.transports.File({ filename: path.join(__dirname, 'logs', 'app.log') })
  ]
});

// Rutas
app.get('/', (req, res) => {
  const msg = "Hola mundo desde Express!";
  logger.info(msg);
  res.send(msg);
});

app.get('/error', (req, res) => {
  const msg = "Error!";
  logger.error(msg);
  res.send(msg);
});

// Iniciar el servidor
app.listen(port, '0.0.0.0', () => {
  console.log(`Servidor escuchando en http://0.0.0.0:${port}`);
});