// --- EVENT ---

// wait for the content of the window element to load, then performs the operations
window.addEventListener("load", () => {
    document.addEventListener("mousemove", sketch);
    document.addEventListener("mouseup", stopPainting);
    document.addEventListener("mousedown", startPainting);

    document.getElementById("download-button").addEventListener("click", downloadImage);
    document.getElementById("send-canvas-button").addEventListener("click", sendCanvas);
    document.getElementById("reset-canvas-button").addEventListener("click", resetCanvas);

    resetCanvas();
});

// --- VARIABLE ---

const canvas = document.querySelector("#canvas");
const ctx = canvas.getContext("2d");

let coord = { x: 0, y: 0 };
let paint = false;
let i = 0;

// --- FUNCTION ---

function getPosition(event) {
    coord.x = (event.clientX - canvas.offsetLeft) / 25;
    coord.y = (event.clientY - canvas.offsetTop) / 25;
}

function startPainting(event) {
    paint = true;
    getPosition(event);
}

function stopPainting() {
    paint = false;
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
        const prediction = data.prediction;
        console.log(prediction);
    } catch (error) {
        console.error("There was a problem :", error);
    }
}
