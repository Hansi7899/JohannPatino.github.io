const video = document.getElementById('introVideo');
const overlay = document.getElementById('overlay');
const cvContent = document.getElementById('cvContent');
const startScreen = document.getElementById('startScreen');
const startBtn = document.getElementById('startBtn');

startBtn.addEventListener('click', () => {
    startScreen.style.display = 'none';
    video.play();
});

video.addEventListener('ended', () => {
    overlay.classList.add('expand');
    video.style.display = 'none';
    setTimeout(() => {
        cvContent.classList.add('show');
    }, 1000);
});


// No idea if i need this for ios devices.
if (navigator.userAgent.match(/iPhone|iPad|iPod/)) {
    const playButton = document.getElementById('startBtn');
    const video = document.getElementById('introVideo');

    playButton.style.display = 'block';
    playButton.addEventListener('click', () => {
        video.play();
        playButton.style.display = 'none';
    });
}

// Add event listener for 'e' to skip the video and show the CV 
document.addEventListener('keydown', function (event) {
    if (event.key === 'e' || event.key === 'E') {
        const video = document.getElementById('introVideo');
        const cvContent = document.getElementById('cvContent');

        if (video) {
            video.pause();
            video.style.display = 'none';
        }

        if (cvContent) {
            overlay.classList.add('expand');
            cvContent.classList.add('show');
            window.scrollTo({ top: cvContent.offsetTop, behavior: 'smooth' });
        }
    }
});

