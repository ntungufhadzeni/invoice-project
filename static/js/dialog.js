// Create a new Bootstrap Modal instance, targeting an element with the ID "modal"
const modal = new bootstrap.Modal(document.getElementById("modal"));

// Listen for the htmx "htmx:afterSwap" event
htmx.on("htmx:afterSwap", (e) => {
  // If the response targets an element with the ID "dialog," show the modal
  if (e.detail.target.id == "dialog") {
    modal.show();
  }
});

// Listen for the htmx "htmx:beforeSwap" event
htmx.on("htmx:beforeSwap", (e) => {
  // If the response targets an element with the ID "dialog" and the response is empty, hide the modal
  if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
    modal.hide();
    // Prevent the default swapping behavior
    e.detail.shouldSwap = false;
  }
});

// Listen for the "hidden.bs.modal" event (Bootstrap event) on the modal
htmx.on("hidden.bs.modal", () => {
  // Clear the content of the element with the ID "dialog" after the modal is hidden
  document.getElementById("dialog").innerHTML = "";
});
