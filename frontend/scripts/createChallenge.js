document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('send-button')
    sendButton.addEventListener('click', (event) => {
        event.preventDefault()
        console.log('click')
    })
})