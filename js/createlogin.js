/* ================================
   CREATE ACCOUNT (STUDENT REGISTRATION)
================================ */

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("ca-send");
  if (!btn) return;

  btn.onclick = registerStudent;
});

async function registerStudent() {
  const username =
    document.getElementById("ca-username")?.value.trim() ||
    document.getElementById("ca-name")?.value.trim();
  const password = document.getElementById("ca-password")?.value.trim();
  const email = document.getElementById("ca-email")?.value.trim();
  const phone = document.getElementById("ca-phone")?.value.trim();

  if (!username || !password || !email || !phone) {
    alert("Please fill all required fields");
    return;
  }

  try {
    const response = await apiCall("/auth/register", "POST", {
      username: username,
      password: password,
      email: email,
      phone_number: phone,
      role: "student",
    });

    alert("Account created successfully! Please login.");
    window.location.href = "/mainlogin.html";
  } catch (error) {
    console.error("Error:", error);
    alert("Failed to create account: " + (error.message || "Please try again"));
  }
}
