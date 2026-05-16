const BID_STORAGE_KEY = "artvaultBids";

const artworkDetails = [
  {
    image: "medium-oil.jpg",
    title: "Abstract Oil Painting",
    name: "Bloom Study",
    seller: "Mira Vale",
    currentBid: 1200,
  },
  {
    image: "medium-watercolor.jpg",
    title: "Blue Watercolor Painting",
    name: "Quiet Interior",
    seller: "Theo Rowan",
    currentBid: 650,
  },
  {
    image: "medium-sculpture.jpg",
    title: "Sculpture Artwork",
    name: "Sculpture Artwork",
    seller: "Lena Hart",
    currentBid: 2400,
  },
  {
    image: "medium-photography.jpg",
    title: "Red Rock Landscape Photograph",
    name: "Spring Canopy",
    seller: "Niko Stone",
    currentBid: 900,
  },
  {
    image: "medium-digital.jpg",
    title: "Colorful Digital Geometric Artwork",
    name: "Prism Field",
    seller: "Iris Calder",
    currentBid: 480,
  },
  {
    image: "coverimg2verklegt2.webp",
    title: "Featured Gallery Artwork",
    name: "Featured Gallery Artwork",
    seller: "Sam Elvar",
    currentBid: 700,
  },
  {
    image: "pexels-minan1398-813269.jpg",
    title: "Green Gallery Study",
    name: "Green Gallery Study",
    seller: "Mira Vale",
    currentBid: 1100,
  },
  {
    image: "pexels-ricky-kwong-113005840-35589498.jpg",
    title: "Urban Collection Study",
    name: "Urban Collection Study",
    seller: "Theo Rowan",
    currentBid: 1150,
  },
  {
    image: "pexels-sarmat-batagov-776392502-35072454.jpg",
    title: "Landscape Collection Study",
    name: "Landscape Collection Study",
    seller: "Lena Hart",
    currentBid: 1200,
  },
  {
    image: "/media/artwork_images/digitalart1.jpeg",
    title: "Digital Artwork Study",
    name: "Digital Artwork Study",
    seller: "Niko Stone",
    currentBid: 750,
  },
  {
    image: "/media/artwork_images/oilpaint1.jpeg",
    title: "Oil Paint Study",
    name: "Oil Paint Study",
    seller: "Iris Calder",
    currentBid: 1050,
  },
  {
    image: "colorful-abstract-painting.jpg",
    title: "Golden Abstract Painting",
    name: "Golden Abstract Painting",
    seller: "Mira Vale",
    currentBid: 1300,
  },
  {
    image: "painting (1).jpg",
    title: "Pine Ridge Study",
    name: "Pine Ridge Study",
    seller: "Theo Rowan",
    currentBid: 620,
  },
  {
    image: "painting(2).jpg",
    title: "Blue River Pattern",
    name: "Blue River Pattern",
    seller: "Iris Calder",
    currentBid: 820,
  },
  {
    image: "painting(3).jpg",
    title: "Hill Pasture Study",
    name: "Hill Pasture Study",
    seller: "Lena Hart",
    currentBid: 950,
  },
  {
    image: "paintingclowds.jpg",
    title: "Cloud Veil Abstract",
    name: "Cloud Veil Abstract",
    seller: "Sam Elvar",
    currentBid: 1400,
  },
  {
    image: "paintingflower.jpg",
    title: "Flower Orbit Study",
    name: "Flower Orbit Study",
    seller: "Mira Vale",
    currentBid: 780,
  },
];

const detailsParams = new URLSearchParams(window.location.search);
const selectedImage = detailsParams.get("img");
const selectedTitle = detailsParams.get("title");
const detailsImage = document.getElementById("selected-artwork-image");
const detailsTitle = document.getElementById("selected-artwork-title");
const detailsDescription = document.getElementById("selected-artwork-description");
const detailsSeller = document.getElementById("selected-artwork-seller");
const detailsPrice = document.getElementById("selected-artwork-price");
const bidForm = document.getElementById("bid-form");
const bidPrice = document.getElementById("bid-price");
const bidMessage = document.getElementById("bid-message");
const bidExpiration = document.getElementById("bid-expiration");

function currency(value) {
  return `$${Number(value).toLocaleString("en-US")}`;
}

function storedBids() {
  try {
    return JSON.parse(localStorage.getItem(BID_STORAGE_KEY)) || [];
  } catch {
    return [];
  }
}

function saveBids(bids) {
  localStorage.setItem(BID_STORAGE_KEY, JSON.stringify(bids));
}

function detailUrl(artwork) {
  const params = new URLSearchParams({
    img: artwork.image,
    title: artwork.title,
  });
  return `details.html?${params.toString()}`;
}

function matchingArtwork() {
  return (
    artworkDetails.find((artwork) => {
      return artwork.image === selectedImage || artwork.title === selectedTitle;
    }) || {
      image: selectedImage || "medium-photography.jpg",
      title: selectedTitle || "Red Rock Landscape Photograph",
      name: selectedTitle || "Spring Canopy",
      seller: "Unknown seller",
      currentBid: 100,
    }
  );
}

const selectedArtwork = matchingArtwork();

function highestBidForArtwork() {
  return storedBids()
    .filter((bid) => bid.artworkTitle === selectedArtwork.name)
    .reduce((highest, bid) => Math.max(highest, Number(bid.price)), selectedArtwork.currentBid);
}

function updateCurrentBidDisplay() {
  const currentBid = highestBidForArtwork();
  detailsPrice.textContent = `Current bid: ${currency(currentBid)}`;
  bidPrice.min = String(currentBid + 1);
  bidPrice.placeholder = `${currentBid + 1} or higher`;
  document.getElementById("bid-rule").textContent =
    `Your bid must be higher than the current bid of ${currency(currentBid)}.`;
}

function setDefaultExpiration() {
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 7);
  tomorrow.setMinutes(tomorrow.getMinutes() - tomorrow.getTimezoneOffset());
  bidExpiration.value = tomorrow.toISOString().slice(0, 16);
}

function renderArtworkDetails() {
  if (selectedImage) {
    detailsImage.src = selectedImage;
  }

  detailsImage.alt = selectedArtwork.title;
  detailsTitle.textContent = selectedArtwork.name;
  detailsDescription.textContent = selectedArtwork.title;
  detailsSeller.textContent = `Seller: ${selectedArtwork.seller}`;
  updateCurrentBidDisplay();
  setDefaultExpiration();
}

function submitBid(event) {
  event.preventDefault();

  const currentBid = highestBidForArtwork();
  const submittedPrice = Number(bidPrice.value);
  const expirationDate = new Date(bidExpiration.value);

  if (submittedPrice <= currentBid) {
    bidMessage.className = "bid-message error";
    bidMessage.textContent = `Bid must be higher than ${currency(currentBid)}.`;
    return;
  }

  if (Number.isNaN(expirationDate.getTime()) || expirationDate <= new Date()) {
    bidMessage.className = "bid-message error";
    bidMessage.textContent = "Expiration date must be in the future.";
    return;
  }

  const now = new Date();
  const newBid = {
    id: `${Date.now()}`,
    artworkTitle: selectedArtwork.name,
    artworkDescription: selectedArtwork.title,
    artworkImage: selectedArtwork.image,
    artworkUrl: detailUrl(selectedArtwork),
    seller: selectedArtwork.seller,
    price: submittedPrice,
    expiration: bidExpiration.value,
    createdAt: now.toISOString(),
    status: "Pending",
  };
  const bids = storedBids().filter((bid) => bid.artworkTitle !== selectedArtwork.name);
  bids.unshift(newBid);
  saveBids(bids);

  bidMessage.className = "bid-message success";
  bidMessage.textContent = "Your bid was submitted successfully and added to My bids.";
  bidPrice.value = "";
  updateCurrentBidDisplay();
}

renderArtworkDetails();
bidForm.addEventListener("submit", submitBid);
