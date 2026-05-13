const header = document.querySelector(".site-header");
const pageSearchInput = document.querySelector("#page-search-input");

checkNavbar();
window.addEventListener("scroll", checkNavbar, { passive: true });

// If someone searches from the home page, keep their text in the big box.
if (pageSearchInput) {
  const params = new URLSearchParams(window.location.search);
  const searchText = params.get("q");

  if (searchText) {
    pageSearchInput.value = searchText;
  }
}

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


