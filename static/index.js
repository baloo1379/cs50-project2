(function () {
    let not = document.getElementsByClassName('notification')[0];
    let notDel = document.getElementsByClassName('delete');
    if (notDel.length > 0) {
        notDel[0].addEventListener('click', () => {
            not.remove();
        }, false)
    }
})();

function registerOnChannel(socket, nickname, channelIndex) {
    socket.emit("register_on_channel", {
        "channel": channelIndex,
        "nickname": nickname
    });
}

function sendMessage(socket, nickname, message, channel) {
    socket.emit("new_message", {
        "channel": channel,
        "nickname": nickname,
        "message": message
    });
}