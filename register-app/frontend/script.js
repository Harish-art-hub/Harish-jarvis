document.addEventListener("DOMContentLoaded", function () {
    // ✅ Handle Login Form
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            let email = document.getElementById("loginEmail").value;
            let password = document.getElementById("loginPassword").value;

            let response = await fetch("http://127.0.0.1:5000/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });

            let result = await response.json();
            document.getElementById("loginMessage").innerText = result.message;

            if (result.success) {
                localStorage.setItem("user", result.user);
                window.location.href = "home.html"; // Redirect to home page after login
            }
        });
    }

    // ✅ Redirect logged-in users away from login/register pages
    if (window.location.pathname.includes("login.html") || window.location.pathname.includes("index.html")) {
        const user = localStorage.getItem("user");
        if (user) {
            window.location.href = "home.html"; // Redirect if already logged in
        }
    }

    // ✅ Show Username on All Pages
    const usernameElement = document.getElementById("username");
    if (usernameElement) {
        const user = localStorage.getItem("user");
        if (!user) {
            window.location.href = "login.html"; // Redirect to login if not logged in
        } else {
            usernameElement.innerText = user;
        }
    }

    // ✅ Handle Logout
    const logoutButton = document.getElementById("logout");
    if (logoutButton) {
        logoutButton.addEventListener("click", function () {
            localStorage.removeItem("user"); // Remove user session
            window.location.href = "login.html"; // Redirect to login
        });
    }

    // ✅ Start J.A.R.V.I.S. on Button Click (Ensures Dynamic Navigation)
    function enableJarvis() {
        fetch("http://127.0.0.1:5001/start-jarvis")
            .then(response => response.json())
            .then(result => {
                if (result.navigate) {
                    // Check if it's an external link or internal navigation
                    if (result.navigate.startsWith("http")) {
                        window.open(result.navigate, "_blank"); // Open external links in a new tab
                    } else {
                        window.location.href = result.navigate; // Navigate to internal pages
                    }
                } else if (result.message) {
                    alert(result.message); // Display non-navigation responses
                }
            })
            .catch(error => console.error("Error starting J.A.R.V.I.S.:", error));
    }

    // ✅ Add Voice Assistant Button to All Pages
    function addVoiceAssistantButton() {
        if (!document.getElementById("voiceAssistantButton")) {
            let voiceButton = document.createElement("button");
            voiceButton.innerText = "🎙️ Voice Assistant";
            voiceButton.id = "voiceAssistantButton";
            voiceButton.style.position = "fixed";
            voiceButton.style.bottom = "20px";
            voiceButton.style.right = "20px";
            voiceButton.style.padding = "10px 15px";
            voiceButton.style.background = "red";
            voiceButton.style.color = "white";
            voiceButton.style.border = "none";
            voiceButton.style.borderRadius = "5px";
            voiceButton.style.cursor = "pointer";
            voiceButton.style.zIndex = "1000";

            voiceButton.addEventListener("click", enableJarvis);
            document.body.appendChild(voiceButton);
        }
    }

    // ✅ Add Button When Page Loads
    addVoiceAssistantButton();

    // ✅ Re-add Button After Navigation (Handles dynamic content)
    document.addEventListener("click", function () {
        setTimeout(addVoiceAssistantButton, 500);
    });
});
