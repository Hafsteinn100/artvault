const form = document.getElementById("profile-form");
const imageInput = document.getElementById("profile-image");
const preview = document.getElementById("profile-preview");
const resetBtn = document.getElementById("reset-profile");
const status = document.getElementById("status-message");

const defaultImage = "profile.png";

let selectedImage = null;

const savedImage = localStorage.getItem("profileImage");
preview.src = savedImage || defaultImage;

imageInput.addEventListener("change", function () {
    const file = this.files[0];

    if (file) {
        const reader = new FileReader();

        reader.onload = function (e) {
            selectedImage = e.target.result;
            preview.src = selectedImage;
        };

        reader.readAsDataURL(file);
    }
});

form.addEventListener("submit", function (e) {
    e.preventDefault();

    if (selectedImage) {
        localStorage.setItem("profileImage", selectedImage);
    }

    status.textContent = "Profile updated successfully!";
    status.style.color = "green";
    status.style.display = "block";
});

resetBtn.addEventListener("click", function () {
    localStorage.removeItem("profileImage");
    selectedImage = null;
    preview.src = defaultImage;

    status.textContent = "Profile reset to default.";
    status.style.color = "blue";
    status.style.display = "block";
});