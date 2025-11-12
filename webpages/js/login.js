async function loginUser() {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const role = document.getElementById("role").value;
    const error = document.getElementById("error");

    
    if (!email || !password) {
        error.innerText = "Please enter both email and password.";
        return;
    }

    try {
        const response = await fetch("http://localhost:8000/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password, role })
        });


        const result = await response.json();

        if (!result.success) {
            error.innerText = "Invalid login credentials.";
            return;
        }

        // Redirect based on role
        if (result.role === "professor") {
            localStorage.setItem("prof_id", result.user_id);
            window.location.href = "../html/professor_dashboard.html";
        }
        else if (result.role === "student") {
            localStorage.setItem("student_id", result.user_id);
            window.location.href = "../html/student_dashboard.html";
        }


    } catch (err) {
        error.innerText = "Server error. Try again.";
    }
}
