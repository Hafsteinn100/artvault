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

const sellerPages = {
    "mira-vale": {
        name: "Mira Vale",
        bio: "Contemporary painter and curator based in Reykjavik, listing original oil, watercolor, and mixed media works for collectors.",
        about: "Mira works with layered pigments, quiet architectural forms, and warm earth tones. Each listing includes condition details, shipping notes, and bid windows before purchase finalization.",
        listings: "12",
        sales: "48",
        rating: "4.9",
        cover: "coverimg2verklegt2.webp",
        coverAlt: "Framed artwork displayed above an orange sofa",
        avatar: "profile.png",
        artworks: [
            {
                title: "Abstract Oil Painting",
                img: "medium-oil.jpg",
                alt: "Abstract oil painting",
                price: "$1,200",
            },
            {
                title: "Green Gallery Study",
                img: "pexels-minan1398-813269.jpg",
                alt: "Green gallery study",
                price: "$1,100",
            },
            {
                title: "Oil Paint Study",
                img: "/media/artwork_images/oilpaint1.jpeg",
                alt: "Oil paint study",
                price: "$1,050",
            },
        ],
    },
    "theo-rowan": {
        name: "Theo Rowan",
        bio: "Watercolor artist focused on atmospheric studies, soft city scenes, and calm interior pieces.",
        about: "Theo's listings lean toward gentle color, layered washes, and compact works that fit easily into private collections.",
        listings: "8",
        sales: "31",
        rating: "4.8",
        cover: "medium-watercolor.jpg",
        coverAlt: "Blue watercolor painting",
        avatar: "profile.png",
        artworks: [
            {
                title: "Blue Watercolor Painting",
                img: "medium-watercolor.jpg",
                alt: "Blue watercolor painting",
                price: "$650",
            },
            {
                title: "Urban Collection Study",
                img: "pexels-ricky-kwong-113005840-35589498.jpg",
                alt: "Urban collection study",
                price: "$1,150",
            },
        ],
    },
    "lena-hart": {
        name: "Lena Hart",
        bio: "Gallery seller specializing in sculpture, landscape studies, and tactile contemporary pieces.",
        about: "Lena presents selected works from studio visits and gallery consignments, with emphasis on material quality and provenance.",
        listings: "10",
        sales: "27",
        rating: "4.7",
        cover: "medium-sculpture.jpg",
        coverAlt: "Sculpture artwork",
        avatar: "profile.png",
        artworks: [
            {
                title: "Sculpture Artwork",
                img: "medium-sculpture.jpg",
                alt: "Sculpture artwork",
                price: "$2,400",
            },
            {
                title: "Landscape Collection Study",
                img: "pexels-sarmat-batagov-776392502-35072454.jpg",
                alt: "Landscape collection study",
                price: "$1,200",
            },
        ],
    },
    "niko-stone": {
        name: "Niko Stone",
        bio: "Photographer and digital seller listing landscape photographs, studies, and editioned visual work.",
        about: "Niko's work centers on color, distance, and outdoor light, with listings prepared for collectors looking for bold wall pieces.",
        listings: "9",
        sales: "36",
        rating: "4.9",
        cover: "medium-photography.jpg",
        coverAlt: "Red rock landscape photograph",
        avatar: "profile.png",
        artworks: [
            {
                title: "Red Rock Landscape Photograph",
                img: "medium-photography.jpg",
                alt: "Red rock landscape photograph",
                price: "$900",
            },
            {
                title: "Digital Artwork Study",
                img: "/media/artwork_images/digitalart1.jpeg",
                alt: "Digital artwork study",
                price: "$750",
            },
        ],
    },
    "iris-calder": {
        name: "Iris Calder",
        bio: "Digital artist building vivid geometric works and painterly studies for contemporary collectors.",
        about: "Iris mixes digital composition with bold color systems, offering accessible pieces and higher-value edition studies.",
        listings: "11",
        sales: "44",
        rating: "4.9",
        cover: "medium-digital.jpg",
        coverAlt: "Colorful digital geometric artwork",
        avatar: "profile.png",
        artworks: [
            {
                title: "Colorful Digital Geometric Artwork",
                img: "medium-digital.jpg",
                alt: "Colorful digital geometric artwork",
                price: "$480",
            },
            {
                title: "Oil Paint Study",
                img: "/media/artwork_images/oilpaint1.jpeg",
                alt: "Oil paint study",
                price: "$1,050",
            },
        ],
    },
    "sam-elvar": {
        name: "Sam Elvar",
        bio: "Collector-seller with featured gallery works and warm residential display pieces.",
        about: "Sam lists selected works from private collections, focusing on pieces that are already framed or display-ready.",
        listings: "6",
        sales: "19",
        rating: "4.6",
        cover: "coverimg2verklegt2.webp",
        coverAlt: "Framed artwork displayed above an orange sofa",
        avatar: "profile.png",
        artworks: [
            {
                title: "Featured Gallery Artwork",
                img: "coverimg2verklegt2.webp",
                alt: "Featured gallery artwork",
                price: "$700",
            },
        ],
    },
};

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

function sellerSlug(name) {
    return name
        .trim()
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/^-|-$/g, "");
}

function sellerPageUrl(name) {
    return `seller.html?seller=${encodeURIComponent(sellerSlug(name))}`;
}

function setupSellerLinks() {
    const sellerChips = document.querySelectorAll(".browse-seller, .latest-seller");

    sellerChips.forEach((chip) => {
        if (chip.classList.contains("browse-seller")) {
            const artworkLink = chip.closest("a");
            const resultCard = artworkLink ? artworkLink.closest(".search-result-card") : null;

            if (artworkLink && resultCard && chip.parentElement === artworkLink) {
                artworkLink.after(chip);
            }
        }

        const nameElement = chip.querySelector(".seller-name, .latest-seller-name");
        if (!nameElement) return;

        const sellerName = nameElement.textContent.trim();
        if (!sellerName) return;

        chip.setAttribute("role", "link");
        chip.setAttribute("tabindex", "0");
        chip.setAttribute("aria-label", `View seller page for ${sellerName}`);

        const openSeller = (event) => {
            event.preventDefault();
            event.stopPropagation();
            window.location.href = sellerPageUrl(sellerName);
        };

        chip.addEventListener("click", openSeller);
        chip.addEventListener("keydown", (event) => {
            if (event.key !== "Enter" && event.key !== " ") return;
            openSeller(event);
        });
    });
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

    const masonryGrid = document.querySelector(".search-browse-strip.is-masonry-ready");
    if (masonryGrid) {
        requestAnimationFrame(() => resizeMasonryGrid(masonryGrid));
    }
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

function createSellerArtworkCard(artwork) {
    const article = document.createElement("article");
    article.className = "search-result-card";

    const link = document.createElement("a");
    const detailsParams = new URLSearchParams({
        img: artwork.img,
        title: artwork.title,
    });
    link.href = `details.html?${detailsParams.toString()}`;

    const image = document.createElement("img");
    image.src = artwork.img;
    image.alt = artwork.alt;

    const price = document.createElement("span");
    price.className = "browse-price";
    price.textContent = artwork.price;

    link.append(image, price);
    article.append(link);

    return article;
}

function loadSellerPage() {
    if (!document.body.classList.contains("seller-page")) return;

    const params = new URLSearchParams(window.location.search);
    const selectedSeller = params.get("seller") || "mira-vale";
    const seller = sellerPages[selectedSeller] || sellerPages["mira-vale"];

    document.title = `${seller.name} - ArtVault`;

    const cover = document.querySelector(".seller-cover");
    const avatar = document.querySelector(".seller-avatar-large");
    const name = document.getElementById("seller-name");
    const bio = document.getElementById("seller-bio");
    const about = document.getElementById("seller-about-text");
    const listings = document.getElementById("seller-listing-count");
    const sales = document.getElementById("seller-sales-count");
    const rating = document.getElementById("seller-rating");
    const grid = document.getElementById("seller-art-grid");

    if (cover) {
        cover.src = seller.cover;
        cover.alt = seller.coverAlt;
    }

    if (avatar) {
        avatar.src = seller.avatar;
        avatar.alt = seller.name;
    }

    if (name) name.textContent = seller.name;
    if (bio) bio.textContent = seller.bio;
    if (about) about.textContent = seller.about;
    if (listings) listings.textContent = seller.listings;
    if (sales) sales.textContent = seller.sales;
    if (rating) rating.textContent = seller.rating;

    if (grid) {
        grid.replaceChildren(...seller.artworks.map(createSellerArtworkCard));
    }
}

function resizeMasonryGrid(grid) {
    const cards = Array.from(grid.querySelectorAll(".search-result-card")).filter(
        (card) => !card.hidden,
    );
    if (!cards.length) {
        grid.style.height = "0px";
        return;
    }

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

function createSocialModal() {
    const modal = document.createElement("div");
    modal.className = "social-modal";
    modal.hidden = true;
    modal.innerHTML = `
        <div class="social-modal-backdrop" data-social-modal-close></div>
        <section
            class="social-modal-panel"
            role="dialog"
            aria-modal="true"
            aria-labelledby="social-modal-title"
        >
            <button
                class="social-modal-close"
                type="button"
                aria-label="Close social media message"
                data-social-modal-close
            >
                &times;
            </button>
            <div class="social-modal-icons" aria-hidden="true">
                <i class="fa-brands fa-instagram"></i>
                <i class="fa-brands fa-x-twitter"></i>
                <i class="fa-brands fa-facebook"></i>
            </div>
            <h2 id="social-modal-title">Our social media will be launching soon!</h2>
            <p>Stay tuned.</p>
        </section>
    `;
    document.body.append(modal);
    return modal;
}

function setupSocialModal() {
    const socialLinks = document.querySelectorAll(
        ".social-icons .instagram-link, .social-icons .social-icon-link",
    );

    if (!socialLinks.length) return;

    const modal = createSocialModal();
    const closeButton = modal.querySelector(".social-modal-close");

    const openModal = (event) => {
        event.preventDefault();
        modal.hidden = false;
        document.body.classList.add("is-social-modal-open");
        closeButton.focus();
    };

    const closeModal = () => {
        modal.hidden = true;
        document.body.classList.remove("is-social-modal-open");
    };

    socialLinks.forEach((link) => {
        link.addEventListener("click", openModal);
    });

    modal.querySelectorAll("[data-social-modal-close]").forEach((element) => {
        element.addEventListener("click", closeModal);
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && !modal.hidden) {
            closeModal();
        }
    });
}

moveNavbar();
loadNavbarProfile();
fillSearchBox();
loadSellerPage();
setupSellerLinks();
setupArtworkSearch();
setupBrowseMasonry();
setupSocialModal();

window.addEventListener("scroll", moveNavbar, { passive: true });
