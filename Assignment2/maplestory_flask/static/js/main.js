document.addEventListener('DOMContentLoaded', () => {
    const createCharacterForm = document.getElementById('createCharacterForm');
    const battleForm = document.getElementById('battleForm');
    const characterInfoDiv = document.getElementById('characterInfo');
    const inventoryInfoDiv = document.getElementById('inventoryInfo');

    createCharacterForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('characterName').value;
        const job = document.getElementById('characterJob').value;

        try {
            const response = await fetch('/create_character', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, job }),
            });

            if (response.ok) {
                const data = await response.json();
                displayCharacterInfo(data);
                alert('Character created successfully!');
            } else {
                const error = await response.json();
                alert(`Error: ${error.error}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while creating the character.');
        }
    });

    battleForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const character_name = document.getElementById('battleCharacterName').value;
        const monster_name = document.getElementById('monsterName').value;

        try {
            const response = await fetch('/battle', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ character_name, monster_name }),
            });

            if (response.ok) {
                const data = await response.json();
                alert(data.result);
                displayCharacterInfo(data.character);
            } else {
                const error = await response.json();
                alert(`Error: ${error.error}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during the battle.');
        }
    });

    function displayCharacterInfo(character) {
        characterInfoDiv.innerHTML = `
            <h3>${character.name}</h3>
            <p>Job: ${character.job}</p>
            <p>Level: ${character.level}</p>
            <p>EXP: ${character.exp} / ${character.next_level_exp}</p>
        `;

        inventoryInfoDiv.innerHTML = `
            <h3>Inventory</h3>
            <ul>
                ${character.inventory.map(item => `<li>${item}</li>`).join('')}
            </ul>
        `;

        if (character.inventory.length === 0) {
            inventoryInfoDiv.innerHTML += '<p>No items in inventory.</p>';
        }
    }

    // Function to fetch and display character info
    async function fetchCharacterInfo(name) {
        try {
            const response = await fetch(`/character/${name}`);
            if (response.ok) {
                const data = await response.json();
                displayCharacterInfo(data);
            } else {
                const error = await response.json();
                alert(`Error: ${error.error}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while fetching character info.');
        }
    }

    // Add event listeners to update character info when forms are submitted
    createCharacterForm.addEventListener('submit', () => {
        const name = document.getElementById('characterName').value;
        fetchCharacterInfo(name);
    });

    battleForm.addEventListener('submit', () => {
        const name = document.getElementById('battleCharacterName').value;
        fetchCharacterInfo(name);
    });
});