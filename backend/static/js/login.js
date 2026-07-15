document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorElement = document.getElementById('login-error');

    errorElement.style.display = 'none';

    try {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch('/api/auth/token', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('access_token', data.access_token);
            window.location.href = '/admin';
        } else {
            errorElement.textContent = data.detail || 'Invalid credentials';
            errorElement.style.display = 'block';
        }
    } catch (error) {
        errorElement.textContent = 'Network error. Please try again.';
        errorElement.style.display = 'block';
    }
});

// Check if already logged in
if (localStorage.getItem('access_token')) {
    window.location.href = '/admin';
}