const params = new URLSearchParams(window.location.search);
const student = params.get("student");

document.getElementById("student-name").innerText = student + "'s Submission";
