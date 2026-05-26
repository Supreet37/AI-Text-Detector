// ===========================
// Veritext — Result scripts
// ===========================

(function () {
  // Mobile sidebar toggle
  const sidebar = document.getElementById("sidebar");
  const backdrop = document.getElementById("sidebarBackdrop");
  const menuBtn = document.getElementById("mobileMenuBtn");

  if (menuBtn && sidebar) {
    menuBtn.addEventListener("click", () => {
      sidebar.classList.toggle("open");
    });
  }

  if (backdrop && sidebar) {
    backdrop.addEventListener("click", () => {
      sidebar.classList.remove("open");
    });
  }

  // Total analyses (from localStorage history)
  const totalEl = document.getElementById("totalAnalyses");

  const updateTotal = () => {
    try {
      const history = JSON.parse(localStorage.getItem("detectionHistory") || "[]");
      if (totalEl) {
        totalEl.innerText = history.length;
      }
    } catch (e) {
      if (totalEl) {
        totalEl.innerText = "0";
      }
    }
  };

  // Persist this analysis to history (uses window.__RESULT__ set inline)
  if (window.__RESULT__?.prediction) {
    try {
      const history = JSON.parse(localStorage.getItem("detectionHistory") || "[]");

      history.unshift({
        text: (window.__RESULT__.text || "").slice(0, 240),
        result: window.__RESULT__.prediction,
        confidence: window.__RESULT__.confidence,
        date: new Date().toLocaleString(),
      });

      // Keep only the latest 20 entries
      if (history.length > 20) {
        history.pop();
      }

      localStorage.setItem("detectionHistory", JSON.stringify(history));
    } catch (e) {
      // Fail silently
    }
  }

  updateTotal();
})();
