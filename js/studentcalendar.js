// 1. Initialize Framework7 for Student Portal
const app = new Framework7({
  el: "#app",
  name: "Student Portal",
  theme: "auto",
});

let studentCalendar;
let academicEvents = []; // Starts empty, populated by Backend

/**
 * FETCH DATA FROM BACKEND
 */
async function fetchCalendarEvents() {
  try {
    // Check authentication
    const user = getUser();
    if (!user || user.role !== "student") {
      window.location.href = "/mainlogin.html";
      return;
    }

    // Fetch calendar events from backend
    const response = await apiCall("/schedule/calendar");

    // Transform backend data into JS Date objects
    academicEvents = (response.events || []).map((item) => ({
      date: new Date(item.date),
      title: item.title,
      type: item.event_type || "general",
    }));

    renderStudentCalendar();
  } catch (error) {
    console.error("Error loading events:", error);
    // Fallback: Render empty calendar if backend fails
    renderStudentCalendar();
  }
}

/**
 * Renders the Framework7 Calendar with Highlighting
 */
function renderStudentCalendar() {
  studentCalendar = app.calendar.create({
    containerEl: "#student-calendar-container",
    value: [new Date()],
    weekHeader: true,
    // HIGHLIGHTING LOGIC: Assigns CSS classes based on event type
    events: academicEvents.map((e) => ({
      date: e.date,
      cssClass: "event-" + e.type,
    })),
    on: {
      dayClick(calendar, dayEl, year, month, day) {
        const clickedDate = new Date(year, month, day).toDateString();
        const found = academicEvents.find(
          (e) => e.date.toDateString() === clickedDate
        );

        if (found) {
          // Displays the popup as seen in your previews
          app.dialog.alert(found.title, "Event Details");
        }
      },
    },
  });
}

// Initialize on page load
document.addEventListener("DOMContentLoaded", fetchCalendarEvents);

/**
 * Navigation Routes
 * Matches your student folder structure
 */
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
  window.location.href = "/page/student/studentcalendar.html";
}
