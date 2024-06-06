// --- EVENT ---

// wait for the content of the window element to load, then performs the operations
window.addEventListener("load", () => {
    document.addEventListener("mousemove", sketch);
    document.addEventListener("mouseup", stopPainting);
    document.addEventListener("mousedown", startPainting);

    document.getElementById("download-button").addEventListener("click", downloadImage);
    document.getElementById("reset-canvas-button").addEventListener("click", resetCanvas);

    resetCanvas();
});

// --- VARIABLE ---

const canvas = document.querySelector("#canvas");
const ctx = canvas.getContext("2d");

let progress = document.querySelectorAll(".container-progress progress");

let coord = { x: 0, y: 0 };
let paint = false;
let i = 0;

// --- FUNCTION ---

// - canvas -

function getPosition(event) {
    coord.x = (event.clientX - canvas.offsetLeft) / 25;
    coord.y = (event.clientY - canvas.offsetTop) / 25;
}

function isOnCanvas(event) {
    return (
        event.clientX >= canvas.offsetLeft &&
        event.clientX < canvas.offsetLeft + canvas.clientWidth &&
        event.clientY >= canvas.offsetTop &&
        event.clientY < canvas.offsetTop + canvas.clientHeight
    );
}

function startPainting(event) {
    if (isOnCanvas(event)) {
        paint = true;
        getPosition(event);
    }
}

function stopPainting() {
    if (paint) {
        paint = false;
        sendCanvas();
    }
}

function sketch(event) {
    if (!paint) return;

    ctx.beginPath();
    ctx.lineWidth = 1;

    ctx.moveTo(coord.x, coord.y); // The cursor to start drawing moves to this coordinate
    getPosition(event); // The position of the cursor gets updated as we move the mouse around.
    ctx.lineTo(coord.x, coord.y); // A line is traced from start coordinate to this coordinate

    ctx.stroke();
}

function downloadImage() {
    const dataURL = canvas.toDataURL("image/jpeg");

    const link = document.createElement("a");
    link.href = dataURL;
    link.download = "canvas-image.jpg";

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function resetCanvas() {
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    updateProgress([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]);
}

async function sendCanvas() {
    // - get array -

    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const pixels = Array.from(imageData.data);

    const pixels_gray = [];
    for (let i = 0; i < pixels.length; i += 4) {
        pixels_gray.push(pixels[i]);
    }

    // - send array -
    try {
        const response = await fetch("/post-canvas", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                pixels: Array.from(pixels_gray),
                width: canvas.width,
                height: canvas.height,
            }),
        });

        if (!response.ok) {
            throw new Error("Network error " + response.statusText);
        }

        const data = await response.json();
        const prediction = data.prediction[0];
        const number = data.number;

        updateProgress(prediction, number);
    } catch (error) {
        console.error("There was a problem :", error);
    }
}

// - progress -

function updateProgress(prediction, number = -1) {
    for (let i = 0; i < progress.length; i++) {
        progress[i].value = prediction[i];
        progress[i].style.accentColor = "#DF2E38";
    }

    if (number != -1) {
        progress[number].style.accentColor = "#5D9C59";
    }
}
