(function () {
    let not = document.getElementsByClassName('notification')[0];
    let notDel = document.getElementsByClassName('delete');
    if (notDel.length > 0) {
        notDel[0].addEventListener('click', () => {
            not.remove();
        }, false)
    }
})();
(function () {
    const navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

    if (navbarBurgers.length > 0) {
        // Add a click event on each of them
        navbarBurgers.forEach(el => {
            el.addEventListener('click', () => {

                // Get the target from the "data-target" attribute
                const target_name = el.dataset.target;
                const target = document.getElementById(target_name);

                // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
                el.classList.toggle('is-active');
                target.classList.toggle('is-active');

            });
        });
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