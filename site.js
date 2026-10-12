// Reef 7 Lab: menu su telefono, anno, modulo contatti che apre l'email.
(() => {
  const email = (window.REEF || {}).email;
  const top = document.querySelector(".top");
  const menu = document.querySelector(".menu");
  const label = menu.textContent;
  menu.addEventListener("click", () => {
    const open = top.classList.toggle("open");
    menu.setAttribute("aria-expanded", String(open));
    menu.textContent = open ? menu.dataset.close : label;
  });

  const form = document.getElementById("contact-form");
  if (form) form.addEventListener("submit", (e) => {
    e.preventDefault();
    const f = new FormData(form);
    const who = `${f.get("nome")}${f.get("azienda") ? ` (${f.get("azienda")})` : ""}`;
    const subject = `${f.get("servizio")} · ${who}`;
    const body = `${f.get("messaggio")}\n\n${who}`;
    window.location.href = `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  });
})();
