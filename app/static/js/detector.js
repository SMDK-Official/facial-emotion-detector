const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let buffer = []; 

function startPredicting() {
    setInterval(async () => {
        ctx.drawImage(video, 0, 0, 400, 300);
        const res = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: canvas.toDataURL('image/jpeg') })
        });
        const data = await res.json();
        if (data.status === 'success') stabilize(data.emotion, data.confidence);
    }, 500); 
}

function stabilize(emotion, conf) {
    buffer.push(emotion);
    if (buffer.length > 4) buffer.shift(); 
    const counts = buffer.reduce((acc, val) => { acc[val] = (acc[val] || 0) + 1; return acc; }, {});
    const dominant = Object.keys(counts).reduce((a, b) => counts[a] > counts[b] ? a : b);
    document.getElementById('emotion-text').innerText = `Emotion: ${dominant}`;
    document.getElementById('confidence-text').innerText = `Confidence: ${conf}%`;
}