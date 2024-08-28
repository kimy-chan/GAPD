
const socket = new WebSocket('ws://' + window.location.host + '/ws/notificaciones/');

socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log('Received message:', data);

};

socket.onclose = function (e) {
    console.log(e);

    console.error('WebSocket closed unexpectedly');
};


socket.onopen = function (e) {
    alert('conectada')
    socket.send(JSON.stringify({
        'message': 'Hello, WebSocket!'
    }));
};
