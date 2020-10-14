'use strict';

require('dotenv').config()


const express = require('express');
const app = express();

app.use(express.static(__dirname + '/views')); 
app.use(express.static(__dirname + '/public'));

const server = app.listen(process.env.PORT || 5000, () => {
  console.log('Express server listening on port %d in %s mode', server.address().port, app.settings.env);
});

const io = require('socket.io')(server);
io.on('connection', function(socket){
  console.log('a user connected');
});


// Web UI
app.get('/', (req, res) => {
  res.sendFile('index.html');
});



io.on('connection', function(socket) {
  socket.on('chat message', (text) => {
    console.log('Message: ' + text);
    var request = require('request');
    var propertiesObject = { incoming:text };
    request({url:'http://127.0.0.1:3000/message', qs:propertiesObject}, function(err, response, body) {
      if(err) { console.log(err); return; }
      console.log("Get response: " + response.statusCode);
      const data = JSON.parse(body);
      console.log('data: ' + data.message);
      let return_message = data.message.toString().replace(/,/g,"\n");
      console.log('Bot reply: ' + return_message);
      socket.emit('bot reply', return_message);  
     });
  });
});
