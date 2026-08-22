const offscreenCanvas = document.createElement('canvas');
offscreenCanvas.width = 400;
offscreenCanvas.height = 300;
const offscreenCtx = offscreenCanvas.getContext('2d');

const saveBtn = document.getElementById('save-btn');
const emotionDisplay = document.getElementById('emotion-display');
const confidenceVal = document.getElementById('confidence-val');
const confidenceProgress = document.getElementById('confidence-progress');
const reportText = document.getElementById('report-text');

let buffer = [];
let currentDominant = "";
let currentConfidence = 0.0;
let isPredicting = false;

// 1. The Bulletproof Smart Loop
async function predictLoop() {
    // If the system is turned off, stop entirely.
    if (!isPredicting) return;

    // THE FIX: If the camera is still warming up, wait 100ms and check again!
    if (!video.videoWidth) {
        setTimeout(predictLoop, 100);
        return; 
    }

    offscreenCtx.drawImage(video, 0, 0, 400, 300);
    const base64Data = offscreenCanvas.toDataURL('image/jpeg', 0.5); 

    try {
        const res = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: base64Data })
        });

        const data = await res.json();

        if (data.status === 'success') {
            stabilize(data.emotion, data.confidence);
        } else if (data.status === 'no_face_detected') {
            emotionDisplay.innerText = 'No Face';
            confidenceVal.innerText = '0.0%';
            confidenceProgress.style.width = '0%';
            reportText.innerText = 'AI Blinded: Cannot detect facial features. Please check your lighting or reduce camera glare.';
            saveBtn.style.display = 'none';
        }
    } catch (err) {
        console.error('Inference pipeline error:', err);
    }

    setTimeout(predictLoop, 50); 
}

function startPredicting() {
    isPredicting = true;
    predictLoop(); 
}

function stabilize(emotion, conf) {
    buffer.push(emotion);
    if (buffer.length > 3) buffer.shift();

    const counts = buffer.reduce((acc, val) => {
        acc[val] = (acc[val] || 0) + 1;
        return acc;
    }, {});

    currentDominant = Object.keys(counts).reduce((a, b) => counts[a] > counts[b] ? a : b);
    currentConfidence = conf;

    emotionDisplay.innerText = currentDominant;
    confidenceVal.innerText = `${currentConfidence.toFixed(1)}%`;
    confidenceProgress.style.width = `${currentConfidence}%`;
    reportText.innerText = `The model classified the observed facial expression as ${currentDominant.toUpperCase()} with ${currentConfidence.toFixed(1)}% confidence.`;

    saveBtn.style.display = 'inline-flex';
}

saveBtn.addEventListener('click', async () => {
    saveBtn.innerText = 'Saving...';
    saveBtn.disabled = true;

    const currentSnapshot = offscreenCanvas.toDataURL('image/jpeg', 0.8);

    try {
        const res = await fetch('/api/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                emotion: currentDominant,
                confidence: currentConfidence,
                image: currentSnapshot 
            })
        });

        const data = await res.json();
        if (data.status === 'success') {
            saveBtn.innerText = 'Moment Saved!';
            saveBtn.style.background = '#64748b';
            setTimeout(() => {
                saveBtn.innerText = 'Save Moment';
                saveBtn.style.background = 'var(--accent-purple)';
                saveBtn.disabled = false;
            }, 2500);
        }
    } catch (err) {
        saveBtn.innerText = 'Save Error';
        saveBtn.disabled = false;
    }
});