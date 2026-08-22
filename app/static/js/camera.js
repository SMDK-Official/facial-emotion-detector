const video = document.getElementById('webcam');
const startBtn = document.getElementById('start-btn');
const streamStatus = document.getElementById('stream-status');
const videoOverlay = document.getElementById('video-overlay');

startBtn.addEventListener('click', async () => {
    try {
        startBtn.innerText = 'Connecting...';
        const stream = await navigator.mediaDevices.getUserMedia({
            video: {
                width: { ideal: 640 },
                height: { ideal: 480 },
                facingMode: 'user'
            },
            audio: false
        });

        video.srcObject = stream;
        videoOverlay.style.display = 'none';
        startBtn.style.display = 'none';
        
        streamStatus.innerText = 'Active Streaming';
        streamStatus.style.background = 'rgba(16, 185, 129, 0.2)';
        streamStatus.style.color = '#10b981';

        startPredicting();
    } catch (err) {
        console.error('Camera access error:', err);
        streamStatus.innerText = 'Access Denied';
        streamStatus.style.background = 'rgba(244, 63, 94, 0.2)';
        streamStatus.style.color = '#f43f5e';
        alert('Could not access webcam. Please ensure browser permissions are granted.');
        startBtn.innerText = 'Retry Camera Init';
    }
});