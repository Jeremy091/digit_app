const fileInput = document.getElementById('fileInput');
const predictButton = document.getElementById('predictButton');
const result = document.getElementById('result');
const preview = document.getElementById('preview');
const progressBar = document.getElementById('progress-bar');
const progressContainer = document.getElementById('progress-container');

fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            preview.innerHTML = `<img src="${e.target.result}" width="150" />`;
        };
        reader.readAsDataURL(file);
    }
});

predictButton.addEventListener('click', async () => {
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select an image.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    progressContainer.style.display = 'block';
    progressBar.style.width = '0%';

    // Simulación de carga
    let progress = 0;
    const interval = setInterval(() => {
        if (progress < 90) {
            progress += 10;
            progressBar.style.width = `${progress}%`;
        }
    }, 100);

    const response = await fetch('/api/predict', {
        method: 'POST',
        body: formData
    });

    clearInterval(interval);
    progressBar.style.width = '100%';

    if (response.ok) {
        const data = await response.json();
        result.innerText = `Prediction: ${data.digit} (Confidence: ${(data.confidence * 100).toFixed(2)}%)`;
    } else {
        result.innerText = 'Error during prediction.';
    }
});
