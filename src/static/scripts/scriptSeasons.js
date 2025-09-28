document.addEventListener('DOMContentLoaded', () => {

    const form = document.getElementById("season-form");
    const container = document.getElementById("anime-container");
    const loader = document.getElementById("loader");
    const errorMessage = document.getElementById("error-message");
    
    const yearInput = document.getElementById("year");
    const seasonInput = document.getElementById("season");
    const typeInput = document.getElementById("type");

    async function loadAnimes(year, season, type) {
        loader.classList.remove("hidden");
        errorMessage.classList.add("hidden");
        container.innerHTML = "";

        try {
            const response = await fetch(`/api/getSeasonOut?seasons=${season}&y=${year}&type=${type}`);
            if (!response.ok) {
                throw new Error(`Erreur HTTP: ${response.status}`);
            }
            const data = await response.json();
            displayAnimes(data);

        } catch (err) {
            console.error("Erreur lors du chargement :", err);
            errorMessage.classList.remove("hidden");
        } finally {
            loader.classList.add("hidden");
        }
    }

    function displayAnimes(animes) {
        if (!animes || animes.length === 0) {
            container.innerHTML = `<p id="no-results">Aucun animé trouvé pour ces critères.</p>`;
            return;
        }

        animes.forEach(anime => {
            const card = document.createElement("div");
            card.className = "anime-card";

            const studios = anime.studios_name?.join(", ") || "Inconnu";
            const genres = anime.genres_name?.join(", ") || "N/A";

            card.innerHTML = `
                <img src="${anime.image_jpg_big || anime.image_jpg || ''}" alt="Affiche de ${anime.title}">
                <div class="anime-card-content">
                    <h3 class="anime-title">${anime.title}</h3>
                    <div class="anime-info"><strong>Studio :</strong> ${studios}</div>
                    <div class="anime-info"><strong>Genres :</strong> ${genres}</div>
                    <div class="anime-info"><strong>Note :</strong> ${anime.rating || "?"}</div>
                </div>
                <div class="anime-card-footer">
                    <a href="${anime.url}" target="_blank" rel="noopener noreferrer" class="mal-link">Voir sur MAL</a>
                </div>
            `;
            container.appendChild(card);
        });
    }

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        loadAnimes(yearInput.value, seasonInput.value, typeInput.value);
    });

    // Chargement initial des données au premier affichage de la page
    loadAnimes(yearInput.value, seasonInput.value, typeInput.value);
});