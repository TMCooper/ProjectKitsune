document.addEventListener("DOMContentLoaded", function() {

    const dayForm = document.getElementById("dayForm");
    const resultsDiv = document.getElementById("results");
    const loader = document.getElementById("loader");
    const errorDiv = document.getElementById("error");
    const daySelect = document.getElementById("day");

    dayForm.addEventListener("submit", async function(e) {
        e.preventDefault(); 
        
        loader.classList.remove("hidden");
        errorDiv.classList.add("hidden");
        resultsDiv.innerHTML = "";

        try {
            const day = daySelect.value;
            const res = await fetch(`/api/getCurrentOut?day=${day}`);

            if (!res.ok) {
                throw new Error(`Erreur HTTP: ${res.status}`);
            }

            const data = await res.json();
            displayAnimes(data);

        } catch (error) {
            console.error("Erreur lors de la récupération des données:", error);
            errorDiv.classList.remove("hidden");
        } finally {
            loader.classList.add("hidden");
        }
    });

    function displayAnimes(animes) {
        if (!animes || animes.length === 0) {
            resultsDiv.innerHTML = "<p>Aucun anime trouvé pour ce jour.</p>";
            return;
        }

        animes.forEach(anime => {
            const card = document.createElement("div");
            card.className = "anime-card";

            const studios = anime.studios_name?.join(", ") || "N/A";
            const genres = anime.genres_name?.join(", ") || "N/A";

            card.innerHTML = `
                <img src="${anime.image_jpg || ''}" alt="Affiche de ${anime.title}">
                <div class="anime-card-content">
                    <h3>${anime.title}</h3>
                    <p><b>🎬 Studios :</b> ${studios}</p>
                    <p><b>🎭 Genres :</b> ${genres}</p>
                    <p><b>📺 Épisodes :</b> ${anime.episodes_number || "?"}</p>
                    <p><b>Statut :</b> ${anime.status || "?"}</p>
                    <p><b>⭐ Note :</b> ${anime.rating || "?"}</p>
                </div>
                <div class="anime-card-footer">
                    <a href="${anime.url}" target="_blank" rel="noopener noreferrer">Voir sur MyAnimeList</a>
                </div>
            `;

            resultsDiv.appendChild(card);
        });
    }
});