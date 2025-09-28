document.addEventListener('DOMContentLoaded', () => {

    const searchInput = document.getElementById('anime-search-input');
    const suggestionsContainer = document.getElementById('suggestions-container');
    const detailsContainer = document.getElementById('anime-details-container');
    const loader = document.getElementById('loader');

    let debounceTimer;

    // Écouteur sur la barre de recherche
    searchInput.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        const query = searchInput.value.trim();

        if (query.length < 3) {
            suggestionsContainer.innerHTML = '';
            suggestionsContainer.classList.add('hidden');
            return;
        }
        
        suggestionsContainer.classList.remove('hidden');
        debounceTimer = setTimeout(() => {
            fetchSuggestions(query);
        }, 300);
    });

    // Fonction pour récupérer les suggestions
    async function fetchSuggestions(query) {
        suggestionsContainer.innerHTML = '<div class="suggestion-item">Chargement...</div>';
        try {
            const response = await fetch(`/api/getAnimeSearch?q=${query}&l=5`);
            const suggestions = await response.json();
            
            // DEBUG: Vérifie ce que retourne l'API
            console.log("Données reçues de l'API:", suggestions);
            
            // Vérifie chaque anime individuellement
            suggestions.forEach((anime, index) => {
                console.log(`Anime ${index}:`, {
                    title: anime.title,
                    image_jpg_small: anime.image_jpg_small,
                    hasImage: !!anime.image_jpg_small
                });
            });
            
            displaySuggestions(suggestions);
        } catch (error) {
            console.error("Erreur lors de la récupération des suggestions:", error);
            suggestionsContainer.innerHTML = '<div class="suggestion-item">Erreur de chargement.</div>';
        }
    }

    // MODIFIÉ : Fonction d'affichage des suggestions
    function displaySuggestions(suggestions) {
        suggestionsContainer.innerHTML = '';
        if (suggestions.length === 0) {
            suggestionsContainer.innerHTML = '<div class="suggestion-item">Aucun résultat trouvé.</div>';
            return;
        }

        suggestions.forEach(anime => {
            const item = document.createElement('div');
            item.className = 'suggestion-item';

            // MODIFIÉ : On utilise maintenant "anime.image_jpg_small"
            const imageHtml = anime.image_jpg 
                ? `<img src="${anime.image_jpg}" alt="${anime.title}" class="suggestion-image">`
                : '<div class="suggestion-image-placeholder"></div>';

            item.innerHTML = `
                ${imageHtml}
                <span class="suggestion-title">${anime.title}</span>
            `;

            item.dataset.id = anime.id;
            item.addEventListener('click', () => {
                fetchDetails(anime.id);
                suggestionsContainer.innerHTML = '';
                suggestionsContainer.classList.add('hidden');
                searchInput.value = anime.title;
            });
            suggestionsContainer.appendChild(item);
        });
    }

    // Fonction pour récupérer les détails d'un animé
    async function fetchDetails(animeId) {
        detailsContainer.innerHTML = ''; 
        loader.classList.remove('hidden');
        // MODIFIÉ : Réinitialiser le style du conteneur
        detailsContainer.style.backgroundImage = 'none';
        detailsContainer.classList.remove('has-background');

        try {
            const response = await fetch(`/api/getinfoByid?id=${animeId}`);
            const anime = await response.json();
            displayDetails(anime);
        } catch (error)
        {
            console.error("Erreur lors de la récupération des détails:", error);
            detailsContainer.innerHTML = '<div class="error-box">Impossible de charger les informations.</div>';
        } finally {
            loader.classList.add('hidden');
        }
    }

    // MODIFIÉ : Fonction pour afficher la fiche détaillée avec le nouveau layout en 2 colonnes
    function displayDetails(anime) {
        const genres = anime.genres_name.map(g => `<span class="tag">${g}</span>`).join('');
        const studios = anime.studios_name.map(s => `<span class="tag">${s}</span>`).join('');

        // La nouvelle structure HTML utilise une grille CSS
        detailsContainer.innerHTML = `
            <div class="anime-details-grid">
                <div class="anime-poster">
                    <img src="${anime.image_jpg_big || anime.image_jpg}" alt="Affiche de ${anime.title}">
                </div>

                <div class="anime-info">
                    <h2>${anime.title}</h2>
                    <h3 class="subtitle">${anime.title_english || anime.title_japanese}</h3>
                    
                    <div class="stats-grid">
                        <div class="stat-item"><div class="label">Rang</div><div class="value">#${anime.rank || 'N/A'}</div></div>
                        <div class="stat-item"><div class="label">Épisodes</div><div class="value">${anime.episodes_number || '?'}</div></div>
                        <div class="stat-item"><div class="label">Saison</div><div class="value">${anime.season ? anime.season.charAt(0).toUpperCase() + anime.season.slice(1) : '?'}</div></div>
                        <div class="stat-item"><div class="label">Statut</div><div class="value">${anime.status || '?'}</div></div>
                    </div>

                    <div class="section-header">
                        <h4 class="section-title">Synopsis</h4>
                        <button class="translate-btn" data-target="synopsis-text">Traduire</button>
                    </div>
                    <p class="synopsis" id="synopsis-text" data-original-text="${escape(anime.synopsis || "Aucun synopsis disponible.")}">${anime.synopsis || "Aucun synopsis disponible."}</p>

                    <h4 class="section-title">Genres</h4>
                    <div class="tag-list">${genres}</div>

                    <h4 class="section-title">Studios</h4>
                    <div class="tag-list">${studios}</div>

                    ${anime.background ? `
                        <div class="section-header">
                            <h4 class="section-title">Contexte</h4>
                            <button class="translate-btn" data-target="background-text">Traduire</button>
                        </div>
                        <p class="synopsis" id="background-text" data-original-text="${escape(anime.background)}">${anime.background}</p>
                    ` : ''}
                </div>
            </div>
        `;
    }
    
    // La logique de traduction reste la même, elle est très bien !
    detailsContainer.addEventListener('click', async (e) => {
        if (e.target.classList.contains('translate-btn')) {
            const button = e.target;
            const targetId = button.dataset.target;
            const textElement = document.getElementById(targetId);

            if (!textElement) return;

            const currentText = textElement.textContent;
            const originalText = unescape(textElement.dataset.originalText);
            
            if (currentText !== originalText) {
                textElement.textContent = originalText;
                button.textContent = 'Traduire';
                return;
            }

            button.textContent = 'Traduction...';
            button.disabled = true;

            try {
                const response = await fetch('/api/translate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: originalText })
                });
                const data = await response.json();
                if (response.ok) {
                    textElement.textContent = data.translated_text;
                    button.textContent = "Voir l'original";
                } else {
                    throw new Error(data.error || 'Erreur inconnue');
                }
            } catch (error) {
                console.error("Erreur de traduction:", error);
                textElement.textContent = originalText;
                button.textContent = 'Réessayer';
            } finally {
                button.disabled = false;
            }
        }
    });

    // Cacher les suggestions si on clique ailleurs sur la page
    document.addEventListener('click', (e) => {
        if (!suggestionsContainer.contains(e.target) && e.target !== searchInput) {
            suggestionsContainer.innerHTML = '';
            suggestionsContainer.classList.add('hidden');
        }
    });
});