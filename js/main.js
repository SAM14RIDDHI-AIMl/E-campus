/* =========================
   UTILS
========================= */
function loadUsers() {
  return JSON.parse(localStorage.getItem("users") || "[]");
}

function saveUsers(users) {
  localStorage.setItem("users", JSON.stringify(users));
}

function setLoggedIn(user) {
  localStorage.setItem("loggedInUser", JSON.stringify(user));
}

function getLoggedIn() {
  return JSON.parse(localStorage.getItem("loggedInUser"));
}

/* =========================
   ENSURE DEFAULT ADMIN
========================= */
function ensureAdmin() {
  const users = loadUsers();
  if (!users.find((u) => u.role === "admin")) {
    users.push({
      role: "admin",
      username: "admin",
      password: "admin123",
      name: "Admin",
    });
    saveUsers(users);
  }
}

/* =========================
   ADMIN LOGIN
========================= */
function initAdminLogin() {
  const btn = document.getElementById("al-login");
  if (!btn) return;

  btn.onclick = async () => {
    const username = document.getElementById("al-username").value.trim();
    const password = document.getElementById("al-password").value;

    if (!username || !password) {
      alert("Please enter username and password");
      return;
    }

    try {
      // Call backend login API
      const response = await apiCall("/auth/login", "POST", {
        username,
        password,
      });

      // Verify admin role
      if (response.user.role !== "admin") {
        alert("Invalid admin credentials. Admin access required.");
        return;
      }

      // Store token and user info
      setAuthToken(response.token);
      setUser(response.user);

      // ✅ Smooth transition
      document.body.style.opacity = "0";
      document.body.style.transition = "opacity 0.4s";

      setTimeout(() => {
        window.location.href = "/page/admin/adminhome.html";
      }, 400);
    } catch (error) {
      alert("Invalid Admin Login: " + error.message);
    }
  };
}

/* =========================
   ROUTER
========================= */
document.addEventListener("DOMContentLoaded", () => {
  const page = window.location.pathname.split("/").pop();

  if (page === "adminlogin.html") initAdminLogin();
});
