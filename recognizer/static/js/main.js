let paint = false;
let another = false;
let canvasSize;
let context;
let canvas;

let predBox;
let answer;
let symbol;
let val2;

window.onload = function() {
    canvas = document.getElementById("canvas");
    predBox = document.getElementById("dummy");
    answer = document.getElementById("answer");
    symbol = document.getElementById("button_2");

    context = canvas.getContext("2d");

    canvasSize = Math.round(window.innerWidth * 0.4);
    let lineW = Math.round(window.innerWidth * 0.007);
    context.canvas.width = canvasSize;
    context.canvas.height = canvasSize;

    context.fillStyle = "#000";
    context.lineWidth = lineW;
    context.strokeStyle = "#fff";

    canvas.onmousedown = startDrawing;
    canvas.onmousemove = draw;
    canvas.onmouseup = stopDrawing;

    canvas.addEventListener('touchstart', touchStart, false);
    canvas.addEventListener('touchmove', touchMove, false);
    canvas.addEventListener('touchend', touchEnd, false);
}

function startDrawing(e) {
    paint = true;
    another = false;
    context.beginPath();
    context.moveTo(e.pageX - canvas.offsetLeft, e.pageY - canvas.offsetTop);
}

function draw(e) {
    if (paint) {
        let x = e.pageX - canvas.offsetLeft;
        let y = e.pageY - canvas.offsetTop;

        context.lineTo(x, y);
        context.stroke();
    }
}

function stopDrawing(e) {
    paint = false;
    let timerID = setTimeout(sendImage, 300);
}

function touchStart(e) {
    startDrawing(e.touches[0]);
}

function touchMove(e) {
    draw(e.touches[0]);
    e.preventDefault();
}

function touchEnd(e) {
    stopDrawing(e.touches[0]);
}

function clearCanvas() {
    context.fillRect(0, 0, canvasSize + 10, canvasSize + 10);
    predBox.style.visibility = 'hidden';
    symbol.style.visibility = 'hidden';
}

function sendImage() {
    let canvasData = canvas.toDataURL('image/png');

    fetch('/api/greek-ai', {
        method: 'POST',
        body: new URLSearchParams({
            image: canvasData
        })
    })
        .then(response => response.json())
        .then(data => {
            symbol.href = "#/";

            let code = data.code;
		    let rate = data.probability;
		    val2 = data.symbol;
            let CASE;

            if (code.charAt(0) === 'L') {
                CASE = 'lower';
            } else {
                CASE = 'upper';
            }

            answer.innerText = `Suggestion: ${CASE} ${code.slice(1)} \n ${rate}%`;
            symbol.innerText = val2;

            predBox.style.visibility = 'visible';
            symbol.style.visibility = 'visible';
        })
}
