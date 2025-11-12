// To-Do Logic
document.getElementById("add-todo").addEventListener("click", () => {
    const input = document.getElementById("todo-item");
    const todoText = input.value.trim();
    if (todoText === "") return;

    const list = document.getElementById("todo-list");
    const item = document.createElement("div");
    item.className = "todo-item";
    item.innerText = todoText;

    list.appendChild(item);
    input.value = "";
});

// Assignment Upload Logic
document.getElementById("assignment-upload").addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const assignmentList = document.getElementById("assignment-list");
    const card = document.createElement("div");
    card.className = "assignment-card";

    card.innerHTML = `
        <strong>${file.name}</strong><br>
        <span>Uploaded successfully ✅</span>
    `;

    assignmentList.appendChild(card);
});


async function loadStudentAssignments() {
    const active = await (await fetch("http://localhost:8000/active")).json();

    if (!active.user_id || active.role !== "student") {
        alert("Please login as student first.");
        window.location.href = "login_page.html";
        return;
    }

    const studentId = active.user_id;

    const res = await fetch(`http://localhost:8000/student/${studentId}/assignments`);
    const assignments = await res.json();

    const list = document.getElementById("student-assignment-list");
    list.innerHTML = "";

    if (assignments.success === false) {
        list.innerHTML = `<p>${assignments.message}</p>`;
        return;
    }

    assignments.forEach(a => {
        list.innerHTML += `
            <div class="std-assignment-card">
                <h3>${a.title}</h3>
                <p><strong>Due:</strong> ${new Date(a.due_date).toLocaleDateString()}</p>
                <p>${a.description || "<i>No description provided.</i>"}</p>
                <button onclick="openAssignment(${a.assignment_id})">Open</button>
            </div>
        `;
    });
}

loadStudentAssignments();

