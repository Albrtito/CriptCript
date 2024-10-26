document.addEventListener('DOMContentLoaded', async () => {
    const privateChallenges = document.getElementById('private-challenges')
    const publicChallenges = document.getElementById('public-challenges')

    const publicResponse = await fetch('http://localhost:5001/get_public_challenges')
    if(!publicResponse.ok){
        alert('Ups, something went wrong when rendering the public challenges')
    } else {
        const data = await publicResponse.json()
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

    const user = localStorage.getItem('userLogged')
    const privateResponse = await fetch(`http://localhost:5001/get_private_challenges?user=${user}`)
    if(!privateResponse.ok){
        alert('Ups, something went wrong when rendering your private challenges')
    } else {
        const data = await privateResponse.json()
        data.response.forEach(challenge => {
            const htmlElement = `
            <div style="border: 1px solid #ccc; border-radius: 8px; padding: 16px; margin-bottom: 1rem; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h3 style="margin: 0; font-size: 1.5rem; color: #333;">${challenge.title}</h3>
                <p style="margin: 8px 0; font-size: 1rem; color: #555;">${challenge.content}</p>
            </div>
        `;
        privateChallenges.innerHTML += htmlElement
    })
    }
})