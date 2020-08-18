var canvas = document.getElementById("myCanvas");
var secretIframe = document.getElementById("secretIframe");
var context = canvas.getContext('2d');

var points = {
    a: { x:  60, y:   5 },
    b: { x: 160, y:   5 },
    c: { x: 215, y: 155 },
    d: { x: 215, y: 205 },
    e: { x: 160, y: 595 },
    f: { x:  60, y: 595 },
    g: { x:   5, y: 205 },
    h: { x:   5, y: 155 },
    i: { x:  17, y: 291 },
    j: { x: 202, y: 291 },
    k: { x:  31, y: 395 },
    l: { x: 188, y: 395 },
    m: { x:  45, y: 498 },
    n: { x: 174, y: 498 }
}

function lineTo(point) {
    context.lineTo(point.x, point.y);
}

function moveTo(point) {
    context.moveTo(point.x, point.y);
}

function showSectionControl() {
    context.lineWidth = 10;
    //context.fillStyle = "Green";
    context.beginPath()
    moveTo(points.a);
    lineTo(points.h);
    lineTo(points.g);
    lineTo(points.f);
    lineTo(points.e);
    lineTo(points.d);
    lineTo(points.c);
    lineTo(points.b);
    lineTo(points.a);
    context.strokeStyle = "Green";
    context.closePath();
    context.stroke();
    context.beginPath()
    moveTo(points.h);
    lineTo(points.c);
    moveTo(points.g);
    lineTo(points.d);
    moveTo(points.i);
    lineTo(points.j);
    moveTo(points.k);
    lineTo(points.l);
    moveTo(points.m);
    lineTo(points.n);
    context.strokeStyle = "#996400";
    context.closePath();
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

showSectionControl();