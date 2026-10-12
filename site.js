// Reef 7 Lab: luce dell'acqua nell'hero, menu su telefono, modulo contatti.
(() => {
  const top = document.querySelector(".top");
  const menu = document.querySelector(".menu");
  const label = menu.textContent;
  menu.addEventListener("click", () => {
    const open = top.classList.toggle("open");
    menu.setAttribute("aria-expanded", String(open));
    menu.textContent = open ? menu.dataset.close : label;
  });

  // modulo contatti: invia la richiesta via FormSubmit (arriva nella casella email del Lab) e mostra la conferma
  const form = document.getElementById("contact-form");
  if (form) form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const d = form.dataset;
    const msg = form.querySelector(".form-msg");
    const btn = form.querySelector('button[type="submit"]');
    msg.textContent = "";

    // controllo dei campi obbligatori, con il campo sbagliato evidenziato
    let firstBad = null;
    form.querySelectorAll("[required]").forEach((el) => {
      const bad = el.type === "checkbox" ? !el.checked : !el.value.trim() || (el.type === "email" && !el.validity.valid);
      el.closest(".field, .check").classList.toggle("invalid", bad);
      if (bad && !firstBad) firstBad = el;
    });
    if (firstBad) { firstBad.focus(); return; }

    const f = new FormData(form);
    if (f.get("_honey")) return; // compilato solo dai bot
    const label = btn.innerHTML;
    btn.disabled = true;
    btn.textContent = d.sending;
    try {
      const res = await fetch(d.endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({
          _subject: `${d.subject}: ${f.get("servizio")} · ${f.get("nome")}`,
          _replyto: f.get("email"),
          _template: "table",
          _captcha: "false",
          Nome: f.get("nome"), Email: f.get("email"), Azienda: f.get("azienda") || "—",
          Servizio: f.get("servizio"), Messaggio: f.get("messaggio"),
        }),
      });
      const out = await res.json().catch(() => ({}));
      if (!res.ok || out.success === false || out.success === "false") throw new Error(out.message || res.status);
      form.hidden = true;
      form.parentElement.querySelector(".form-ok").hidden = false;
    } catch {
      msg.innerHTML = `${d.err} <a href="mailto:${d.email}">${d.email}</a>.`;
      btn.disabled = false;
      btn.innerHTML = label;
    }
  });
  if (form) form.addEventListener("input", (e) => e.target.closest(".field, .check")?.classList.remove("invalid"));

  // prima/dopo: gli strumenti partono sparsi e, quando la sezione entra nello schermo, si collegano al centro
  const eco = document.querySelector("[data-eco]");
  if (eco) {
    const buttons = eco.querySelectorAll(".eco-toggle button");
    const set = (after) => {
      eco.classList.toggle("is-after", after);
      buttons.forEach((b) => b.setAttribute("aria-pressed", String((b.dataset.state === "after") === after)));
    };
    buttons.forEach((b) => b.addEventListener("click", () => set(b.dataset.state === "after")));
    if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      set(false);
      const io = new IntersectionObserver(([e]) => {
        if (!e.isIntersecting) return;
        io.disconnect();
        setTimeout(() => set(true), 700);
      }, { threshold: 0.45 });
      io.observe(eco.querySelector(".eco-stage"));
    }
  }

  // caustiche: la luce che filtra dalla superficie e danza sul fondale (shader WebGL)
  const canvas = document.getElementById("water");
  if (!canvas || !canvas.offsetParent) return; // nella versione B il canvas è nascosto
  const gl = canvas.getContext("webgl", { antialias: false, alpha: true, premultipliedAlpha: false });
  if (!gl) return;
  const vs = "attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}";
  const fs = `precision mediump float;
uniform vec2 r;uniform float t;
float caustic(vec2 uv,float time){
  vec2 p=mod(uv*6.2831,6.2831)-250.;vec2 i=p;float c=1.;float inten=.005;
  for(int n=0;n<4;n++){float tt=time*(1.-(3.5/float(n+1)));
    i=p+vec2(cos(tt-i.x)+sin(tt+i.y),sin(tt-i.y)+cos(tt+i.x));
    c+=1./length(vec2(p.x/(sin(i.x+tt)/inten),p.y/(cos(i.y+tt)/inten)));}
  c/=4.;c=1.17-pow(c,1.4);return pow(abs(c),8.);}
void main(){
  vec2 uv=gl_FragCoord.xy/r;vec2 q=vec2(uv.x*r.x/r.y,uv.y)*.55;
  float c=caustic(q,t*.18);
  float depth=smoothstep(0.,1.,uv.y);
  vec3 deep=vec3(.016,.031,.059);vec3 mid=vec3(.03,.16,.32);vec3 lit=vec3(.37,.88,.95);
  vec3 col=mix(deep,mid,depth*.9);
  col+=lit*c*(.18+.55*depth);
  float rays=pow(max(0.,sin((uv.x+uv.y*.35)*9.+t*.25)*.5+.5),6.)*depth*.12;
  col+=lit*rays;
  gl_FragColor=vec4(col,1.);}`;
  const sh = (type, src) => { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); return s; };
  const prog = gl.createProgram();
  gl.attachShader(prog, sh(gl.VERTEX_SHADER, vs));
  gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, fs));
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return;
  gl.useProgram(prog);
  gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(prog, "p");
  gl.enableVertexAttribArray(loc);
  gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  const uR = gl.getUniformLocation(prog, "r"), uT = gl.getUniformLocation(prog, "t");

  // risoluzione ridotta: l'effetto è morbido e resta leggero anche sui portatili
  const resize = () => {
    const scale = Math.min(window.devicePixelRatio || 1, 1) * 0.6;
    canvas.width = Math.max(1, canvas.clientWidth * scale);
    canvas.height = Math.max(1, canvas.clientHeight * scale);
    gl.viewport(0, 0, canvas.width, canvas.height);
  };
  resize();
  window.addEventListener("resize", resize);

  const still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let visible = true;
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(canvas);
  const start = performance.now();
  const frame = (now) => {
    if (visible) {
      gl.uniform2f(uR, canvas.width, canvas.height);
      gl.uniform1f(uT, still ? 12 : (now - start) / 1000 + 12);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    }
    if (!still) requestAnimationFrame(frame);
  };
  requestAnimationFrame(frame);
})();
