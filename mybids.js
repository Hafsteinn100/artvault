const BID_STORAGE_KEY = "artvaultBids";
const bidsView = document.getElementById("bids-view");
const finalizeView = document.getElementById("finalize-view");
const finalizeTitle = document.getElementById("finalize-title");
const finalizeSubtitle = document.getElementById("finalize-subtitle");
const finalizeForm = document.getElementById("finalize-form");
const bidsTableBody = document.getElementById("bids-table-body");
const finalizeSteps = ["contact", "payment", "review", "confirmation"];
let currentStep = 0;

const defaultBids = [
  {
    id: "default-bloom-study",
    artworkTitle: "Bloom Study",
    artworkUrl: "details.html?img=medium-oil.jpg&title=Abstract%20Oil%20Painting",
    createdAt: "2026-05-03T14:20:00",
    expiration: "2026-05-24T18:00",
    status: "Pending",
    seller: "Mira Vale",
    price: 1250,
  },
  {
    id: "default-quiet-interior",
    artworkTitle: "Quiet Interior",
    artworkUrl: "details.html?img=medium-watercolor.jpg&title=Blue%20Watercolor%20Painting",
    createdAt: "2026-05-05T10:45:00",
    expiration: "2026-05-28T12:00",
    status: "Accepted",
    seller: "Theo Rowan",
    price: 720,
  },
  {
    id: "default-spring-canopy",
    artworkTitle: "Spring Canopy",
    artworkUrl: "details.html?img=medium-photography.jpg&title=Red%20Rock%20Landscape%20Photograph",
    createdAt: "2026-05-08T16:15:00",
    expiration: "2026-05-26T09:30",
    status: "Rejected",
    seller: "Niko Stone",
    price: 940,
  },
  {
    id: "default-prism-field",
    artworkTitle: "Prism Field",
    artworkUrl: "details.html?img=medium-digital.jpg&title=Colorful%20Digital%20Geometric%20Artwork",
    createdAt: "2026-05-10T11:05:00",
    expiration: "2026-05-30T17:00",
    status: "Contingent",
    seller: "Iris Calder",
    price: 510,
  },
];

function storedBids() {
  try {
    return JSON.parse(localStorage.getItem(BID_STORAGE_KEY)) || [];
  } catch {
    return [];
  }
}

function currency(value) {
  return `$${Number(value).toLocaleString("en-US")}`;
}

function formatDate(value) {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");
  return `${year}-${month}-${day} ${hours}:${minutes}`;
}

function statusClass(status) {
  return status.toLowerCase();
}

function canFinalize(status) {
  return status === "Accepted" || status === "Contingent";
}

function renderBidRow(bid) {
  const row = document.createElement("tr");
  const action = canFinalize(bid.status)
    ? `<button class="text-action finalize-trigger" type="button" data-bid="${bid.artworkTitle}" data-price="${currency(bid.price)}">Finalize</button>`
    : '<span class="muted">Not available</span>';

  row.innerHTML = `
    <td><a href="${bid.artworkUrl}">${bid.artworkTitle}</a></td>
    <td>${formatDate(bid.createdAt)}</td>
    <td>${formatDate(bid.expiration)}</td>
    <td><span class="status ${statusClass(bid.status)}">${bid.status}</span></td>
    <td>${bid.seller}</td>
    <td>${currency(bid.price)}</td>
    <td>${action}</td>
  `;
  return row;
}

function allBids() {
  const submitted = storedBids();
  const submittedTitles = new Set(submitted.map((bid) => bid.artworkTitle));
  return [
    ...submitted,
    ...defaultBids.filter((bid) => !submittedTitles.has(bid.artworkTitle)),
  ];
}

function attachFinalizeButtons() {
  document.querySelectorAll(".finalize-trigger").forEach((button) => {
    button.addEventListener("click", () => openFinalization(button));
  });
}

function renderBids() {
  bidsTableBody.replaceChildren(...allBids().map(renderBidRow));
  attachFinalizeButtons();
}

function selectedPaymentLabel(value) {
  return {
    "credit-card": "Credit card",
    "bank-transfer": "Bank transfer",
    "wire-transfer": "Wire transfer",
  }[value];
}

function renderReview() {
  const data = new FormData(finalizeForm);
  const method = data.get("paymentMethod");
  let paymentDetails = "";

  if (method === "credit-card") {
    paymentDetails = `
      <p><strong>Cardholder name:</strong> ${data.get("cardholder") || ""}</p>
      <p><strong>Credit card number:</strong> ${data.get("cardNumber") || ""}</p>
      <p><strong>Expiry date:</strong> ${data.get("expiry") || ""}</p>
      <p><strong>CVC:</strong> ${data.get("cvc") || ""}</p>
    `;
  } else if (method === "bank-transfer") {
    paymentDetails = `<p><strong>Bank account:</strong> ${data.get("bankAccount") || ""}</p>`;
  } else {
    paymentDetails = `
      <p><strong>Name of sending bank:</strong> ${data.get("sendingBank") || ""}</p>
      <p><strong>Routing number:</strong> ${data.get("routingNumber") || ""}</p>
      <p><strong>Account number:</strong> ${data.get("accountNumber") || ""}</p>
    `;
  }

  document.getElementById("review-output").innerHTML = `
    <h3>Contact information</h3>
    <p><strong>Street name:</strong> ${data.get("street") || ""}</p>
    <p><strong>City:</strong> ${data.get("city") || ""}</p>
    <p><strong>Postal code:</strong> ${data.get("postal") || ""}</p>
    <p><strong>Country:</strong> ${data.get("country") || ""}</p>
    <p><strong>National id:</strong> ${data.get("nationalId") || ""}</p>
    <h3>Payment</h3>
    <p><strong>Payment option:</strong> ${selectedPaymentLabel(method)}</p>
    ${paymentDetails}
  `;
}

function showStep(index) {
  currentStep = Math.max(0, Math.min(index, finalizeSteps.length - 1));

  document.querySelectorAll(".wizard-step").forEach((step) => {
    step.hidden = step.dataset.step !== finalizeSteps[currentStep];
  });

  document.querySelectorAll("[data-step-target]").forEach((button) => {
    button.classList.toggle(
      "is-current",
      button.dataset.stepTarget === finalizeSteps[currentStep],
    );
  });

  document.querySelector("[data-actions]").hidden =
    finalizeSteps[currentStep] === "confirmation";
  document.getElementById("prev-step").hidden = currentStep === 0;
  document.getElementById("next-step").textContent =
    currentStep === 2 ? "Confirm bid" : "Continue";

  if (finalizeSteps[currentStep] === "review") {
    renderReview();
  }
}

function openFinalization(button) {
  bidsView.hidden = true;
  finalizeView.hidden = false;
  finalizeTitle.textContent = `Finalize ${button.dataset.bid}`;
  finalizeSubtitle.textContent = `Bid price ${button.dataset.price}`;
  showStep(0);
}

document.getElementById("back-to-bids").addEventListener("click", () => {
  finalizeView.hidden = true;
  bidsView.hidden = false;
});

document.getElementById("prev-step").addEventListener("click", () => {
  showStep(currentStep - 1);
});

document.getElementById("next-step").addEventListener("click", () => {
  if (currentStep < 2 && !finalizeForm.reportValidity()) return;
  showStep(currentStep + 1);
});

document.querySelectorAll("[data-step-target]").forEach((button) => {
  button.addEventListener("click", () => {
    const targetIndex = finalizeSteps.indexOf(button.dataset.stepTarget);
    if (targetIndex > currentStep && !finalizeForm.reportValidity()) return;
    showStep(targetIndex);
  });
});

document.getElementById("payment-method").addEventListener("change", (event) => {
  document.querySelectorAll("[data-payment]").forEach((section) => {
    section.hidden = section.dataset.payment !== event.target.value;
  });
});

renderBids();
