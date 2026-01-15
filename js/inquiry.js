document.addEventListener("DOMContentLoaded", async () => {
  try {
    // Check authentication
    const user = getUser();
    if (!user || user.role !== "admin") {
      window.location.href = "/mainlogin.html";
      return;
    }

    await loadInquiries();
  } catch (error) {
    console.error("Error initializing inquiries:", error);
  }
});

const filterClass = document.getElementById("filterClass");
const filterSubject = document.getElementById("filterSubject");
const inquiryList = document.getElementById("inquiryList");

let fullList = [];

/* Load inquiries from backend */
async function loadInquiries() {
  try {
    inquiryList.innerHTML = `<p class="loading">Loading inquiries...</p>`;

    const response = await apiCall("/inquiry/all");
    fullList = response.inquiries || [];

    populateFilters(fullList);
    render(fullList);
  } catch (error) {
    inquiryList.innerHTML = `<p>Error loading inquiries: ${error.message}</p>`;
    console.error(error);
  }
}

/* Populate filter dropdowns */
function populateFilters(data) {
  filterClass.innerHTML = `<option value="">Class</option>`;
  filterSubject.innerHTML = `<option value="">Subject</option>`;

  [...new Set(data.map((i) => i.class))].forEach((c) => {
    filterClass.innerHTML += `<option value="${c}">${c}</option>`;
  });

  [...new Set(data.map((i) => i.subject))].forEach((s) => {
    filterSubject.innerHTML += `<option value="${s}">${s}</option>`;
  });
}

/* Render inquiries */
function render(list) {
  inquiryList.innerHTML = "";

  if (list.length === 0) {
    inquiryList.innerHTML = `<p>No inquiries found</p>`;
    return;
  }

  list.forEach((item) => {
    inquiryList.innerHTML += `
        <div class="inquiry-card">
            <p><b>Student:</b> ${item.student}</p>
            <p><b>Class:</b> ${item.class}</p>
            <p><b>Subject:</b> ${item.subject}</p>
            <p><b>Title:</b> ${item.title}</p>
            <p><b>Description:</b> ${item.description}</p>
            <p><b>Status:</b> <span style="color: ${
              item.status === "pending"
                ? "orange"
                : item.status === "approved"
                ? "green"
                : "red"
            }">${item.status}</span></p>
            ${item.response ? `<p><b>Response:</b> ${item.response}</p>` : ""}

            <div class="btn-row">
                ${
                  item.status === "pending"
                    ? `
                    <button class="action-btn accept" onclick="approveInquiry(${item.id})">Approve</button>
                    <button class="action-btn reject" onclick="rejectInquiry(${item.id})">Reject</button>
                `
                    : '<span style="color: gray;">Already ' +
                      item.status +
                      "</span>"
                }
            </div>
        </div>`;
  });
}

/* Apply filters */
function applyFilters() {
  const c = filterClass.value;
  const s = filterSubject.value;

  const filtered = fullList.filter(
    (item) => (c === "" || item.class === c) && (s === "" || item.subject === s)
  );

  render(filtered);
}

filterClass.addEventListener("change", applyFilters);
filterSubject.addEventListener("change", applyFilters);

/* Approve inquiry */
async function approveInquiry(id) {
  try {
    const response = await apiCall(`/inquiry/${id}/approve`, "POST", {
      response: prompt("Enter approval response:"),
    });
    alert("Inquiry approved!");
    await loadInquiries();
  } catch (error) {
    alert("Error: " + error.message);
  }
}

/* Reject inquiry */
async function rejectInquiry(id) {
  try {
    const response = await apiCall(`/inquiry/${id}/reject`, "POST", {
      response: prompt("Enter rejection reason:"),
    });
    alert("Inquiry rejected!");
    await loadInquiries();
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
