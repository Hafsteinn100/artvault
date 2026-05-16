const bidsView = document.getElementById("bids-view");
const finalizeView = document.getElementById("finalize-view");
const finalizeTitle = document.getElementById("finalize-title");
const finalizeSubtitle = document.getElementById("finalize-subtitle");
const finalizeForm = document.getElementById("finalize-form");
const finalizeSteps = ["contact", "payment", "review", "confirmation"];
let currentStep = 0;

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

document.querySelectorAll(".finalize-trigger").forEach((button) => {
  button.addEventListener("click", () => openFinalization(button));
});

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
