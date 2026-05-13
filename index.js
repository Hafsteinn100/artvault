const header = document.querySelector(".site-header");

function updateHeaderGlass() {
  header.classList.toggle("is-scrolled", window.scrollY > 12);
}

updateHeaderGlass();
window.addEventListener("scroll", updateHeaderGlass, { passive: true });

document.addEventListener("DOMContentLoaded", function () {
    const img = document.getElementById("homepage-profile");

    const savedImage = localStorage.getItem("profileImage");

    img.src = savedImage || "profile.png";
});