const apiUrl = 'https://khalijfars.site/api.php';

// Show and hide loader animations
function showLoader() {
    document.getElementById("btnText").classList.add("hidden");
    document.getElementById("loadingDots").classList.remove("hidden");
}

function hideLoader() {
    document.getElementById("btnText").classList.remove("hidden");
    document.getElementById("loadingDots").classList.add("hidden");
}

function showAlert(message, isError = false) {
    const alertBox = document.getElementById("alertBox");
    alertBox.style.display = "block";
    alertBox.innerText = message;
    alertBox.style.backgroundColor = isError ? "rgb(255, 104, 104)" : "rgb(104, 255, 142)";
}

// User registration process
document.getElementById('submit1')?.addEventListener('click', async () => {
    const username = document.getElementById('user1').value.trim();
    const password = document.getElementById('pass1').value.trim();

    if (!username || !password) {
        showAlert("Fill all fields!", true);
        return;
    }

    // Validate username and password length
    if (username.length < 5 || password.length < 5) {
        showAlert("Min 5 chars!", true);
        return;
    }

    // Check for Persian characters in username
    const persianRegex = /[\u0600-\u06FF]/;
    if (persianRegex.test(username)) {
        showAlert("No Persian!", true);
        return;
    }

    showLoader(); // Show loader animation

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({
                action: 'register',
                username: username,
                password: password
            }),
        });

        const responseText = await response.text(); 
        console.log("Response:", responseText);

        try {
            const result = JSON.parse(responseText);

            if (result.error) {
                showAlert("Exists!", true);
            } else {
                showAlert("Success!");
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 1500);
            }
        } catch (jsonError) {
            console.error("JSON error:", jsonError);
            showAlert("Exists!", true);
        }
    } catch (error) {
        hideLoader();
        if (error.message.includes("Failed to fetch")) {
            showAlert("Server error!", true);
        } else {
            showAlert("Exists!", true);
        }
        console.error('Fetch error:', error);
    } finally {
        hideLoader();
    }
});

// User login process
document.getElementById('submit2')?.addEventListener('click', async () => {
    const username = document.getElementById('user2').value.trim();
    const password = document.getElementById('pass2').value.trim();

    if (!username || !password) {
        showAlert("Fill all fields!", true);
        return;
    }

    // Validate username and password length
    if (username.length < 5 || password.length < 5) {
        showAlert("Min 5 chars!", true);
        return;
    }

    // Check for Persian characters in username
    const persianRegex = /[\u0600-\u06FF]/;
    if (persianRegex.test(username)) {
        showAlert("No Persian!", true);
        return;
    }

    showLoader(); // Show loader animation

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({
                action: 'login',
                username: username,
                password: password
            }),
        });

        const result = await response.json();
        hideLoader(); 

        if (!response.ok || result.error) {
            throw new Error(result.error || "Server error!");
        }

        // Save user data to Local Storage
        localStorage.setItem("username", username);
        localStorage.setItem("password", password);

        showAlert("Welcome!");
        setTimeout(() => {
            window.location.href = 'dashboard.html';
        }, 1500); 
    } catch (error) {
        hideLoader(); 
        showAlert("Not Found", true);
        console.error('Fetch error:', error);
    }
});
