const dropArea = document.getElementById('drop-area');
const previewImg = document.getElementById('preview');

;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

;['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => {
        dropArea.classList.add('dragover');
    }, false);
});
;['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => {
        dropArea.classList.remove('dragover');
    }, false);
});

dropArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files.length) {
        uploadFile(files[0]);
    }
}

function uploadFile(file) {
    if (!file.type.startsWith('image/')) {
        alert('Proszę wybrać plik graficzny.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    fetch('http://localhost:5000/process-image', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Błąd przy wysyłaniu: ' + response.statusText);
        }
        return response.blob();  // otrzymujemy binarny blob
    })
    .then(blob => {
        const url = URL.createObjectURL(blob);
        previewImg.src = url;
    })
    .catch(err => {
        console.error(err);
        alert('Wystąpił błąd podczas przesyłania pliku.');
    });
}
