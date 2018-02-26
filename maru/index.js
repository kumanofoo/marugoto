const bus = require('./bus');
const rubbish = require('./rubbish');
const express = require('express');
const app = express();
const serverPort = 8091;

app.post('/googlehome/bus', bus.post_handler);
app.get('/googlehome/bus', bus.get_handler);
app.post('/googlehome/rubbish', rubbish.post_handler);
app.get('/googlehome/rubbish', rubbish.get_handler);
app.listen(serverPort);
