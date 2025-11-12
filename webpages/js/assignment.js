// Fetch title from URL
const params = new URLSearchParams(window.location.search);
const title = params.get("title");

document.getElementById("assignment-title").innerText = title;

// Example student data
const notSubmitted = ["Student A", "Student B", "Student C"];
const submitted = ["Student D", "Student E"];

const notBox = document.getElementById("not-submitted-list");
const subBox = document.getElementById("submitted-list");

// Populate lists
notSubmitted.forEach(name => {
    const div = document.createElement("div");
    div.className = "student-box";
    div.innerText = name;
    notBox.appendChild(div);
});

submitted.forEach(name => {
    const div = document.createElement("div");
    div.className = "student-box";
    div.innerText = name;
    
    div.addEventListener("click", () => {
        window.location.href = "student_submission.html?student=" + name;
    });

    subBox.appendChild(div);
});
