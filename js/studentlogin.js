document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".login-form");

  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const username = document.getElementById("username").value.trim();
      const password = document.getElementById("password").value;

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

        // Verify student role
        if (response.user.role !== "student") {
          alert("Please use admin login for admin accounts");
          return;
        }

        // Store token and user info
        setAuthToken(response.token);
        setUser(response.user);

        // Fade out and redirect
        document.body.style.opacity = "0";
        document.body.style.transition = "opacity 0.4s";

        setTimeout(() => {
          window.location.href = "/page/student/studenthome.html";
        }, 400);
      } catch (error) {
        alert("Login failed: " + error.message);
      }
    });
  }
});
