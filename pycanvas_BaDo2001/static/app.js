var ws = new WebSocket('ws://localhost:5000/ws');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

const images = {};

const toRad = (angle) => (angle * Math.PI) / 180;

const onSetup = ({ width, height }) => {
    canvas.width = width;
    canvas.height = height;
};

const onDraw = ({ type, payload }) => {
    try {
        if (type === 'clearRect') {
            const [x, y, width, height] = payload;
            ctx.clearRect(x, y, width, height);
        } else if (type === 'fillRect') {
            const [x, y, width, height, color] = payload;
            ctx.fillStyle = color;
            ctx.fillRect(x, y, width, height);
        } else if (type === 'strokeRect') {
            const [x, y, width, height, color] = payload;
            ctx.strokeStyle = color;
            ctx.strokeRect(x, y, width, height);
        } else if (type === 'fillCircle') {
            const [x, y, r, color, startAngle, endAngle] = payload;
            ctx.beginPath();
            ctx.arc(x, y, r, toRad(startAngle), toRad(endAngle));
            ctx.closePath();
            ctx.fillStyle = color;
            ctx.fill();
        } else if (type === 'strokeCircle') {
            const [x, y, r, color, startAngle, endAngle] = payload;
            ctx.beginPath();
            ctx.arc(x, y, r, toRad(startAngle), toRad(endAngle));
            ctx.closePath();
            ctx.strokeStyle = color;
            ctx.stroke();
        } else if (type === 'line') {
            const [x1, y1, x2, y2, color, lineWidth] = payload;
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.closePath();
            ctx.strokeStyle = color;
            ctx.lineWidth = lineWidth;
            ctx.stroke();
        } else if (type === 'image') {
            debugger;
            const [id, ...coords] = payload;
            if (!images[id]) {
                throw new Error('This image does not exist!');
            } else {
                if (coords.length === 2) {
                    const [dx, dy] = coords;
                    ctx.drawImage(images[id], dx, dy);
                } else if (coords.length === 4) {
                    const [dx, dy, dw, dh] = coords;
                    ctx.drawImage(images[id], dx, dy, dw, dh);
                } else if (coords.length === 8) {
                    const [sx, sy, sw, sh, dx, dy, dw, dh] = coords;
                    ctx.drawImage(images[id], sx, sy, sw, sh, dx, dy, dw, dh);
                } else {
                    throw new Error('Image coordinates are invalid!');
                }
            }
        } else {
            throw new Error('Unknown command type');
        }
    } catch (error) {
        console.log(error);
    }
};

const onImage = ({ image, id }) => {
    const newImage = new Image();
    newImage.src = image;
    images[id] = newImage;
    newImage.onload = () =>
        ws.send(
            JSON.stringify({
                type: 'image_loaded',
                payload: id
            })
        );
};

const handleMessage = (type, payload) => {
    switch (type) {
        case 'setup':
            onSetup(payload);
            break;
        case 'image':
            onImage(payload);
            break;
        case 'draw':
            onDraw(payload);
            break;

        default:
            console.log('ERROR: Unknown message type');
            ws.send(
                JSON.stringify({
                    type: 'error',
                    message: 'ERROR: Unknown message type'
                })
            );
    }
};

ws.onmessage = (evt) => {
    const { type, payload } = JSON.parse(evt.data);
    if (type === 'batch') {
        for (let item of payload) {
            handleMessage(...item);
        }
    } else {
        handleMessage(type, payload);
    }
};

const sendEvent = (type, payload) => {
    ws.send(
        JSON.stringify({
            type: 'event',
            payload: {
                type,
                payload
            }
        })
    );
};

window.onkeydown = (e) => sendEvent('keydown', e.code);

window.onkeyup = (e) => sendEvent('keyup', e.code);

window.onmousedown = (e) => {
    if (e.target === canvas) {
        sendEvent('mousedown', [
            e.which,
            e.x - canvas.getBoundingClientRect().left,
            e.y - canvas.getBoundingClientRect().top
        ]);
    }
};

window.onmouseup = (e) => {
    if (e.target === canvas) {
        sendEvent('mouseup', [
            e.which,
            e.x - canvas.getBoundingClientRect().left,
            e.y - canvas.getBoundingClientRect().top
        ]);
    }
};

window.oncontextmenu = () => false;
