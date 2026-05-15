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

function normalizeSearchText(text) {
    return text.trim().toLowerCase();
}

function artworkMatchesSearch(artwork, searchText) {
    const normalizedSearch = normalizeSearchText(searchText);

    if (!normalizedSearch) return true;

    const searchWords = normalizedSearch.split(/\s+/);
    const searchableNames = [artwork.title, ...artwork.aliases].map((name) =>
        normalizeSearchText(name)
    );

    return searchWords.every((word) =>
        searchableNames.some((name) => name.includes(word))
    );
}

function getSelectedFilters() {
    return Array.from(filterCheckboxes)
        .filter((checkbox) => checkbox.checked)
        .map((checkbox) => checkbox.value);
}

function artworkMatchesFilters(artwork, selectedFilters) {
    if (!selectedFilters.length) return true;

    return selectedFilters.includes(artwork.medium);
}

function getArtworkFromCard(card) {
    const link = card.querySelector("a");

    if (!link) return null;

    const url = new URL(link.href);
    const title = url.searchParams.get("title");
    const image = url.searchParams.get("img");

    return artworks.find((artwork) => artwork.title === title) || {
        title,
        image,
        medium: "",
        aliases: [card.querySelector("img")?.alt || ""],
    };
}

function filterArtworkCards(searchText, selectedFilters = getSelectedFilters()) {
    const isSearchPage = document.body.classList.contains("search-page");
    const hasActiveFilter =
        Boolean(normalizeSearchText(searchText)) || selectedFilters.length > 0;

    if (!isSearchPage) return;

    document.querySelectorAll(".search-result-card").forEach((card) => {
        if (card.classList.contains("empty-card")) {
            card.hidden = hasActiveFilter;
            return;
        }

        const artwork = getArtworkFromCard(card);
        card.hidden =
            !artwork ||
            !artworkMatchesSearch(artwork, searchText) ||
            !artworkMatchesFilters(artwork, selectedFilters);
    });
}

function setupArtworkSearch() {
    const isSearchPage = document.body.classList.contains("search-page");

    if (isSearchPage) {
        const params = new URLSearchParams(window.location.search);
        filterArtworkCards(params.get("q") || "");
    }

    searchInputs.forEach((input) => {
        input.addEventListener("input", () => {
            if (!isSearchPage) return;

            searchInputs.forEach((otherInput) => {
                if (otherInput !== input) {
                    otherInput.value = input.value;
                }
            });

            filterArtworkCards(input.value);
        });
    });

    filterCheckboxes.forEach((checkbox) => {
        checkbox.addEventListener("change", () => {
            const searchText = searchInputs[0]?.value || "";

            filterArtworkCards(searchText);
        });
    });

    searchForms.forEach((form) => {
        form.addEventListener("submit", (event) => {
            if (!isSearchPage) return;

            const input = form.querySelector('input[type="search"]');
            const searchText = input?.value || "";
            const url = new URL(window.location.href);

            if (normalizeSearchText(searchText)) {
                url.searchParams.set("q", searchText);
            } else {
                url.searchParams.delete("q");
            }

            event.preventDefault();
            window.history.replaceState({}, "", url);
            filterArtworkCards(searchText);
        });
    });
}

moveNavbar();
loadNavbarProfile();
fillSearchBox();
setupArtworkSearch();

window.addEventListener("scroll", moveNavbar, { passive: true });
