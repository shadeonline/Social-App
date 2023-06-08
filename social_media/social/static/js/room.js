const roomName = JSON.parse(document.getElementById('room-name').textContent);

const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/' + roomName + '/');
document.querySelector('#chat-log').scrollTop = document.querySelector('#chat-log').scrollHeight;

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    const months = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.", "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."];
    const now = new Date();
    const month = months[now.getMonth()];
    const day = now.getDate();
    const year = now.getFullYear();
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const ampm = hours >= 12 ? "p.m." : "a.m.";
    const formattedHours = hours % 12 || 12;
    const formattedMinutes = minutes < 10 ? "0" + minutes : minutes;
    const formattedTime = month + " " + day + ", " + year + ", " + formattedHours + ":" + formattedMinutes + " " + ampm;
    document.querySelector('#chat-log').value += (formattedTime + ' - ' + data.username + ': ' + data.message + '\n\n');
    document.querySelector('#chat-log').scrollTop = document.querySelector('#chat-log').scrollHeight;

};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    const username = document.getElementById("chat-message-submit").getAttribute("name");
    chatSocket.send(JSON.stringify({
        'message': message,
        'username': username
    }));
    messageInputDom.value = '';
};
