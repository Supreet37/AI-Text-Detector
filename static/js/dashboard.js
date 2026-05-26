// ===========================
// Veritext — Dashboard scripts
// ===========================

(function () {
  // Total analyses counter from localStorage
  const totalEl = document.getElementById("totalAnalyses");
  if (totalEl) {
    try {
      const history = JSON.parse(localStorage.getItem("detectionHistory") || "[]");
      totalEl.innerText = history.length.toString();
    } catch (e) {
      totalEl.innerText = "0";
    }
  }

  // Mobile sidebar toggle
  const sidebar = document.getElementById("sidebar");
  const backdrop = document.getElementById("sidebarBackdrop");
  const menuBtn = document.getElementById("mobileMenuBtn");

  const closeSidebar = () => {
    if (sidebar) sidebar.classList.remove("open");
  };

  if (menuBtn && sidebar) {
    menuBtn.addEventListener("click", () => {
      sidebar.classList.toggle("open");
    });
  }

  if (backdrop) {
    backdrop.addEventListener("click", closeSidebar);
  }

  // Form validation: shake on invalid input
  const form = document.getElementById("analyzeForm");
  const textarea = document.getElementById("analyzeInput");
  const wrap = document.getElementById("textareaWrap");
  const errorMsg = document.getElementById("errorMsg");
  const errorText = document.getElementById("errorText");
  const charCount = document.getElementById("charCount");
  const clearBtn = document.getElementById("clearBtn");

  // Character counter
  if (textarea && charCount) {
    const updateCount = () => {
      charCount.innerText = textarea.value.length.toString();
    };
    textarea.addEventListener("input", updateCount);
    updateCount();
  }

  // Shake helper
  const triggerShake = (message) => {
    if (!wrap) return;
    if (errorText && message) errorText.innerText = message;
    if (errorMsg) errorMsg.classList.add("show");

    wrap.classList.remove("shake");
    // force reflow so we can replay the animation
    void wrap.offsetWidth;
    wrap.classList.add("shake");

    if (textarea) textarea.focus();
  };

  // Clear error styles when typing
  if (textarea) {
    textarea.addEventListener("input", () => {
      if (wrap) wrap.classList.remove("shake");
      if (errorMsg) errorMsg.classList.remove("show");
    });
  }

  // Intercept submit
  if (form && textarea) {
    form.addEventListener("submit", (e) => {
      const val = textarea.value.trim();
      if (val.length === 0) {
        e.preventDefault();
        triggerShake("Please enter some text before analyzing.");
        return;
      }
      if (val.length < 10) {
        e.preventDefault();
        triggerShake("Text is too short. Please enter at least 10 characters.");
        return;
      }
      // OK — let the form submit to /predict
    });
  }

  // Clear button
  if (clearBtn && textarea) {
    clearBtn.addEventListener("click", () => {
      textarea.value = "";
      if (charCount) charCount.innerText = "0";
      if (wrap) wrap.classList.remove("shake");
      if (errorMsg) errorMsg.classList.remove("show");
      textarea.focus();
    });
  }
})();
