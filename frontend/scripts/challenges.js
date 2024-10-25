document.addEventListener('DOMContentLoaded', async () => {
    const privateChallenges = document.getElementById('private-challenges')
    const publicChallenges = document.getElementById('public-challenges')

    const response = await fetch('http://localhost:5001/get_public_challenges')
    if(!response.ok){
        alert('Ups, something went wrong')
    } else {
        const data = await response.json()
        data.response.forEach(challenge => {
            const htmlElement = `
            <div style="border: 1px solid #ccc; border-radius: 8px; padding: 16px; margin-bottom: 1rem; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h3 style="margin: 0; font-size: 1.5rem; color: #333;">${challenge.title}</h3>
                <p style="margin: 8px 0; font-size: 1rem; color: #555;">${challenge.content}</p>
            </div>
        `;
        publicChallenges.innerHTML += htmlElement
    })
    }
})