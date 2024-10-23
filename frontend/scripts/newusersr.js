document.addEventListener('DOMContentLoaded', () => {
    const registerButton = document.getElementById('register')
    registerButton.addEventListener('click', async (event) => {
        event.preventDefault()
        const form = document.getElementById('form')
        const { user, password, repeatPassword } = { user: form.user.value, password: form.password.value, repeatPassword: form.repeatPassword.value }

        if (!checkPassword(password, repeatPassword)) {
            alert("Contraseñas no son iguales")
        }

        const response = await fetch('http://localhost:5001/create_user', {
            headers: {
                "Content-Type": "application/json"
            },
            method: "POST",
            body: JSON.stringify({"username": user, "password": password})
        });

        const data = await response.json()
        console.log(data)
    })
})

/** checks if password is the same
 * 
 * @param {*} password 
 * @param {*} repeatPassword 
 */
function checkPassword(password, repeatPassword) {
    return (password === repeatPassword) // true o false
}