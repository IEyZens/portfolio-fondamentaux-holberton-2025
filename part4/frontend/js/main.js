/* === RPG Portfolio Main JS === */
/* Handles JWT authentication, API fetches, and DOM updates */

const API_URL = "http://localhost:5000/api";
const AUTH_URL = "http://localhost:5000/auth";

// === Check for valid token ===
function checkAuth() {
    const token = localStorage.getItem("jwt");
    if (!token) {
        window.location.href = "login.html";
    }
}

// === Fetch player profile ===
async function loadPlayerProfile() {
    checkAuth();
    const token = localStorage.getItem("jwt");
    const response = await fetch(`${AUTH_URL}/me`, {
        headers: { "Authorization": `Bearer ${token}` }
    });

    const data = await response.json();
    const playerDiv = document.getElementById("player-info");

    playerDiv.innerHTML = `
        <h2>${data.name} — Level ${data.level}</h2>
        <p>Class: ${data.class}</p>
        <div class="xp-bar">
            <div class="xp-fill" style="width:${data.xp % 100}%"></div>
        </div>
        <p>XP: ${data.xp}</p>
    `;
}

// === Logout ===
document.getElementById("logout-btn")?.addEventListener("click", () => {
    localStorage.removeItem("jwt");
    window.location.href = "login.html";
});

// === Load player info if on index ===
if (document.getElementById("player-info")) {
    loadPlayerProfile();
}
