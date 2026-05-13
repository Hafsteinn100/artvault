const header = document.querySelector(".site-header");

function updateHeaderGlass() {
  header.classList.toggle("is-scrolled", window.scrollY > 12);
}

updateHeaderGlass();
window.addEventListener("scroll", updateHeaderGlass, { passive: true });

document.addEventListener("DOMContentLoaded", function () {
    const img = document.getElementById("homepage-profile");
    const name = document.getElementById("homepage-username"); // optional if you display it

    const savedImage = localStorage.getItem("profileImage");
    const savedName = localStorage.getItem("profileName");

    img.src = savedImage || "profile.png";

    if (name && savedName) {
        name.textContent = savedName;
    }
});