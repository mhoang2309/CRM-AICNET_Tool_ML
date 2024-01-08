function uploadFile() {
    var fileInput = document.getElementById('file-input');
    var file = fileInput.files[0];

    if (file) {
        var formData = new FormData();
        formData.append('file', file);

        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'http://127.0.0.1:5000/api/upload_file', true);

        xhr.onload = function () {
            if (xhr.status === 200) {
                console.log('File uploaded successfully');
                // Add any additional handling here
            } else {
                console.error('File upload failed');
                // Handle error conditions here
            }
        };

        xhr.send(formData);
    } else {
        console.error('No file selected');
        // Handle case where no file is selected
    }
}
