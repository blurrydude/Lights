var canvas = document.getElementById("myCanvas");
var secretIframe = document.getElementById("secretIframe");
var context = canvas.getContext('2d');

function showSectionControl() {
    context.lineWidth = 10;
    context.moveTo(60, 5); // a
    context.lineTo(5, 155); // h
    context.lineTo(5, 205); // g
    context.lineTo(60, 595); // f
    context.lineTo(160, 595); // e
    context.lineTo(215, 205); // d
    context.lineTo(215, 155); // c
    context.lineTo(160, 5); // b
    context.lineTo(60, 5); // a
    context.moveTo(5, 155); // h
    context.lineTo(215, 155); // c
    context.moveTo(5, 205); // g
    context.lineTo(215, 205); // d
    context.moveTo(17, 291);
    context.lineTo(202, 291);
    context.moveTo(31, 395);
    context.lineTo(188, 395);
    context.moveTo(45, 498);
    context.lineTo(174, 498);
    context.stroke();
}
function writeMessage(message) {
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.font = '18pt Calibri';
    context.fillStyle = 'black';
    context.fillText(message, 10, 25);
}
function getMousePos(evt) {
    var rect = canvas.getBoundingClientRect();
    return {
    x: evt.clientX - rect.left,
    y: evt.clientY - rect.top
    };
}

/*canvas.addEventListener('mousemove', function(evt) {
    var mousePos = getMousePos(canvas, evt);
    var message = 'Mouse position: ' + mousePos.x + ',' + mousePos.y;
    //writeMessage(canvas, message);
    console.log(message)
}, false);*/

var colorPicker = document.getElementById("colorPicker");
colorPicker.addEventListener('change', function(evt) {
    var color = hexToRgb(colorPicker.value);
    var url = window.location.origin + '/?r='+color.r+'&g='+color.g+'&b='+color.b+'&a=0&z=119';
    $.get(url, function(response) {
        console.log(response);
    });
}, false);

var sectionControlButton = document.getElementById("sectionControlButton");
sectionControlButton.addEventListener('click', function(evt) {
    showSectionControl();
}, false);

function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

$.get(window.location.origin + '/version', function(response) {
    document.getElementById("versionEle").innerHTML = JSON.parse(response).version;
});