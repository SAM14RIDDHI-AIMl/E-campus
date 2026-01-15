/* =========================
   STUDENT HOME – ATTENDANCE
========================= */

document.addEventListener("DOMContentLoaded", async () => {
  try {
    // Get current user
    const user = getUser();
    if (!user || user.role !== "student") {
      window.location.href = "/mainlogin.html";
      return;
    }

    // Fetch attendance statistics from backend
    const response = await apiCall(`/attendance/statistics/${user.id}`);
    const stats = response.statistics;
    const percent = stats.percentage;

    // Update UI
    const attendanceEl = document.getElementById("attendanceValue");
    attendanceEl.innerText = percent + "%";

    // Color logic
    if (percent < 35) {
      attendanceEl.style.color = "#e74c3c"; // red
    } else if (percent < 75) {
      attendanceEl.style.color = "#f1c40f"; // yellow
    } else {
      attendanceEl.style.color = "#27ae60"; // green
    }
  } catch (error) {
    console.error("Error loading attendance:", error);
    document.getElementById("attendanceValue").innerText = "Error";
  }
});
// Change goSchedule to goClassSchedule
function goClassSchedule() {
  window.location.href = "/page/student/classstudent.html";
}

function goAttendance() {
  window.location.href = "/page/student/studentattendence.html";
}

function goInquiry() {
  window.location.href = "/page/student/inquirystudent.html";
}

function goCalendar() {
  window.location.href = "/page/student/calendarstudent.html";
}

// Change goStudentProfile to goProfile
function goProfile() {
  window.location.href = "/page/student/studentprofile.html";
}
