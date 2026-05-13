const header = document.querySelector(".site-header");
const pageSearchInput = document.querySelector("#page-search-input");

// Makes the navbar easier to read after the page moves a little.
function checkNavbar() {
  if (!header) return;

  header.classList.toggle("is-scrolled", window.scrollY > 12);
}

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
