(function () {
  // Get references to the toast element and its body
  const toastElement = document.getElementById("toast");
  const toastBody = document.getElementById("toast-body");

  // Create a new Bootstrap Toast instance with a delay of 2000 milliseconds (2 seconds)
  const toast = new bootstrap.Toast(toastElement, { delay: 2000 });

  // Listen for a custom htmx event named "showMessage"
  htmx.on("showMessage", (e) => {
    console.log(e.detail.value);

    // Set the text content of the toast body to the value of the "showMessage" event
    toastBody.innerText = e.detail.value;

    // Show the toast
    toast.show();
  });
})();
