document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('send-button')
    sendButton.addEventListener('click', async (event) => {
        event.preventDefault()
        const title = document.getElementById('title').value
        const document = document.getElementById('document').value
        const userToShare = document.getElementById('user').value
        const userLogged = localStorage.getItem('userLogged')

        if (title === '' || document === '' || userToShare === '' || userLogged === ''){
            alert('There is something that cannot be empty... Or maybe you are not log in correctly?')
        }

        const response = await fetch('http://localhost:5001/create_challenge', {
            headers: {
                'Content-Type': 'application/json'
            },
            method: 'POST',
            body: JSON.stringify({"title": title, "document": document, "userLogged": userLogged, "userToShare": userToShare})
        })

        if (response.status === 201) {
            alert('El challenge se ha creado correctamente')
            window.location.hred='./challenges.html'
        }
    })
})