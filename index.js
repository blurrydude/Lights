var canvas = document.getElementById("myCanvas");
var secretIframe = document.getElementById("secretIframe");
var context = canvas.getContext('2d');
var mem = [];

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

var targetColor = "#ff0000";

var segments = [
    { a: points.n, b: points.e, r1:   0, r2:   5, c: "#00ff00" },
    { a: points.e, b: points.f, r1:   6, r2:  11, c: "#00ff00" },
    { a: points.f, b: points.m, r1:  12, r2:  17, c: "#00ff00" },
    { a: points.m, b: points.k, r1:  18, r2:  24, c: "#00ff00" },
    { a: points.k, b: points.i, r1:  25, r2:  30, c: "#00ff00" },
    { a: points.i, b: points.g, r1:  31, r2:  35, c: "#00ff00" },
    { a: points.g, b: points.h, r1:  36, r2:  39, c: "#00ff00" },
    { a: points.h, b: points.a, r1:  40, r2:  50, c: "#00ff00" },
    { a: points.a, b: points.b, r1:  51, r2:  56, c: "#00ff00" },
    { a: points.b, b: points.c, r1:  57, r2:  67, c: "#00ff00" },
    { a: points.c, b: points.d, r1:  68, r2:  71, c: "#00ff00" },
    { a: points.d, b: points.j, r1:  72, r2:  75, c: "#00ff00" },
    { a: points.j, b: points.l, r1:  76, r2:  81, c: "#00ff00" },
    { a: points.l, b: points.n, r1:  82, r2:  89, c: "#00ff00" },
];

var sections = [
    [7,8,9],
    [6, 10],
    [5, 11],
    [4, 12],
    [3, 13],
    [2,1,0]
];

function lineTo(point) {
    context.lineTo(point.x, point.y);
}

function moveTo(point) {
    context.moveTo(point.x, point.y);
}

function drawCoffin() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.lineWidth = 5;
    //context.fillStyle = "Green";

    context.beginPath();
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
    context.strokeStyle = "#000000";
    context.closePath();
    context.stroke();

    /*context.beginPath()
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
    context.stroke();*/
    for(var s in segments) {
        drawSegment(segments[s]);
    }
}

function drawSegment(segment) {
    context.beginPath();
    moveTo(segment.a);
    lineTo(segment.b);
    context.strokeStyle = segment.c;
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
    targetColor = colorPicker.value;
}, false);

function setSection(sec) {
    console.log('set section '+sec);
    var segs = sections[sec];
    var promises = [];
    for(var s in segs) {
        promises.push(setSegment(segs[s]));
    }
    Promise.all(promises).then(function(responses) {
        console.log(responses);
        drawCoffin();
    });
}

function setSegment(s) {
    return new Promise(function(resolve, reject) {
        var segment = segments[s];
        console.log('set segment ', segment);
        segment.c = targetColor;
        var color = hexToRgb(targetColor);
        var url = window.location.origin + '/?r='+color.r+'&g='+color.g+'&b='+color.b+'&a='+segment.r1+'&z='+segment.r2;
        $.get(url, function(response) {
            resolve(response);
        });
    });
}

function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

$.get(window.location.origin + '/version', function(response) {
    document.getElementById("versionEle").innerHTML = JSON.parse(response).version;
});

$.get(window.location.origin + '/mem', function(response) {
    mem = response;
    for(var s in segments) {
        var segment = segments[s];
        var m = mem[segment.r1];
        segment.c = rgbToHex(m[0],m[1],m[2]);
        drawCoffin();
    }
});
