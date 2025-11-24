import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';

document.addEventListener('DOMContentLoaded', () => {
    
    // --- UI ELEMENTS ---
    const passwordGate = document.getElementById('password-gate');
    const modeSwitcher = document.getElementById('mode-switcher');
    const switchBtn = document.getElementById('switch-btn');
    const currentModeText = document.getElementById('current-mode-text');
    const cyberInterface = document.getElementById('cyber-interface');
    const classicInterface = document.getElementById('classic-interface');
    
    // --- CONFIG ---
    let isCyberMode = false; // <--- DÉFAUT: CLASSIQUE
    let animationId = null;

    // --- THREE.JS VARS ---
    let camera, scene, renderer, composer, controls;
    let coreGroup, particlesData = [], particlePositions, linesMesh, pointCloud, galaxyPoints;
    const maxParticleCount = 200; 
    const r = 18; 
    const connectionDistance = 6;

    // ============================================================
    // 1. AUTHENTIFICATION & START
    // ============================================================
    
    if(sessionStorage.getItem('isAdminAuthenticated') === 'true') {
        unlockSystem();
    }

    document.getElementById('password-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const pwd = document.getElementById('admin-password').value;
        try {
            const res = await fetch('/admin/verify', {
                method: 'POST', headers: {'Content-Type':'application/json'},
                body: JSON.stringify({password: pwd})
            });
            const data = await res.json();
            if(data.success) {
                sessionStorage.setItem('isAdminAuthenticated', 'true');
                unlockSystem();
            } else {
                document.getElementById('password-error').classList.remove('hidden');
            }
        } catch(e) { console.error(e); }
    });

    function unlockSystem() {
        passwordGate.style.opacity = 0;
        setTimeout(() => passwordGate.style.display = 'none', 500);
        modeSwitcher.classList.remove('hidden');
        
        // On applique le mode par défaut (Classique ici)
        if(isCyberMode) enableCyberMode();
        else enableClassicMode();
    }


    // ============================================================
    // 2. SWITCH MODE LOGIC
    // ============================================================

    switchBtn.addEventListener('click', () => {
        isCyberMode = !isCyberMode;
        if(isCyberMode) enableCyberMode();
        else enableClassicMode();
    });

    function enableCyberMode() {
        document.body.classList.remove('classic-mode');
        document.body.classList.add('cyber-body');
        classicInterface.classList.add('hidden');
        cyberInterface.classList.remove('hidden');
        currentModeText.innerText = "CYBER";
        
        if(!renderer) init3D(); 
        startAnimationLoop();
    }

    function enableClassicMode() {
        document.body.classList.remove('cyber-body');
        document.body.classList.add('classic-mode');
        cyberInterface.classList.add('hidden');
        classicInterface.classList.remove('hidden');
        currentModeText.innerText = "CLASSIC";
        
        stopAnimationLoop();
    }


    // ============================================================
    // 3. THREE.JS ENGINE
    // ============================================================

    function init3D() {
        const container = document.getElementById('canvas-container');
        if(!container) return;

        scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x050a14, 0.002);

        const loader = new THREE.TextureLoader();
        const bgTexture = loader.load('https://images.unsplash.com/photo-1534796636912-3b95b3ab5986?q=80&w=2072');
        const bgSphere = new THREE.Mesh(
            new THREE.SphereGeometry(500, 64, 64),
            new THREE.MeshBasicMaterial({ map: bgTexture, side: THREE.BackSide, transparent:true, opacity:0.6 })
        );
        scene.add(bgSphere);

        camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 2000);
        camera.position.set(0, 0, 35);

        renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        container.appendChild(renderer.domElement);

        controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.minDistance = 15; controls.maxDistance = 150;

        const renderScene = new RenderPass(scene, camera);
        const bloomPass = new UnrealBloomPass(new THREE.Vector2(window.innerWidth, window.innerHeight), 1.5, 0.4, 0.85);
        bloomPass.strength = 2.2; bloomPass.radius = 0.4; bloomPass.threshold = 0.1;
        
        composer = new EffectComposer(renderer);
        composer.addPass(renderScene);
        composer.addPass(bloomPass);

        coreGroup = new THREE.Group();
        scene.add(coreGroup);

        const coreMesh = new THREE.Mesh(new THREE.SphereGeometry(3.5, 64, 64), new THREE.MeshBasicMaterial({ color: 0x00ffff }));
        coreGroup.add(coreMesh);
        const shell = new THREE.Mesh(new THREE.IcosahedronGeometry(7, 2), new THREE.MeshBasicMaterial({ color: 0x0055ff, wireframe: true, transparent: true, opacity: 0.2 }));
        coreGroup.add(shell);

        initNeuralNetwork();
        createGalaxy();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
            composer.setSize(window.innerWidth, window.innerHeight);
        });
    }

    function initNeuralNetwork() {
        particlesData = [];
        particlePositions = new Float32Array(maxParticleCount * 3);

        for (let i = 0; i < maxParticleCount; i++) {
            const x = (Math.random() - 0.5) * r * 2;
            const y = (Math.random() - 0.5) * r * 2;
            const z = (Math.random() - 0.5) * r * 2;
            const d = Math.sqrt(x*x + y*y + z*z);
            const ratio = (r + Math.random() * 5) / d;
            
            particlePositions[i*3] = x * ratio;
            particlePositions[i*3+1] = y * ratio;
            particlePositions[i*3+2] = z * ratio;

            particlesData.push({ velocity: new THREE.Vector3(-0.5+Math.random(), -0.5+Math.random(), -0.5+Math.random()), numConnections: 0 });
        }

        pointCloud = new THREE.Points(
            new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(particlePositions, 3).setUsage(THREE.DynamicDrawUsage)),
            new THREE.PointsMaterial({ color: 0x00ffff, size: 0.5, blending: THREE.AdditiveBlending, transparent: true })
        );
        coreGroup.add(pointCloud);

        linesMesh = new THREE.LineSegments(
            new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(new Float32Array(maxParticleCount*maxParticleCount*3), 3).setUsage(THREE.DynamicDrawUsage)),
            new THREE.LineBasicMaterial({ vertexColors: false, color: 0x00ffff, transparent: true, opacity: 0.3, blending: THREE.AdditiveBlending })
        );
        coreGroup.add(linesMesh);
    }

    function updateNeuralNetwork() {
        let vertexpos = 0;
        let numConnected = 0;
        for (let i = 0; i < maxParticleCount; i++) particlesData[i].numConnections = 0;
        for (let i = 0; i < maxParticleCount; i++) {
            const pData = particlesData[i];
            particlePositions[i*3] += pData.velocity.x * 0.05;
            particlePositions[i*3+1] += pData.velocity.y * 0.05;
            particlePositions[i*3+2] += pData.velocity.z * 0.05;
            const d = Math.sqrt(particlePositions[i*3]**2 + particlePositions[i*3+1]**2 + particlePositions[i*3+2]**2);
            if(d > r+5 || d < 5) { pData.velocity.x *= -1; pData.velocity.y *= -1; pData.velocity.z *= -1; }
            for (let j = i + 1; j < maxParticleCount; j++) {
                const dx = particlePositions[i*3] - particlePositions[j*3];
                const dy = particlePositions[i*3+1] - particlePositions[j*3+1];
                const dz = particlePositions[i*3+2] - particlePositions[j*3+2];
                if (dx*dx+dy*dy+dz*dz < connectionDistance*connectionDistance) {
                    pData.numConnections++; particlesData[j].numConnections++;
                    const positions = linesMesh.geometry.attributes.position.array;
                    positions[vertexpos++] = particlePositions[i*3]; positions[vertexpos++] = particlePositions[i*3+1]; positions[vertexpos++] = particlePositions[i*3+2];
                    positions[vertexpos++] = particlePositions[j*3]; positions[vertexpos++] = particlePositions[j*3+1]; positions[vertexpos++] = particlePositions[j*3+2];
                    numConnected++;
                }
            }
        }
        linesMesh.geometry.setDrawRange(0, numConnected * 2);
        linesMesh.geometry.attributes.position.needsUpdate = true;
        pointCloud.geometry.attributes.position.needsUpdate = true;
    }

    function createGalaxy() {
        const parameters = { count: 5000, size: 0.3, radius: 120, branches: 5, spin: 1, randomness: 0.5, insideColor: 0x00ffff, outsideColor: 0xff0055 };
        const positions = new Float32Array(parameters.count * 3);
        const colors = new Float32Array(parameters.count * 3);
        const colorInside = new THREE.Color(parameters.insideColor);
        const colorOutside = new THREE.Color(parameters.outsideColor);

        for(let i = 0; i < parameters.count; i++) {
            const i3 = i * 3;
            const radius = Math.random() * parameters.radius + 20;
            const spinAngle = radius * parameters.spin;
            const branchAngle = (i % parameters.branches) / parameters.branches * Math.PI * 2;
            
            const randomX = (Math.random()-0.5) * parameters.randomness * radius;
            const randomY = (Math.random()-0.5) * parameters.randomness * radius;
            const randomZ = (Math.random()-0.5) * parameters.randomness * radius;

            positions[i3] = Math.cos(branchAngle + spinAngle) * radius + randomX;
            positions[i3+1] = randomY / 2;
            positions[i3+2] = Math.sin(branchAngle + spinAngle) * radius + randomZ;

            const mixedColor = colorInside.clone();
            mixedColor.lerp(colorOutside, radius / parameters.radius);
            colors[i3] = mixedColor.r; colors[i3+1] = mixedColor.g; colors[i3+2] = mixedColor.b;
        }
        const geometry = new THREE.BufferGeometry();
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        galaxyPoints = new THREE.Points(geometry, new THREE.PointsMaterial({ size: parameters.size, sizeAttenuation: true, depthWrite: false, blending: THREE.AdditiveBlending, vertexColors: true }));
        scene.add(galaxyPoints);
    }

    function startAnimationLoop() {
        if(animationId) return;
        const animate = () => {
            animationId = requestAnimationFrame(animate);
            controls.update();
            coreGroup.rotation.y += 0.002;
            if(galaxyPoints) galaxyPoints.rotation.y += 0.0005;
            updateNeuralNetwork();
            composer.render();
        };
        animate();
    }

    function stopAnimationLoop() {
        if(animationId) { cancelAnimationFrame(animationId); animationId = null; }
    }

    // ============================================================
    // 4. DRAG & DROP
    // ============================================================
    
    const makeDraggable = (elm) => {
        let pos1=0, pos2=0, pos3=0, pos4=0;
        const header = elm.querySelector(".drag-handle");
        if(header) header.onmousedown = (e) => {
            e.preventDefault(); pos3 = e.clientX; pos4 = e.clientY;
            document.onmouseup = () => { document.onmouseup = null; document.onmousemove = null; };
            document.onmousemove = (e) => {
                e.preventDefault(); pos1 = pos3 - e.clientX; pos2 = pos4 - e.clientY; pos3 = e.clientX; pos4 = e.clientY;
                elm.style.top = (elm.offsetTop - pos2) + "px"; elm.style.left = (elm.offsetLeft - pos1) + "px";
            };
        };
    };
    document.querySelectorAll('.draggable').forEach(makeDraggable);

    document.querySelectorAll('.dock-action').forEach(btn => {
        btn.onclick = () => {
            const targetId = btn.dataset.target;
            const el = document.getElementById(targetId);
            el.style.display = el.style.display === 'none' ? 'flex' : 'none';
        };
    });
    document.querySelectorAll('.close-win').forEach(btn => {
        btn.onclick = (e) => e.target.closest('.cyber-window').style.display = 'none';
    });
    document.getElementById('reset-cam-btn').onclick = () => {
        if(camera && controls) { camera.position.set(0, 0, 35); controls.reset(); }
    };


    // ============================================================
    // 5. DATA FETCHING
    // ============================================================

    // FETCH BOT
    const handleBotRefresh = async (btnElement) => {
        if(btnElement) btnElement.innerText = "Chargement...";
        try {
            const r = await fetch('/api/botStatus');
            const d = await r.json();
            updateAllBotUI(d);
        } catch(e) { console.error(e); }
        if(btnElement) btnElement.innerText = isCyberMode ? "SCAN NETWORK" : "Rafraîchir le Statut";
    };

    function updateAllBotUI(data) {
        const color = data.status === 'online' ? '#2ecc71' : '#7f8c8d';
        const banner = data.banner || 'https://via.placeholder.com/400x150';
        const avatar = data.avatar || 'https://via.placeholder.com/100';
        const name = data.username || 'Unknown';
        const st = data.status || 'offline';

        // CYBER UI
        const cyberBox = document.getElementById('cyber-bot-container');
        if(cyberBox) {
            cyberBox.innerHTML = `
                <div class="bot-banner"><img src="${banner}" style="width:100%; height:80px; object-fit:cover;"></div>
                <div style="display:flex; align-items:center; margin-top:10px">
                    <img src="${avatar}" style="width:50px; height:50px; border-radius:50%; border:2px solid ${color}; margin-right:10px">
                    <div><div style="font-weight:bold; color:#fff;">${name}</div><div style="color:${color}">● ${st.toUpperCase()}</div></div>
                </div>`;
        }

        // CLASSIC UI (Design Restauré)
        const classicBox = document.getElementById('classic-bot-container');
        if(classicBox) {
            classicBox.classList.remove('placeholder');
            classicBox.innerHTML = `
                <div class="bot-profile-card">
                    <div class="bot-banner"><img src="${banner}"></div>
                    <div class="bot-header-classic">
                        <div class="bot-avatar-wrapper-classic">
                            <img src="${avatar}">
                            <div class="bot-status-indicator-classic ${st}"></div>
                        </div>
                        <div class="bot-names-classic">
                            <h3 class="bot-username-classic">${name}</h3>
                            <p class="bot-status-text-classic ${st}">${st}</p>
                        </div>
                    </div>
                </div>`;
        }
    }

    // FETCH GIT
    const handleGitUpdate = async (btnElement, outputId) => {
        if(!confirm("Confirmer la mise à jour ?")) return;
        const pwd = prompt("Mot de passe Admin :");
        if(!pwd) return;
        
        const outEl = document.getElementById(outputId);
        if(outEl) outEl.innerText = "Exécution en cours...";
        
        try {
            const r = await fetch('/admin/update', {
                method:'POST', headers:{'Content-Type':'application/json'},
                body: JSON.stringify({password: pwd})
            });
            const d = await r.json();
            const txt = d.output || d.error;
            document.getElementById('cyber-update-output').innerText = txt;
            document.getElementById('classic-update-output').innerText = txt;
        } catch(e) { if(outEl) outEl.innerText = "Erreur critique."; }
    };

    // Event Listeners
    document.getElementById('cyber-refresh-bot').onclick = (e) => handleBotRefresh(e.target);
    document.getElementById('classic-refresh-bot').onclick = (e) => handleBotRefresh(e.target);
    
    document.getElementById('cyber-update-btn').onclick = (e) => handleGitUpdate(e.target, 'cyber-update-output');
    document.getElementById('classic-update-btn').onclick = (e) => handleGitUpdate(e.target, 'classic-update-output');

    setInterval(() => { document.getElementById('clock').innerText = new Date().toLocaleTimeString(); }, 1000);
});