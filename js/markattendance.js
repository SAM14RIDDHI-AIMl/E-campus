document.addEventListener("DOMContentLoaded", async () => {
  try {
    // Check authentication
    const user = getUser();
    if (!user || user.role !== "admin") {
      window.location.href = "/mainlogin.html";
      return;
    }

    await loadSubjects();
  } catch (error) {
    console.error("Error initializing:", error);
  }
});

let attendanceData = {};

// Load subjects from backend
async function loadSubjects() {
  try {
    const response = await apiCall("/schedule/subjects");
    let select = document.getElementById("subjectSelect");
    select.innerHTML = `<option value="">Select Subject</option>`;

    response.subjects.forEach((sub) => {
      select.innerHTML += `<option value="${sub.id}|${sub.name}">${sub.name}</option>`;
    });
  } catch (error) {
    console.error("Error loading subjects:", error);
  }
}

// Load students when subject is selected
async function loadStudents() {
  try {
    let subjectSelect = document.getElementById("subjectSelect").value;
    if (!subjectSelect) return;

    document.getElementById(
      "studentList"
    ).innerHTML = `<p class="loading">Loading students...</p>`;

    // Get all students from backend
    const response = await apiCall("/admin/users?role=student");
    let list = document.getElementById("studentList");
    list.innerHTML = "";

    response.users.forEach((std) => {
      attendanceData[std.id] = ""; // initialize

      list.innerHTML += `
            <div class="student-card">
                <span class="student-name">${std.name}</span>
                <div class="btn-group">
                    <button class="present-btn" onclick="markPresent('${std.id}', this)">P</button>
                    <button class="absent-btn" onclick="markAbsent('${std.id}', this)">A</button>
                </div>
            </div>`;
    });
  } catch (error) {
    console.error("Error loading students:", error);
    document.getElementById(
      "studentList"
    ).innerHTML = `<p>Error loading students: ${error.message}</p>`;
  }
}

// Mark Present
function markPresent(id, btn) {
  attendanceData[id] = "P";

  let parent = btn.parentNode;
  parent.querySelector(".present-btn").classList.add("present-active");
  parent.querySelector(".absent-btn").classList.remove("absent-active");
}

// Mark Absent
function markAbsent(id, btn) {
  attendanceData[id] = "A";

  let parent = btn.parentNode;
  parent.querySelector(".absent-btn").classList.add("absent-active");
  parent.querySelector(".present-btn").classList.remove("present-active");
}

// Submit Attendance
async function submitAttendance() {
  try {
    let subjectSelect = document.getElementById("subjectSelect").value;
    if (!subjectSelect) {
      alert("Please select a subject!");
      return;
    }

    const [subjectId] = subjectSelect.split("|");
    const classId = 1; // Default class

    let formatted = [];

    for (let id in attendanceData) {
      if (attendanceData[id] !== "") {
        formatted.push({
          student_id: parseInt(id),
          status: attendanceData[id],
        });
      }
    }

    if (formatted.length === 0) {
      alert("Please mark attendance!");
      return;
    }

    await apiCall("/attendance/submit", "POST", {
      subject_id: parseInt(subjectId),
      class_id: classId,
      attendance: formatted,
    });

    alert("Attendance submitted successfully!");

    // Reset form
    document.getElementById("studentList").innerHTML = "";
    document.getElementById("subjectSelect").value = "";
    attendanceData = {};
  } catch (error) {
    alert("Error: " + error.message);
  }
}
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
