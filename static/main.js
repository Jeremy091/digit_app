const fileInput = document.getElementById('fileInput');
const predictButton = document.getElementById('predictButton');
const result = document.getElementById('result');
const preview = document.getElementById('preview');
const progressBar = document.getElementById('progress-bar');

fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            preview.innerHTML = `<img src="${e.target.result}" style="max-width:200px;">`;
        };
        reader.readAsDataURL(file);
    }
});

predictButton.addEventListener('click', async () => {
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select an image first!');
        return;
    }

    progressBar.style.width = '0%';
    progressBar.classList.add('loading');

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Prediction failed.');
        }

        const data = await response.json();
        result.innerText = `Predicted digit: ${data.digit} (confidence: ${(data.confidence * 100).toFixed(2)}%)`;
    } catch (error) {
        result.innerText = error.message;
    } finally {
        progressBar.style.width = '100%';
        setTimeout(() => progressBar.classList.remove('loading'), 500);
    }
});
