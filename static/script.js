window.addEventListener('DOMContentLoaded', () => {
    const clock = document.getElementById('clock');
    if (clock) {
        setInterval(() => {
            const now = new Date();
            clock.textContent = now.toLocaleTimeString();
        }, 1000);
    }
});
