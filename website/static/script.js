toggleMenu = () => {
  let menu = document.getElementById("menu");
  let overlay = document.getElementById("overlay");
  let opacity = Number(menu.style.opacity);
  let menuZIndex = Number(menu.style.zIndex);
  let overlayZIndex = Number(overlay.style.zIndex);
  menu.style.zIndex = -menuZIndex;
  overlay.style.zIndex = -overlayZIndex;
  menu.style.opacity = opacity == 0 ? 1 : 0;
  overlay.style.opacity = opacity == 0 ? 0.5 : 0;
};

let currentBookID = 0;

function openModal(id, title) {
  let modal = document.getElementById("modal");
  modal.style.display = "block";
  overlay.style.opacity = 0.5;

  let bookspan = document.getElementById("book");
  bookspan.innerHTML = `You are checking out <i> ${title} </i> (ID${id})`;
  currentBookID = id;
}

function checkOutBook() {
  let nameInput = document.getElementById("name");
  let name = nameInput.value;

  fetch("/check-out", {
    method: "POST",
    body: JSON.stringify({ id: currentBookID, name: name }),
  }).then((_res) => {
    window.location.href = "/library";
  });
}

closeModal = () => {
  let modal = document.getElementById("modal");
  modal.style.display = "none";
  overlay.style.opacity = 0;
};

function checkInBook(id) {
  fetch("/check-in", {
    method: "POST",
    body: JSON.stringify({ id: id }),
  }).then((_res) => {
    window.location.href = "/librarian";
  });
}

let returnHome = () => {
  window.location.href = "/";
};

let librarianAuth = () => {
  let overlay = document.getElementById("librarian-login-overlay");
  let entered_passwd = document.getElementById("librarian-password").value;
  if (entered_passwd == "jeeb") {
    window.location.href = "/librarian";
  }
};
