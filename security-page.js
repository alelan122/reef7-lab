// Pagina Sicurezza: la lista finale si spunta; con due sì il pulsante si accende.
(() => {
  const list = document.querySelector(".sec-check-i");
  if (!list) return;
  const box = document.querySelector(".sec-final-cta"), ok = box.querySelector(".sec-final-ok");
  list.addEventListener("change", () => {
    const n = list.querySelectorAll("input:checked").length;
    box.classList.toggle("on", n >= 2);
    ok.textContent = n >= 2 ? ok.dataset.ok : "";
  });
})();
