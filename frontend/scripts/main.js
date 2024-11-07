import { logInUser } from "./loginsr.js"

document.addEventListener('DOMContentLoaded', () => {
    const logInButton = document.querySelector('.login')
    localStorage.setItem('userLogged', null)

    logInButton.addEventListener('click', (event) => {
        event.preventDefault()
        logInUser()
    })
})