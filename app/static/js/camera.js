const video = document.getElementById('webcam');
const startBtn = document.getElementById('start-btn');

startBtn.addEventListener('click', async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        startBtn.style.display = 'none';
        startPredicting();
    } catch (err) {
        alert("Camera permission denied.");
    }
});