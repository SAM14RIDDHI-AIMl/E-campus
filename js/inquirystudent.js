/* ===============================
   STUDENT INQUIRY PAGE
=============================== */

document.addEventListener("DOMContentLoaded", async () => {
  try {
    // Check authentication
    const user = getUser();
    if (!user || user.role !== "student") {
      window.location.href = "/mainlogin.html";
      return;
    }

    await loadSubjects();
    await loadClasses();
  } catch (error) {
    console.error("Error initializing:", error);
  }
});

/* Load Subjects */
async function loadSubjects() {
  try {
    const response = await apiCall("/schedule/subjects");
    const subjectBox = document.getElementById("inqSubject");
    subjectBox.innerHTML = `<option value="">Select Subject</option>`;

    response.subjects.forEach((sub) => {
      subjectBox.innerHTML += `<option value="${sub.id}">${sub.name}</option>`;
    });
  } catch (error) {
    console.error("Error loading subjects:", error);
  }
}

/* Load Classes */
async function loadClasses() {
  try {
    const response = await apiCall("/schedule/classes");
    const classBox = document.getElementById("inqClass");
    if (classBox) {
      classBox.innerHTML = `<option value="">Select Class</option>`;
      response.classes.forEach((cls) => {
        classBox.innerHTML += `<option value="${cls.id}">${cls.name}</option>`;
      });
    }
  } catch (error) {
    console.error("Error loading classes:", error);
  }
}

/* Submit Inquiry */
async function submitInquiry() {
  try {
    const subject = document.getElementById("inqSubject").value;
    const classId = document.getElementById("inqClass")
      ? document.getElementById("inqClass").value
      : "1";
    const title = document.getElementById("inqTitle")
      ? document.getElementById("inqTitle").value
      : "General Inquiry";
    const desc = document.getElementById("inqDesc").value;

    if (!subject || !desc) {
      alert("Please fill all required fields");
      return;
    }

    await apiCall("/inquiry/submit", "POST", {
      subject_id: parseInt(subject),
      class_id: parseInt(classId) || 1,
      title: title || "Inquiry",
      description: desc,
    });

    alert("Inquiry submitted successfully");
    document.getElementById("inqSubject").value = "";
    document.getElementById("inqDesc").value = "";
  } catch (error) {
    console.error("Error:", error);
    alert("Failed to submit inquiry");
  }
}

/* ---------- FOOTER NAVIGATION ---------- */
function goStudentHome() {
  window.location.href = "/page/student/studenthome.html";
}

function goStudentClassSchedule() {
  window.location.href = "/page/student/classstudent.html";
}

function goStudentAttendance() {
  window.location.href = "/page/student/studentattendence.html";
}

function goStudentInquiry() {
  window.location.href = "/page/student/inquirystudent.html";
}

function goStudentCalendar() {
  window.location.href = "/page/student/calendarstudent.html";
}
