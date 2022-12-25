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
