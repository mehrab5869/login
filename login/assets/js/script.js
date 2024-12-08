
const apiUrl = 'https://khalijfars.site/api.php';

// Register user
document.getElementById('registerButton')?.addEventListener('click', async () => {
    const username = document.getElementById('registerUsername').value;
    const password = document.getElementById('registerPassword').value;

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

        const result = await response.json();
        if (result.error) {
            alert('Error: ' + result.error);
        } else {
            alert(result.message);
            window.location.href = 'index.html';
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
});


// Login user
document.getElementById('submit')?.addEventListener('click', async () => {
    const username = document.getElementById("loginUsername").value.trim();
    const password = document.getElementById("loginPassword").value.trim();

    if (!username || !password) {
        alert("Please fill in all fields.");
        return;
    }

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
        if (result.error) {
            alert('Error: ' + result.error);
        } else {
            alert('Login successful!');
            window.location.href = 'dashboard.html';
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
});

