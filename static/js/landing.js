// ===========================
// Veritext — Landing scripts
// ===========================

(function () {
  // Mobile menu toggle
  const toggle = document.getElementById("menuToggle");
  const drawer = document.getElementById("mobileDrawer");

  if (toggle && drawer) {
    toggle.addEventListener("click", () => {
      drawer.classList.toggle("open");
      const icon = toggle.querySelector("i");
      if (icon) {
        icon.className = drawer.classList.contains("open")
          ? "fa-solid fa-xmark"
          : "fa-solid fa-bars";
      }
    });

    // Close drawer when a link is clicked
    drawer.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => {
        drawer.classList.remove("open");
        const icon = toggle.querySelector("i");
        if (icon) icon.className = "fa-solid fa-bars";
      })
    );
  }

  // Reveal-on-scroll
  const revealEls = document.querySelectorAll(
    ".feature-card, .step, .stat, .faq-item, .cta-card, .hero-demo, .hero-title, .hero-sub, .section-head"
  );
  revealEls.forEach((el) => el.classList.add("reveal"));

  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    // Fallback for older browsers
    revealEls.forEach((el) => el.classList.add("in"));
  }

  // Animate stat numbers
  const statNums = document.querySelectorAll(".stat-num");

  const animateStat = (el) => {
    const text = el.textContent.trim();
    const match = text.match(/([\d.]+)/);
    if (!match) return;

    const target = parseFloat(match[1]);
    const isFloat = match[1].includes(".");
    const suffix = el.querySelector("span") ? el.querySelector("span").outerHTML : "";
    let current = 0;
    const duration = 1200;
    const start = performance.now();

    const step = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      const val = target * eased;
      const numStr = isFloat ? val.toFixed(1) : Math.floor(val).toString();
      el.innerHTML = numStr + suffix;
      if (progress < 1) requestAnimationFrame(step);
    };

    requestAnimationFrame(step);
  };

  if ("IntersectionObserver" in window && statNums.length) {
    const statIO = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            animateStat(entry.target);
            statIO.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.4 }
    );
    statNums.forEach((s) => statIO.observe(s));
  } else {
    // Fallback: animate immediately
    statNums.forEach((s) => animateStat(s));
  }
})();
