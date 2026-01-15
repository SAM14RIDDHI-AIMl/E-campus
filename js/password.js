/* ================================
   CHANGE PASSWORD
================================ */

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("np-send");
  if (!btn) return;

  btn.onclick = changePassword;
});

async function changePassword() {
  const oldPass = document.getElementById("np-old")?.value || "";
  const newPass = document.getElementById("np-pass").value;
  const confirm = document.getElementById("np-confirm").value;

  if (!newPass || !confirm) {
    alert("Please fill all fields");
    return;
  }

  if (newPass !== confirm) {
    alert("Passwords do not match");
    return;
  }

  try {
    const user = getUser();
    if (!user) {
      alert("Session expired. Please login again.");
      window.location.href = "/mainlogin.html";
      return;
    }

    await apiCall("/auth/change-password", "POST", {
      old_password: oldPass,
      new_password: newPass,
    });

    alert("Password updated successfully");
    window.location.href = "/mainlogin.html";
  } catch (error) {
    console.error("Error:", error);
    alert(
      "Failed to change password: " + (error.message || "Please try again")
    );
  }
}
