var canvas;
var context;
var timeout_id;
var url;
window.onload = function() {
      canvas = document.getElementById("drawingCanvas");
      context = canvas.getContext("2d");
      context.lineWidth = 10;
	  now = new Date();

      // Подключаем требуемые для рисования события
      canvas.onmousedown = startDrawing;
      canvas.onmouseup = stopDrawing;
      canvas.onmouseout = stopDrawing;
      canvas.onmousemove = draw;
}

function startDrawing(e) {
	// Начинаем рисовать
	isDrawing = true;
	clearTimeout(timeout_id);

	// Создаем новый путь (с текущим цветом и толщиной линии)
	context.beginPath();

	// Нажатием левой кнопки мыши помещаем "кисть" на холст
	context.moveTo(e.pageX - canvas.offsetLeft, e.pageY - canvas.offsetTop);
}

function draw(e) {
	if (isDrawing == true)
	{
	  	// Определяем текущие координаты указателя мыши
		var x = e.pageX - canvas.offsetLeft;
		var y = e.pageY - canvas.offsetTop;

		// Рисуем линию до новой координаты
		context.lineTo(x, y);
		context.stroke();
	}
}

function stopDrawing() {
    isDrawing = false;
	timeout_id = setTimeout(clearCanvas, 2000);
}

function saveData(){
	var canvasData = canvas.toDataURL("image/png");
	var ajax = new XMLHttpRequest();
	ajax.open("POST",'http://localhost:8080/server.php',true);
	ajax.setRequestHeader('Content-Type', 'application/upload');
	ajax.send(canvasData);
	context.clearRect(0, 0, canvas.width, canvas.height);
}

function clearCanvas() {
	saveData();
}

function clearCanvasButton() {
	context.clearRect(0, 0, canvas.width, canvas.height);
	clearTimeout(timeout_id);
}