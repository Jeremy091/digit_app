// static/main.js
document.getElementById("btnUpload").onclick = async () => {
    const input = document.getElementById("fileInput");
    if (!input.files.length) {
      return alert("Selecciona un archivo primero");
    }
  
    const form = new FormData();
    form.append("file", input.files[0]);
  
    const res = await fetch("/api/predict", {
      method: "POST",
      body: form
    });
    const data = await res.json();
  
    const resultDiv = document.getElementById("result");
    if (data.error) {
      resultDiv.innerText = `Error: ${data.error}`;
    } else {
      resultDiv.innerText =
        `Predicción: ${data.digit} (confianza ${(data.confidence*100).toFixed(1)}%)`;
    }
  };
  