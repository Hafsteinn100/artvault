const sellers = {
    lisa: {
        name: "Lisa",
        image: "lisa.png",
        description: "Oil painter from Iceland.",
        location: "Reykjavik"
    },

    john: {
        name: "John",
        image: "john.png",
        description: "Digital artist and sculptor.",
        location: "London"
    },

    emma: {
        name: "Emma",
        image: "emma.png",
        description: "Watercolor specialist.",
        location: "Paris"
    }
};

const params = new URLSearchParams(window.location.search);

const sellerId = params.get("seller");

const seller = sellers[sellerId];

if (seller) {

    document.getElementById("seller-name").textContent =
        seller.name;

    document.getElementById("seller-image").src =
        seller.image;

    document.getElementById("seller-description").textContent =
        seller.description;

    document.getElementById("seller-location").textContent =
        seller.location;
}