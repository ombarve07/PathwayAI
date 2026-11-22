/**
 * PATHWAY AI - Shared Global UI & Navigation Logic
 */

document.addEventListener("DOMContentLoaded", () => {
  setupNavigation();
  updateAuthUI();
});

function setupNavigation() {
  const toggleBtn = document.querySelector(".nav-toggle");
  const navLinks = document.querySelector(".nav-links");

  if (toggleBtn && navLinks) {
    toggleBtn.addEventListener("click", () => {
      navLinks.classList.toggle("mobile-open");
    });
  }

  // Active state highlighting
  const currentFile = window.location.pathname.split("/").pop() || "index.html";
  const links = document.querySelectorAll(".nav-links a");
  links.forEach(link => {
    const href = link.getAttribute("href") || "";
    const linkFile = href.split("/").pop();
    if (linkFile && (linkFile === currentFile || (currentFile === "" && linkFile === "index.html"))) {
      link.classList.add("active");
    }
  });
}

function updateAuthUI() {
  const user = API.getUser();
  const navActions = document.querySelector(".nav-actions");

  if (!navActions) return;

  const isPagesDir = window.location.pathname.includes("/pages/");
  const p = (page) => isPagesDir ? page : `pages/${page}`;

  if (user && API.isAuthenticated()) {
    // Show logged-in student state
    const adminPill = user.is_admin ? `<a href="${p('admin-dashboard.html')}" class="badge badge-purple" style="margin-right:8px;">Admin Portal</a>` : '';
    navActions.innerHTML = `
      ${adminPill}
      <a href="${p('student-dashboard.html')}" class="btn btn-secondary btn-sm">My Dashboard</a>
      <button onclick="API.auth.logout()" class="btn btn-outline-dark btn-sm">Sign Out</button>
    `;
  } else {
    // Show logged-out guest state
    navActions.innerHTML = `
      <a href="${p('login.html')}" class="btn btn-secondary btn-sm">Login</a>
      <a href="${p('register.html')}" class="btn btn-primary btn-sm">Get Started</a>
    `;
  }
}
