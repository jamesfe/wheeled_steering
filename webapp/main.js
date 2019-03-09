console.log('hi');

class Comms {

  constructor() {
    this.socket = undefined;
    this.connected = false;
  }

  connect() {
    if (!this.connected) {
      console.log('connecting');
      this.socket = new WebSocket("ws://127.0.0.1:9001/control_socket");
      this.socket.addEventListener('open', function (event) {
          console.log('Open for business!');
          setConnected();
      });
    console.log('connected');
    }
  }

  send(message) {
    if (!this.connected) {
      this.connect();
    }
    let json_msg = JSON.stringify(message);
    messageLog.innerHTML = messageLog.innerHTML + "<br>" + json_msg;
    console.log('sending message: ' + json_msg);
    this.socket.send(json_msg);
  }
}

var commo = new Comms();
var global_connected = false;

let setConnected = function() {
  console.log('Connecting to websocket!');
  commo.connected = true;
  global_connected = true;
};

function initial_connect() {
  commo.connect();
}


let messageLog = document.getElementById('messageLog');
document.addEventListener('keydown', handleKeyDown);
document.addEventListener('keyup', handleKeyUp);

function handleKeyDown(event) {
  if (global_connected) {
    switch (event.key) {
      case ' ':
        commo.send({'message': 'stop'});
        break;
      case 'i':
        commo.send({'message': 'faster'});
        break;
      case 'k':
        commo.send({'message': 'slower'});
        break;
      case 'j':
        commo.send({'message': 'left'});
        break;
      case 'l':
        commo.send({'message': 'right'});
        break;
    }
  }
}

function handleKeyUp(event) {
  if (global_connected) {
    switch (event.key) {
      case 'j':
        commo.send({'message': 'straight'});
        break;
      case 'l':
        commo.send({'message': 'straight'});
        break;
    }
  }
}
