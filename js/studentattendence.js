document.addEventListener("DOMContentLoaded", async () => {
  try {
    // Get current user
    const user = getUser();
    if (!user || user.role !== "student") {
      window.location.href = "/mainlogin.html";
      return;
    }

    // Fetch attendance data from backend
    const response = await apiCall(`/attendance/student/${user.id}`);
    const attendanceData = response.attendance;

    const container = document.getElementById("attendance-list");

    if (!container) {
      console.error("attendance-list element not found");
      return;
    }

    container.innerHTML = "";

    if (attendanceData.length === 0) {
      container.innerHTML = "<p>No attendance records found</p>";
      return;
    }

    attendanceData.forEach((sub) => {
      const percent = sub.percentage;
      let color = percent < 35 ? "red" : percent < 75 ? "orange" : "green";

      container.innerHTML += `
                <div class="att-card">
                    <div class="att-top">
                        <div class="att-subject">${sub.subject}</div>
                        <div class="att-percent">${percent}%</div>
                    </div>

                    <div class="att-bar-bg">
                        <div class="att-bar-fill ${color}" style="width:${percent}%"></div>
                    </div>

                    <p class="att-info">
                        ${sub.present}/${sub.total} classes attended
                    </p>
                </div>
            `;
    });
  } catch (error) {
    console.error("Error loading attendance:", error);
    const container = document.getElementById("attendance-list");
    if (container) {
      container.innerHTML = `<p>Error loading attendance: ${error.message}</p>`;
    }
  }
});

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
