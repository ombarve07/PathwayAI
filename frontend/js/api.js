/**
 * PATHWAY AI - Front-End API Client & State Management
 */

// Dynamically determine backend API base:
// If running on port 8000 (FastAPI), use relative/origin.
// If running on Live Server (e.g. port 5500, 3000) or file://, target FastAPI on http://127.0.0.1:8000.
const API_BASE = (window.location.protocol.startsWith("http") && window.location.port === "8000")
  ? window.location.origin
  : "http://127.0.0.1:8000";

// Helper to resolve page links whether running in / or /frontend/ or /pages/
function resolvePageUrl(pagePath) {
  const isPagesDir = window.location.pathname.includes("/pages/");
  if (pagePath === "index.html" || pagePath === "/index.html") {
    return isPagesDir ? "../index.html" : "index.html";
  }
  const cleanName = pagePath.replace(/^\/(pages\/)?/, "");
  return isPagesDir ? cleanName : `pages/${cleanName}`;
}

const API = {
  getToken() {
    return localStorage.getItem("pathway_token");
  },
  setToken(token) {
    localStorage.setItem("pathway_token", token);
  },
  getUser() {
    try {
      const u = localStorage.getItem("pathway_user");
      return u ? JSON.parse(u) : null;
    } catch {
      return null;
    }
  },
  setUser(user) {
    localStorage.setItem("pathway_user", JSON.stringify(user));
  },
  clearAuth() {
    localStorage.removeItem("pathway_token");
    localStorage.removeItem("pathway_user");
  },
  isAuthenticated() {
    return !!this.getToken();
  },

  async request(endpoint, options = {}) {
    const headers = options.headers || {};
    headers["Content-Type"] = "application/json";

    const token = this.getToken();
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const config = {
      ...options,
      headers
    };

    try {
      const url = `${API_BASE}${endpoint}`;
      const response = await fetch(url, config);
      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        if (response.status === 401 && !endpoint.includes("/login")) {
          this.clearAuth();
          if (!window.location.pathname.includes("login.html") && !window.location.pathname.includes("register.html")) {
            window.location.href = resolvePageUrl("login.html");
          }
        }
        const errorMsg = data.detail || data.message || "An error occurred with your request.";
        throw new Error(errorMsg);
      }

      return data;
    } catch (err) {
      if (err.message.includes("Failed to fetch") || err.message.includes("NetworkError")) {
        console.error(`Cannot connect to backend API at ${API_BASE}. Make sure the FastAPI server is running on port 8000.`);
      } else {
        console.error(`API Error [${endpoint}]:`, err.message);
      }
      throw err;
    }
  },

  // --- Auth ---
  auth: {
    async register(data) {
      const res = await API.request("/api/auth/register", {
        method: "POST",
        body: JSON.stringify(data)
      });
      API.setToken(res.access_token);
      API.setUser(res);
      return res;
    },
    async login(data) {
      const res = await API.request("/api/auth/login", {
        method: "POST",
        body: JSON.stringify(data)
      });
      API.setToken(res.access_token);
      API.setUser(res);
      return res;
    },
    logout() {
      API.clearAuth();
      window.location.href = resolvePageUrl("index.html");
    },
    async getMe() {
      return await API.request("/api/auth/me");
    },
    async forgotPassword(email) {
      return await API.request("/api/auth/forgot-password", {
        method: "POST",
        body: JSON.stringify({ email })
      });
    },
    async resetPassword(token, new_password) {
      return await API.request("/api/auth/reset-password", {
        method: "POST",
        body: JSON.stringify({ token, new_password })
      });
    }
  },

  // --- Students ---
  students: {
    async getProfile() {
      return await API.request("/api/students/profile");
    },
    async updateProfile(data) {
      return await API.request("/api/students/profile", {
        method: "PUT",
        body: JSON.stringify(data)
      });
    },
    async saveEducation(data) {
      return await API.request("/api/students/education", {
        method: "POST",
        body: JSON.stringify(data)
      });
    },
    async getDashboard() {
      return await API.request("/api/students/dashboard");
    }
  },

  // --- Careers ---
  careers: {
    async list(categorySlug = "", search = "") {
      let query = [];
      if (categorySlug) query.push(`category_slug=${encodeURIComponent(categorySlug)}`);
      if (search) query.push(`search=${encodeURIComponent(search)}`);
      const qs = query.length ? `?${query.join("&")}` : "";
      return await API.request(`/api/careers${qs}`);
    },
    async getCategories() {
      return await API.request("/api/careers/categories");
    },
    async getDetails(idOrSlug) {
      return await API.request(`/api/careers/${idOrSlug}`);
    },
    async getRoadmap(careerId) {
      return await API.request(`/api/careers/${careerId}/roadmap`);
    },
    async getEligibility(careerId) {
      return await API.request(`/api/careers/${careerId}/eligibility`);
    }
  },

  // --- Assessments ---
  assessments: {
    async start(data) {
      return await API.request("/api/assessments/start", {
        method: "POST",
        body: JSON.stringify(data)
      });
    },
    async getQuestions(sessionId) {
      return await API.request(`/api/assessments/${sessionId}/questions`);
    },
    async submitAnswer(sessionId, data) {
      return await API.request(`/api/assessments/${sessionId}/answer`, {
        method: "POST",
        body: JSON.stringify(data)
      });
    },
    async complete(sessionId) {
      return await API.request(`/api/assessments/${sessionId}/complete`, {
        method: "POST"
      });
    },
    async getResults(sessionId) {
      return await API.request(`/api/assessments/${sessionId}/results`);
    },
    async getHistory() {
      return await API.request("/api/assessments/history");
    },
    async getConfigurations() {
      return await API.request("/api/assessments/configurations");
    },
    async adaptiveNext(sessionId) {
      return await API.request(`/api/assessments/${sessionId}/adaptive-next`, {
        method: "POST"
      });
    }
  },

  // --- Recommendations ---
  recommendations: {
    async getCareers() {
      return await API.request("/api/recommendations/careers");
    },
    async getCourses(skillGap = "") {
      const qs = skillGap ? `?skill_gap=${encodeURIComponent(skillGap)}` : "";
      return await API.request(`/api/recommendations/courses${qs}`);
    },
    async recordClick(courseId) {
      return await API.request(`/api/recommendations/affiliate-click?course_id=${courseId}`, {
        method: "POST"
      });
    }
  },

  // --- Progress ---
  progress: {
    async get() {
      return await API.request("/api/progress");
    },
    async updateSkill(skillId, proficiencyLevel, evidenceNote = "") {
      return await API.request("/api/progress/skills", {
        method: "POST",
        body: JSON.stringify({
          skill_id: skillId,
          proficiency_level: proficiencyLevel,
          evidence_note: evidenceNote
        })
      });
    },
    async updateRoadmap(stageId, isCompleted, notes = "") {
      return await API.request("/api/progress/roadmap", {
        method: "POST",
        body: JSON.stringify({
          stage_id: stageId,
          is_completed: isCompleted,
          notes: notes
        })
      });
    },
    async submitProject(title, description, githubUrl, skills) {
      return await API.request(`/api/progress/projects?title=${encodeURIComponent(title)}&description=${encodeURIComponent(description)}&github_or_file_url=${encodeURIComponent(githubUrl)}&skills_applied=${encodeURIComponent(skills)}`, {
        method: "POST"
      });
    }
  },

  // --- Payments ---
  payments: {
    async createOrder(sessionId = null, itemType = "analytics_report") {
      return await API.request("/api/payments/create-order", {
        method: "POST",
        body: JSON.stringify({ session_id: sessionId, item_type: itemType })
      });
    },
    async verify(orderId, paymentId, signature) {
      return await API.request("/api/payments/verify", {
        method: "POST",
        body: JSON.stringify({
          order_id: orderId,
          payment_id: paymentId,
          signature: signature
        })
      });
    },
    async getHistory() {
      return await API.request("/api/payments/history");
    }
  },

  // --- Admin ---
  admin: {
    async getStats() {
      return await API.request("/api/admin/dashboard");
    },
    async getStudents() {
      return await API.request("/api/admin/students");
    },
    async createCareer(data) {
      return await API.request("/api/admin/careers", {
        method: "POST",
        body: JSON.stringify(data)
      });
    },
    async addQuestion(data) {
      return await API.request("/api/admin/questions", {
        method: "POST",
        body: JSON.stringify(data)
      });
    },
    async getRevenue() {
      return await API.request("/api/admin/revenue");
    },
    async updatePricing(reportPrice, premiumPrice) {
      return await API.request(`/api/admin/pricing?report_price=${reportPrice}&premium_price=${premiumPrice}`, {
        method: "PUT"
      });
    }
  }
};

// Global Toast UI Notification
function showToast(message, type = "info") {
  let container = document.getElementById("toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    container.className = "toast-container";
    document.body.appendChild(container);
  }

  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(10px)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}
