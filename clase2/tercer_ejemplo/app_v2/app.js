const express = require('express');
const mongoose = require('mongoose');
const winston = require('winston');
const path = require('path');

const app = express();
const port = 7000;

// Configuración del logger
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.simple(),
  transports: [
    new winston.transports.File({ filename: path.join(__dirname, 'logs', 'app.log') })
  ]
});

const logger_v2 = winston.createLogger({
  level: 'info',
  format: winston.format.simple(),
  transports: [
    new winston.transports.File({ filename: path.join(__dirname, 'logs', 'app_v2.log') })
  ]
});

// Conexión a MongoDB
mongoose.connect('mongodb://mongodb:27017/myapp', { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('Conectado a MongoDB'))
  .catch(err => {
    console.error('Error de conexión a MongoDB:', err);
    process.exit(1);
});

// Esquema y modelo para los logs
const logSchema = new mongoose.Schema({
  message: String,
  level: String,
  randomNumber: Number,
  timestamp: { type: Date, default: Date.now }
});

const Log = mongoose.model('Log', logSchema);

// Rutas
app.get('/', (req, res) => {
  const msg = "Hola desde la segunda aplicación!";
  logger.info(msg);
  res.send(msg);
});

app.get('/v2', (req, res) => {
  const msg = "Hola desde la segunda aplicación versión 2!";
  logger_v2.info(msg);
  res.send(msg);
});

app.get('/error', (req, res) => {
  const msg = "Error!";
  logger.error(msg);
  res.send(msg);
});

app.get('/add-random-log', async (req, res) => {
  try {
    const randomNumber = Math.floor(Math.random() * 100);
    const levels = ['info', 'warn', 'error'];
    const randomLevel = levels[Math.floor(Math.random() * levels.length)];
    
    const newLog = new Log({
      message: `Log aleatorio número ${randomNumber}`,
      level: randomLevel,
      randomNumber: randomNumber
    });

    await newLog.save();

    const logMessage = `Log aleatorio añadido: ${newLog.message}, Nivel: ${newLog.level}, Número: ${newLog.randomNumber}`;
    logger.info(logMessage);
    
    res.send(logMessage);
  } catch (error) {
    const errorMessage = `Error al añadir log aleatorio: ${error.message}`;
    logger.error(errorMessage);
    res.status(500).send(errorMessage);
  }
});

// Endpoint para obtener los últimos logs
app.get('/logs', async (req, res) => {
  try {
    const logs = await Log.find().sort({ timestamp: -1 }).limit(10);
    logger.info('Consultados los últimos 10 logs de MongoDB');
    res.json(logs);
  } catch (error) {
    const errorMessage = `Error al consultar logs de MongoDB: ${error.message}`;
    logger.error(errorMessage);
    res.status(500).send(errorMessage);
  }
});

// Iniciar el servidor
app.listen(port, '0.0.0.0', () => {
  console.log(`Servidor escuchando en http://0.0.0.0:${port}`);
});