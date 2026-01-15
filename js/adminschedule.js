document.addEventListener("DOMContentLoaded", async () => {
  try {
    // Check authentication
    const user = getUser();
    if (!user || user.role !== "admin") {
      window.location.href = "/mainlogin.html";
      return;
    }

    // Load initial data
    await loadClasses();
    await loadSubjects();
    await loadSchedule();
  } catch (error) {
    console.error("Error initializing schedule:", error);
    document.getElementById(
      "adminScheduleList"
    ).innerHTML = `<p>Error loading schedules: ${error.message}</p>`;
  }
});

const classFilter = document.getElementById("classFilter");
const subjectFilter = document.getElementById("subjectFilter");
const scheduleBox = document.getElementById("adminScheduleList");

/* Load classes */
async function loadClasses() {
  try {
    const response = await apiCall("/schedule/classes");
    classFilter.innerHTML = '<option value="">Select Class</option>';

    response.classes.forEach((cls) => {
      classFilter.innerHTML += `<option value="${cls.name}">${cls.name}</option>`;
    });
  } catch (error) {
    console.error("Error loading classes:", error);
  }
}

/* Load subjects */
async function loadSubjects() {
  try {
    const response = await apiCall("/schedule/subjects");
    subjectFilter.innerHTML = '<option value="">Select Subject</option>';

    response.subjects.forEach((sub) => {
      subjectFilter.innerHTML += `<option value="${sub.name}">${sub.name}</option>`;
    });
  } catch (error) {
    console.error("Error loading subjects:", error);
  }
}

/* Load schedules */
async function loadSchedule() {
  try {
    scheduleBox.innerHTML = `<p class="loading-text">Loading...</p>`;

    const cls = classFilter.value;
    const sub = subjectFilter.value;

    let url = "/schedule/all";
    const params = new URLSearchParams();
    if (cls) params.append("class", cls);
    if (sub) params.append("subject", sub);
    if (params.toString()) url += "?" + params.toString();

    const response = await apiCall(url);
    scheduleBox.innerHTML = "";

    if (response.schedule.length === 0) {
      scheduleBox.innerHTML = `<p>No records found</p>`;
      return;
    }

    response.schedule.forEach((item) => {
      scheduleBox.innerHTML += `
                <div class="schedule-card">
                    <h4>${item.subject}</h4>
                    <p>Class: ${item.class}</p>
                    <p>Day: ${item.day_of_week}</p>
                    <p>Time: ${item.startTime} - ${item.endTime}</p>
                    <p>Teacher: ${item.teacher}</p>
                    <p>Room: ${item.room_number || "N/A"}</p>
                </div>
            `;
    });
  } catch (error) {
    scheduleBox.innerHTML = `<p>Error loading schedules: ${error.message}</p>`;
  }
}

/* Event listeners */
classFilter.addEventListener("change", loadSchedule);
subjectFilter.addEventListener("change", loadSchedule);
/*-------path navigation---------*/

function goHome() {
  window.location.href = "/page/admin/adminhome.html";
}
function goAdminSchedule() {
  window.location.href = "/page/admin/adminschedule.html";
}

function goMarkAttendance() {
  window.location.href = "/page/admin/markattendence.html";
}

function goInquiry() {
  window.location.href = "/page/admin/inquiryadmin.html";
}

function goCalendar() {
  window.location.href = "/page/admin/admincalender.html";
}
