const apiUrl = 'https://khalijfars.site/api.php';
let lod = document.querySelector('#loader'); // تغییر انتخابگر برای مطابقت با HTML

// Register user
document.getElementById('submit1')?.addEventListener('click', async () => {
    const username = document.getElementById('user1').value;
    const password = document.getElementById('pass1').value;

    // نمایش لودر
    lod.style.display = 'block';

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
        lod.style.display = 'none'; // مخفی کردن لودر

        if (result.error) {
            alert('Error: ' + result.error);
        } else {
            alert(result.message);
            window.location.href = 'index.html';
        }
    } catch (error) {
        lod.style.display = 'none'; // مخفی کردن لودر در صورت خطا
        console.error('Fetch error:', error);
    }
});

// Login user
document.getElementById('loginButton')?.addEventListener('click', async () => {
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    // نمایش لودر
    lod.style.display = 'block';

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
        lod.style.display = 'none'; // مخفی کردن لودر

        if (result.error) {
            alert('Error: ' + result.error);
        } else {
            alert('Login successful!');
            window.location.href = 'dashboard.html';
        }
    } catch (error) {
        lod.style.display = 'none'; // مخفی کردن لودر در صورت خطا
        console.error('Fetch error:', error);
    }
});
