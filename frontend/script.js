function uploadFile() {
    let fileInput = document.getElementById("fileInput");
    let message = document.getElementById("message");

    if (fileInput.files.length === 0) {
        message.innerText = "Please select a file.";
        return;
    }

    let file = fileInput.files[0];
    let formData = new FormData();
    formData.append("file", file);

    console.log("Uploading file:", file.name);

    fetch("http://localhost:5000/upload/", {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success:", data);
        message.innerText = data.message;
    })
    .catch(error => {
        console.error("Error:", error);
        message.innerText = "Failed to upload.";
    });
}