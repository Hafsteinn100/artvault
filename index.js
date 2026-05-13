const header = document.querySelector(".site-header");
const pageSearchInput = document.querySelector("#page-search-input");

let lastScroll = window.scrollY;

function moveNavbar() {
    if (!header) return;

    const currentScroll = window.scrollY;
    const isHomepage =
        !document.body.classList.contains("search-page") &&
        !document.body.classList.contains("profile-page");

    if (isHomepage) {
        header.classList.toggle("is-scrolled", currentScroll > 12);
        header.classList.remove("is-hidden");
    } else {
        header.classList.add("is-scrolled");

        if (currentScroll <= 10 || currentScroll < lastScroll) {
            header.classList.remove("is-hidden");
        } else if (currentScroll > lastScroll) {
            header.classList.add("is-hidden");
        }
    }

    lastScroll = currentScroll;
}

function loadNavbarProfile() {
    const img = document.getElementById("homepage-profile");
    const name = document.getElementById("homepage-username");

    if (!img) return;

    img.src = localStorage.getItem("profileImage") || "profile.png";

    if (name) {
        name.textContent = localStorage.getItem("profileName") || "";
    }
}

function fillSearchBox() {
    if (!pageSearchInput) return;

    const params = new URLSearchParams(window.location.search);
    const searchText = params.get("q");

    if (searchText) {
        pageSearchInput.value = searchText;
    }
}

moveNavbar();
loadNavbarProfile();
fillSearchBox();

window.addEventListener("scroll", moveNavbar, { passive: true });
