document.getElementById("fileInput").addEventListener("change", function () {
    const file = this.files[0];
    if (!file) return;

    const url = URL.createObjectURL(file);

    const preview = document.getElementById("preview");
    preview.src = url;
    preview.style.display = "block";

    // Xóa kết quả cũ
    document.getElementById("result-box").innerHTML = "";
});

document.getElementById("uploadBtn").addEventListener("click", function () {

    const fileInput = document.getElementById("fileInput");
    if (fileInput.files.length === 0) {
        alert("Vui lòng chọn ảnh!");
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("image", file);

    // Loading message (không icon)
    const resultBox = document.getElementById("result-box");
    resultBox.innerHTML = `<span class="text-warning fw-bold">Đang dự đoán...</span>`;

    fetch("/predict", {
        method: "POST",
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            resultBox.innerHTML = `
                <div class="fw-bold" style="font-size:28px;color:#0d6efd;">
                    ${data.prediction}
                </div>
            `;
        })
        .catch(error => {
            console.error("Lỗi:", error);
            resultBox.innerHTML = `
                <div class="text-danger">Có lỗi xảy ra. Vui lòng thử lại.</div>
            `;
        });
});

