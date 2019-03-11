function debounce(func, wait, immediate) {
	var timeout;
	return function() {
		var context = this, args = arguments;
		var later = function() {
			timeout = null;
			if (!immediate) func.apply(context, args);
		};
		var callNow = immediate && !timeout;
		clearTimeout(timeout);
		timeout = setTimeout(later, wait);
		if (callNow) func.apply(context, args);
	};
};

class Comms {

  constructor() {
    this.socket = undefined;
    this.connected = false;
    this.messages = [];
  }

  connect(target) {
    if (!this.connected) {
      console.log('connecting');
      // this.socket = new WebSocket("ws://127.0.0.1:9001/control_socket");
      this.socket = new WebSocket("ws://" + target);
      this.socket.addEventListener('open', function (event) {
          console.log(`Connected to websocket at ${target}`);
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
    this.messages.push(json_msg);
    if (this.messages.length > 20) {
      this.messages.shift();
    }
    messageLog.innerHTML = this.messages.join('<br />');
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
  let target = document.getElementById('targetIp').value;
  commo.connect(target);
}


let messageLog = document.getElementById('messageLog');
let debounceRate = 100;
document.addEventListener('keydown', debounce(handleKeyDown, debounceRate));
document.addEventListener('keyup', debounce(handleKeyUp, debounceRate));

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
