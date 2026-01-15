/* ================================
   STUDENT CLASS SCHEDULE
================================ */

document.addEventListener("DOMContentLoaded", async () => {
  try {
    // Check authentication
    const user = getUser();
    if (!user || user.role !== "student") {
      window.location.href = "/mainlogin.html";
      return;
    }

    await loadStudentSchedule();
  } catch (error) {
    console.error("Error initializing:", error);
  }
});

async function loadStudentSchedule() {
  const container = document.getElementById("scheduleList");

  // Show loading state
  container.innerHTML = `<p class="loading-text">Loading schedule...</p>`;

  try {
    const response = await apiCall(`/schedule/student/${getUser().id}`);

    if (!response.schedule || response.schedule.length === 0) {
      container.innerHTML = `<p>No schedule available</p>`;
      return;
    }
    renderSchedule(response.schedule);
  } catch (error) {
    console.error("Error:", error);
    container.innerHTML = `<p style="text-align:center;color:red">
                Failed to load schedule
             </p>`;
  }
}

function renderSchedule(schedule) {
  const container = document.getElementById("scheduleList");
  container.innerHTML = "";

  schedule.forEach((item) => {
    const dayTime = `${item.day} ${item.time}`;
    container.innerHTML += `
            <div class="schedule-card">
                <div class="subject">${item.subject_name}</div>
                <div class="time">⏰ ${dayTime}</div>
                <div class="room">📍 ${item.room || "TBA"}</div>
                <div class="teacher">👨‍🏫 ${item.teacher_name}</div>
            </div>
        `;
  });
}

// Load on page open
loadStudentSchedule();

/* ================================
   FOOTER NAVIGATION (STUDENT)
================================ */

function goHome() {
  window.location.href = "/page/student/studenthome.html";
}

function goSchedule() {
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
