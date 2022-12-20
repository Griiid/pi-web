var ansi_up = new AnsiUp;
function scroll_to_bottom() {
    window.scrollTo(0,document.body.scrollHeight);
}
function append_msg(dt, msg, page_start=false) {
    var html = ansi_up.ansi_to_html(msg);
    var is_at_bottom = false;
    if (page_start == false && window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        is_at_bottom = true;
    }
    $('.content').append('<div class="msg">' + dt + ' ' + html + '</div>');
    if (is_at_bottom) {
        scroll_to_bottom()
    }
}
$(document).ready(() => {
    var socket = io.connect();

    var started = false;
    socket.on('connect', () => {
        socket.emit('start', (response) => {
            if (started == false) {
                started = true
                response.forEach((item) => {
                    var dt = item.datetime;
                    var msg = item.msg;
                    append_msg(dt, msg, true);
                });
                scroll_to_bottom();
            }
        });
    });

    socket.on('msg', (data) => {
        var dt = data.datetime;
        var msg = data.msg;
        append_msg(dt, msg);
    });

    socket.on('start-list-msg', (data) => {
        data.forEach((item) => {
            var dt = item.datetime;
            var msg = item.msg;
            append_msg(dt, msg);
        });
    });
    $(".to-bottom-button").click(() => {
        scroll_to_bottom();
    });
    $(window).scroll(() => {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
            $(".to-bottom-button").css("visibility","hidden");
        }
        else {
            $(".to-bottom-button").css("visibility","visible");
        }
    });
});
