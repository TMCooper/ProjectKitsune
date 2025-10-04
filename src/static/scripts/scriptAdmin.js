document.addEventListener('DOMContentLoaded', () => {
    // Éléments de la porte de connexion
    const passwordGate = document.getElementById('password-gate');
    const passwordForm = document.getElementById('password-form');
    const passwordInput = document.getElementById('admin-password');
    const passwordError = document.getElementById('password-error');

    // Conteneur principal du site
    const siteWrapper = document.getElementById('site-wrapper');

    // ---- LA CORRECTION EST ICI ----
    // On déclare les éléments du panneau admin SANS les assigner tout de suite.
    // On le fera seulement une fois connecté.
    let botStatusContainer, refreshBotBtn, updateSiteBtn, updateOutput;

    // Fonction qui s'exécute APRES une connexion réussie
    function initializeAdminPanel() {
        // 1. On cache la porte de connexion et on affiche le site
        passwordGate.classList.add('fade-out');
        siteWrapper.classList.remove('hidden');
        
        // Pour une transition plus douce, on retire complètement la porte après l'animation
        setTimeout(() => {
            passwordGate.style.display = 'none';
        }, 300);

        // 2. MAINTENANT que le site est visible, on peut trouver les éléments
        botStatusContainer = document.getElementById('bot-status-container');
        refreshBotBtn = document.getElementById('refresh-bot-status');
        updateSiteBtn = document.getElementById('update-site-btn');
        updateOutput = document.getElementById('update-output');
        
        // 3. Et on attache les écouteurs d'événements
        refreshBotBtn.addEventListener('click', handleRefreshBotStatus);
        updateSiteBtn.addEventListener('click', handleUpdateSite);
    }

    // Vérifier si l'utilisateur est déjà authentifié dans la session
    if (sessionStorage.getItem('isAdminAuthenticated') === 'true') {
        initializeAdminPanel();
    }

    // Gérer la soumission du formulaire
    passwordForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const password = passwordInput.value;
        const button = passwordForm.querySelector('button');
        button.disabled = true;
        button.textContent = "Vérification...";

        try {
            const response = await fetch('/admin/verify', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ password: password })
            });
            const data = await response.json();

            if (response.ok && data.success) {
                sessionStorage.setItem('isAdminAuthenticated', 'true');
                passwordError.classList.add('hidden');
                initializeAdminPanel(); // On appelle la fonction d'initialisation
            } else {
                passwordError.classList.remove('hidden');
                passwordInput.value = '';
                passwordInput.focus();
            }
        } catch (error) {
            console.error("Erreur de connexion:", error);
            passwordError.textContent = "Erreur de connexion au serveur.";
            passwordError.classList.remove('hidden');
        } finally {
            button.disabled = false;
            button.textContent = "Connexion";
        }
    });

    // ---- Fonctions pour les boutons du panneau admin ----

    async function handleRefreshBotStatus() {
        refreshBotBtn.disabled = true;
        refreshBotBtn.textContent = 'Chargement...';
        botStatusContainer.innerHTML = '<div class="loader"></div>';
        botStatusContainer.classList.remove('placeholder');

        try {
            const response = await fetch('/api/Frieren');
            const data = await response.json();
            if (data.error) throw new Error(data.error);
            displayBotStatus(data);
        } catch (error) {
            botStatusContainer.innerHTML = `<p class="error-box">Erreur: ${error.message}</p>`;
        } finally {
            refreshBotBtn.disabled = false;
            refreshBotBtn.textContent = 'Rafraîchir le Statut';
        }
    }
    
    async function handleUpdateSite() {
        const password = prompt("Veuillez confirmer votre mot de passe administrateur :");
        if (!password) return;

        updateSiteBtn.disabled = true;
        updateSiteBtn.textContent = 'Mise à jour en cours...';
        updateOutput.textContent = 'Lancement de la commande `git pull`...';

        try {
            const response = await fetch('/admin/update', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ password: password })
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Erreur inconnue');
            updateOutput.textContent = data.output;
        } catch (error) {
            updateOutput.textContent = `ERREUR : ${error.message}`;
        } finally {
            updateSiteBtn.disabled = false;
            updateSiteBtn.textContent = 'Lancer la mise à jour';
        }
    }
    
    function displayBotStatus(data) {
        const statusClass = data.status || 'offline';
        const bannerHTML = data.banner 
            ? `<div class="bot-banner"><img src="${data.banner}" alt="Bannière du bot"></div>`
            : `<div class="bot-banner" style="height: 180px; background: linear-gradient(135deg, var(--primary-color), #6f7aff);"></div>`;

        botStatusContainer.innerHTML = `
            <div class="bot-profile-card">
                ${bannerHTML}
                <div class="bot-header">
                    <div class="bot-avatar-wrapper">
                        <img src="${data.avatar || ''}" alt="Avatar du bot">
                        <div class="bot-status-indicator ${statusClass}"></div>
                    </div>
                    <div class="bot-names">
                        <h3 class="bot-username">${data.username || 'N/A'}</h3>
                        <p class="bot-status-text ${statusClass}">${statusClass}</p>
                    </div>
                </div>
            </div>`;
    }
});