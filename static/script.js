document.getElementById("generateBtn").addEventListener("click", function () {
    const imageUploadInput = document.getElementById("imageUpload");
    const imageFile = imageUploadInput.files[0];

    if (!imageFile) {
        alert("❌ Please upload an image first!");
        return;
    }

    // Display preview immediately (optional)
    const reader = new FileReader();
    reader.onload = function (e) {
        document.getElementById("uploadedImage").src = e.target.result;
        document.getElementById("uploadedImage").style.display = 'block';
    };
    reader.readAsDataURL(imageFile);

    const formData = new FormData();
    formData.append("image", imageFile);

    fetch("/generate_caption", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("captionText").innerText = data.error;
        } else {
            // Optional: update again if you want to display from backend too
            document.getElementById("uploadedImage").src = data.image_url;
            document.getElementById("uploadedImage").style.display = 'block';
            document.getElementById("captionText").innerText = "📝 Caption: " + data.caption;
        }
    })
    .catch(error => {
        document.getElementById("captionText").innerText = "❌ Error generating caption.";
        console.error("Error:", error);
    });
});
