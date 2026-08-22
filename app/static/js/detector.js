const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const saveBtn = document.getElementById('save-btn');

let buffer = [];
let currentDominant = "";
let currentConfidence = 0;

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
    
    // Find the most frequent emotion in the last 4 frames
    const counts = buffer.reduce((acc, val) => { acc[val] = (acc[val] || 0) + 1; return acc; }, {});
    currentDominant = Object.keys(counts).reduce((a, b) => counts[a] > counts[b] ? a : b);
    currentConfidence = conf;
    
    document.getElementById('emotion-text').innerText = `Emotion: ${currentDominant}`;
    document.getElementById('confidence-text').innerText = `Confidence: ${currentConfidence}%`;
    
    // Show the save button once we have a stable reading
    saveBtn.style.display = 'inline-block';
}

// Click event for the Save Button
saveBtn.addEventListener('click', async () => {
    saveBtn.innerText = "Saving...";
    const res = await fetch('/api/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ emotion: currentDominant, confidence: currentConfidence })
    });
    const data = await res.json();
    if (data.status === 'success') {
        saveBtn.innerText = "Saved!";
        saveBtn.style.background = "#64748b";
        setTimeout(() => {
            saveBtn.innerText = "Save Result to Database";
            saveBtn.style.background = "#10b981";
        }, 2000);
    }
});