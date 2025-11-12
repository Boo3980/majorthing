console.log("JS loaded — profId =", localStorage.getItem("prof_id"));
// Get the list container
async function getActiveProfessorId() {
    const res = await fetch("http://localhost:8000/active");
    const data = await res.json();

    if (!data.user_id || data.role !== "professor") {
        alert("Please login as professor first.");
        window.location.href = "login_page.html";
        return null;
    }

    return data.user_id;
}

const assignmentList = document.getElementById("assignment-list");

// --- NEW: "Add Assignment" now adds an inline form card ---
document.getElementById("add-assignment").addEventListener("click", () => {
    // Prevent adding multiple new-assignment cards
    if (document.querySelector(".new-assignment-form")) {
        alert("Please save or cancel the current new assignment first.");
        return;
    }

    const card = document.createElement("div");
    card.className = "assignment-card new-assignment-form"; // Added a new class

    card.innerHTML = `
        <h3>New Assignment</h3>
        <input type="text" id="new-title" class="form-input" placeholder="Assignment Title">
        <input type="date" id="new-due-date" class="form-input">
        <textarea id="new-description" class="form-textarea" placeholder="Add a description..."></textarea>
        <div class="form-controls">
            <button class="save-new-btn">Save to DB</button>
            <button class="cancel-new-btn">Cancel</button>
        </div>
    `;
    
    // Add the new form card to the top
    assignmentList.prepend(card);
});


/**
 * Loads all assignments from the server and displays them.
 */

async function loadAssignments() {
    const profId = await getActiveProfessorId();



    if (!profId) {
        console.error("❌ ERROR: prof_id missing from localStorage");
        return;
    }

    try {
        const response = await fetch(`http://localhost:8000/prof/${profId}/assignments`);
        
        if (!response.ok) throw new Error(`Network error: ${response.statusText}`);

        const assignments = await response.json();
        const container = document.getElementById("assignment-list");
        container.innerHTML = ""; // Clear existing assignments

        if (!Array.isArray(assignments) || assignments.length === 0) {
            container.innerHTML = "<p>No assignments found.</p>";
            return;
        }

        assignments.forEach(a => {
            const card = document.createElement("div");
            card.className = "assignment-card";
            card.setAttribute("data-card-id", a.assignment_id); // Add ID to the card itself

            const dueDate = new Date(a.due_date).toLocaleDateString("en-US", {
                year: 'numeric', month: 'long', day: 'numeric'
            });

            // --- UPDATED: Card now includes description and Edit button ---
            card.innerHTML = `
                <div class="assignment-header">
                    <h3>${a.title}</h3>
                    <button class="delete-btn" data-id="${a.assignment_id}">Delete</button>
                </div>
                <p><strong>Due:</strong> ${dueDate}</p>
                
                <div class="view-mode">
                    <p class="assignment-description">${a.description || '<i>No description.</i>'}</p>
                    <button class="edit-btn" data-id="${a.assignment_id}">Edit</button>
                    <button class="open-btn" data-id="${a.assignment_id}">Open</button>
                </div>

                <div class="edit-mode" style="display: none;">
                    <textarea class="edit-description">${a.description || ''}</textarea>
                    <button class="save-edit-btn" data-id="${a.assignment_id}">Save</button>
                    <button class="cancel-edit-btn">Cancel</button>
                </div>
            `;
            container.appendChild(card);
        });

    } catch (error) {
        console.error("❌ Failed to load assignments:", error);
        document.getElementById("assignment-list").innerHTML = 
            "<p>Error loading assignments. Please try again later.</p>";
    }
}

// --- NEW: Function to CREATE a new assignment ---
async function createNewAssignment(title, dueDate, description) {
    const profId = await getActiveProfessorId();


    if (!profId) {
        alert("⚠️ No active professor session. Please login again.");
        window.location.href = "login_page.html";
        return;
    }

    if (!title || !dueDate) {
        alert("Please provide at least a title and a due date.");
        return;
    }

    try {
        const response = await fetch(`http://localhost:8000/prof/${profId}/assignments`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                title,
                due_date: dueDate,
                description
            })
        });

        const result = await response.json();
        if (result.success) {
            alert("✅ Assignment Saved!");
            loadAssignments(); 
        } else {
            alert(`❌ Failed to save: ${result.message || 'Unknown server error'}`);
        }
    } catch (error) {
        console.error("❌ Error saving new assignment:", error);
        alert("❌ A network error occurred while saving.");
    }
}


// --- NEW: Function to UPDATE an assignment's description ---
async function updateAssignment(id, newDescription) {
    try {
        const response = await fetch(`http://localhost:8000/assignment/${id}`, {
            method: "PUT", // Use PUT or PATCH
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ description: newDescription })
        });

        const result = await response.json();
        if (result.success) {
            alert("✅ Description updated!");
            loadAssignments(); // Easiest way to refresh the card
        } else {
            alert(`❌ Failed to update: ${result.message || 'Unknown server error'}`);
        }
    } catch (error) {
        console.error("❌ Error updating assignment:", error);
        alert("❌ A network error occurred while updating.");
    }
}

/**
 * Deletes an assignment from the database.
 */
async function deleteAssignment(id) {
    console.log("Deleting database assignment ID:", id);

    if (!confirm("Are you sure? This will permanently delete the assignment.")) return;

    try {
        const response = await fetch(`http://localhost:8000/assignment/${id}`, {
            method: "DELETE"
        });
        const result = await response.json();

        if (result.success) {
            alert("✅ Assignment deleted!");
            loadAssignments(); // Reload the list
        } else {
            alert(`❌ Failed to delete assignment: ${result.message || 'Unknown error'}`);
        }
    } catch (error) {
        console.error("❌ Error during deletion:", error);
        alert("❌ Failed to delete assignment due to a network or server error.");
    }
}

// --- BUG FIX: Added the missing openAssignment function ---
/**
 * Navigates to the specific assignment page.
 */
function openAssignment(id) {
    window.location.href = `assignment_page.html?id=${id}`;
}


// --- BUG FIX: Moved event listener to the global scope ---
// This single listener now handles all button clicks
document.addEventListener("click", (e) => {
    
    // --- Database Assignment Clicks ---

    // Open saved assignment
    if (e.target.classList.contains("open-btn")) {
        const id = e.target.getAttribute("data-id");
        openAssignment(id);
    }

    // Delete saved assignment
    if (e.target.classList.contains("delete-btn")) {
        const id = e.target.getAttribute("data-id");
        deleteAssignment(id);
    }

    // --- Edit Mode Toggles ---

    // Click "Edit"
    if (e.target.classList.contains("edit-btn")) {
        const card = e.target.closest(".assignment-card");
        card.querySelector(".view-mode").style.display = "none";
        card.querySelector(".edit-mode").style.display = "block";
    }

    // Click "Cancel" (in edit mode)
    if (e.target.classList.contains("cancel-edit-btn")) {
        const card = e.target.closest(".assignment-card");
        card.querySelector(".view-mode").style.display = "block";
        card.querySelector(".edit-mode").style.display = "none";
    }

    // Click "Save" (in edit mode)
    if (e.target.classList.contains("save-edit-btn")) {
        const id = e.target.getAttribute("data-id");
        const card = e.target.closest(".assignment-card");
        const newDescription = card.querySelector(".edit-description").value;
        updateAssignment(id, newDescription);
    }

    // --- New Assignment Form Clicks ---

    // Click "Save to DB" (for new assignment)
    if (e.target.classList.contains("save-new-btn")) {
        const card = e.target.closest(".new-assignment-form");
        const title = card.querySelector("#new-title").value;
        const dueDate = card.querySelector("#new-due-date").value;
        const description = card.querySelector("#new-description").value;
        createNewAssignment(title, dueDate, description);
    }

    // Click "Cancel" (for new assignment)
    if (e.target.classList.contains("cancel-new-btn")) {
        if (confirm("Cancel creating this new assignment?")) {
            e.target.closest(".new-assignment-form").remove();
        }
    }
});


// Initial load of assignments when the page starts
loadAssignments();
localStorage.setItem("profId", 1);
// --- BUG FIX: Removed the extra '}' syntax error that was here ---