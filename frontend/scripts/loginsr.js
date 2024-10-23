export async function logInUser(){
    const username = document.getElementById('user').value
    const password = document.getElementById('password').value

    if (username === '' || password === '') {
        alert('Username or password cannot be empty')
    }

    const response = await fetch('http://localhost:5001/login_user', {
        headers: {
            "Content-Type": "application/json"
        },
        method: "POST",
        body: JSON.stringify({"username": username, "password": password})
    });

    if (response.status === 201) {
        localStorage.setItem('userLogged', username)
        window.location.href = './challenges.html'
    } else {
        alert('User does not exist')
    }
}