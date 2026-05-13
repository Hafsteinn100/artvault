const form = document.getElementById("profile-form");
const imageInput = document.getElementById("profile-image");
const preview = document.getElementById("profile-preview");
const resetBtn = document.getElementById("reset-profile");
const status = document.getElementById("status-message");
const nameInput = document.getElementById("name");

const defaultImage = "profile.png";

let selectedImage = null;

// LOAD SAVED DATA
const savedImage = localStorage.getItem("profileImage");
const savedName = localStorage.getItem("profileName");

preview.src = savedImage || defaultImage;
nameInput.value = savedName || nameInput.value;

// IMAGE PREVIEW ONLY
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

// SAVE ONLY ON UPDATE
form.addEventListener("submit", function (e) {
    e.preventDefault();

    // save name
    localStorage.setItem("profileName", nameInput.value);

    // save image only if changed
    if (selectedImage) {
        localStorage.setItem("profileImage", selectedImage);
    }

    status.textContent = "Profile updated successfully!";
    status.style.color = "green";
    status.style.display = "block";
});

// RESET PROFILE
resetBtn.addEventListener("click", function () {
    localStorage.removeItem("profileImage");
    localStorage.removeItem("profileName");

    selectedImage = null;
    preview.src = defaultImage;
    nameInput.value = "Lisa";

    status.textContent = "Profile reset to default.";
    status.style.color = "blue";
    status.style.display = "block";
});