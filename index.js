const header = document.querySelector(".site-header");
const searchTerm = document.querySelector("#search-term");

function updateHeaderGlass() {
  header.classList.toggle("is-scrolled", window.scrollY > 12);
}

updateHeaderGlass();
window.addEventListener("scroll", updateHeaderGlass, { passive: true });

if (searchTerm) {
  const params = new URLSearchParams(window.location.search);
  searchTerm.textContent = params.get("q") || "{search}";
}
