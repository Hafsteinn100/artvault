const header = document.querySelector(".site-header");
const searchForms = document.querySelectorAll(".search-form");
const searchInputs = document.querySelectorAll('.search-form input[type="search"]');
const filterCheckboxes = document.querySelectorAll('input[name="filters"]');

const artworks = [
    {
        title: "Abstract Oil Painting",
        image: "medium-oil.jpg",
        medium: "oil",
        aliases: ["Bloom Study", "Oil"],
    },
    {
        title: "Blue Watercolor Painting",
        image: "medium-watercolor.jpg",
        medium: "watercolor",
        aliases: ["Quiet Interior", "Watercolor"],
    },
    {
        title: "Sculpture Artwork",
        image: "medium-sculpture.jpg",
        medium: "sculpture",
        aliases: ["Sculpture"],
    },
    {
        title: "Red Rock Landscape Photograph",
        image: "medium-photography.jpg",
        medium: "photography",
        aliases: ["Spring Canopy", "Photography"],
    },
    {
        title: "Colorful Digital Geometric Artwork",
        image: "medium-digital.jpg",
        medium: "digital",
        aliases: ["Prism Field", "Digital"],
    },
];

let lastScroll = window.scrollY;

function moveNavbar() {
    if (!header) return;

    const currentScroll = window.scrollY;
    const isHomepage =
        !document.body.classList.contains("search-page") &&
        !document.body.classList.contains("profile-page") &&
        !document.body.classList.contains("details-page");

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
    const params = new URLSearchParams(window.location.search);
    const searchText = params.get("q");

    if (searchText) {
        searchInputs.forEach((input) => {
            input.value = searchText;
        });
    }
}

function resizeMasonryGrid(grid) {
    const cards = Array.from(grid.querySelectorAll(".search-result-card"));
    if (!cards.length) return;

    const styles = getComputedStyle(grid);
    const gap = parseFloat(styles.columnGap || styles.gap) || 20;
    const minColumnWidth =
        parseFloat(styles.getPropertyValue("--masonry-column-min")) || 210;
    const gridWidth = grid.clientWidth;
    const columnCount = Math.max(
        1,
        Math.floor((gridWidth + gap) / (minColumnWidth + gap)),
    );
    const columnWidth = (gridWidth - gap * (columnCount - 1)) / columnCount;
    const columnHeights = Array(columnCount).fill(0);

    cards.forEach((card) => {
        card.style.width = `${columnWidth}px`;
    });

    cards.forEach((card) => {
        const shortestColumnHeight = Math.min(...columnHeights);
        const columnIndex = columnHeights.indexOf(shortestColumnHeight);
        const x = columnIndex * (columnWidth + gap);
        const y = shortestColumnHeight;

        card.style.transform = `translate(${x}px, ${y}px)`;
        columnHeights[columnIndex] = y + card.getBoundingClientRect().height + gap;
    });

    grid.style.height = `${Math.max(...columnHeights) - gap}px`;
}

function setupBrowseMasonry() {
    const grid = document.querySelector(".search-browse-strip");
    if (!grid) return;

    const resize = () => requestAnimationFrame(() => resizeMasonryGrid(grid));
    grid.classList.add("is-masonry-ready");

    grid.querySelectorAll("img").forEach((img) => {
        if (img.complete) return;
        img.addEventListener("load", resize, { once: true });
    });

    resize();
    window.addEventListener("load", resize);
    window.addEventListener("resize", resize);
}

moveNavbar();
loadNavbarProfile();
fillSearchBox();
setupBrowseMasonry();

window.addEventListener("scroll", moveNavbar, { passive: true });
