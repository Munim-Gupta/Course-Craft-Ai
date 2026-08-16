/* ==========================================================================
   CourseCraft AI - Interactive Application Logic & Live Background Engine
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initLiveBackgroundCanvas();
    initMarkdownParser();
    initCourseGeneratorLoader();
    initStudioNavigation();
    initDashboardSearch();
    initCodeCopyButtons();
});

/**
 * Automatically parses raw markdown inside .lesson-body elements into clean HTML
 */
function initMarkdownParser() {
    const lessonBodies = document.querySelectorAll('.lesson-body');
    
    lessonBodies.forEach(body => {
        const rawText = body.innerHTML.trim();
        if (rawText.includes('###') || rawText.includes('---') || (rawText.includes('**') && !rawText.includes('<p>'))) {
            if (typeof marked !== 'undefined' && typeof marked.parse === 'function') {
                const textToParse = rawText.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
                body.innerHTML = marked.parse(textToParse);
            }
        }
    });
}

/**
 * Live Background Canvas - Interactive Mouse Particle Network
 */
function initLiveBackgroundCanvas() {
    const canvas = document.getElementById('liveBackgroundCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width, height;
    let particles = [];
    const particleCount = Math.min(75, Math.floor(window.innerWidth / 22));

    // Mouse Tracking State
    const mouse = {
        x: null,
        y: null,
        radius: 180
    };

    window.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;

        // Mouse Parallax for Floating Background Orbs
        const moveX = (e.clientX - window.innerWidth / 2) * 0.03;
        const moveY = (e.clientY - window.innerHeight / 2) * 0.03;
        
        const orb1 = document.querySelector('.orb-1');
        const orb2 = document.querySelector('.orb-2');
        const orb3 = document.querySelector('.orb-3');

        if (orb1) orb1.style.transform = `translate(${moveX}px, ${moveY}px)`;
        if (orb2) orb2.style.transform = `translate(${-moveX * 1.2}px, ${-moveY * 1.2}px)`;
        if (orb3) orb3.style.transform = `translate(${moveX * 0.8}px, ${-moveY * 0.8}px)`;
    });

    window.addEventListener('mouseleave', () => {
        mouse.x = null;
        mouse.y = null;
    });

    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }

    window.addEventListener('resize', () => {
        resize();
        createParticles();
    });
    resize();

    class Particle {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.baseRadius = Math.random() * 2.5 + 1.2;
            this.radius = this.baseRadius;
            this.vx = (Math.random() - 0.5) * 0.6;
            this.vy = (Math.random() - 0.5) * 0.6;
            this.alpha = Math.random() * 0.5 + 0.3;
            
            const colors = ['#6366f1', '#8b5cf6', '#06b6d4', '#38bdf8', '#a855f7'];
            this.color = colors[Math.floor(Math.random() * colors.length)];
        }

        update() {
            this.x += this.vx;
            this.y += this.vy;

            // Bounce / Wrap Screen Boundaries
            if (this.x < 0) this.x = width;
            if (this.x > width) this.x = 0;
            if (this.y < 0) this.y = height;
            if (this.y > height) this.y = 0;

            // Mouse Interactive Repulsion & Growth
            if (mouse.x !== null && mouse.y !== null) {
                const dx = mouse.x - this.x;
                const dy = mouse.y - this.y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < mouse.radius) {
                    const angle = Math.atan2(dy, dx);
                    const force = (mouse.radius - dist) / mouse.radius;
                    const pushX = Math.cos(angle) * force * 3;
                    const pushY = Math.sin(angle) * force * 3;

                    this.x -= pushX;
                    this.y -= pushY;
                    this.radius = Math.min(this.baseRadius + 2.5, 6);
                } else {
                    if (this.radius > this.baseRadius) {
                        this.radius -= 0.1;
                    }
                }
            } else {
                if (this.radius > this.baseRadius) {
                    this.radius -= 0.1;
                }
            }
        }

        draw() {
            ctx.save();
            ctx.globalAlpha = this.alpha;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.shadowBlur = 14;
            ctx.shadowColor = this.color;
            ctx.fill();
            ctx.restore();
        }
    }

    function createParticles() {
        particles = [];
        for (let i = 0; i < particleCount; i++) {
            particles.push(new Particle());
        }
    }

    function connectParticles() {
        const maxDist = 135;

        // 1. Connect Mouse to Nearby Particles
        if (mouse.x !== null && mouse.y !== null) {
            for (let i = 0; i < particles.length; i++) {
                const dx = mouse.x - particles[i].x;
                const dy = mouse.y - particles[i].y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < mouse.radius) {
                    const opacity = (1 - dist / mouse.radius) * 0.45;
                    ctx.save();
                    ctx.globalAlpha = opacity;
                    ctx.beginPath();
                    ctx.moveTo(mouse.x, mouse.y);
                    ctx.lineTo(particles[i].x, particles[i].y);
                    ctx.strokeStyle = '#06b6d4';
                    ctx.lineWidth = 1.5;
                    ctx.shadowBlur = 8;
                    ctx.shadowColor = '#06b6d4';
                    ctx.stroke();
                    ctx.restore();
                }
            }
        }

        // 2. Connect Particles to each other
        for (let a = 0; a < particles.length; a++) {
            for (let b = a + 1; b < particles.length; b++) {
                const dx = particles[a].x - particles[b].x;
                const dy = particles[a].y - particles[b].y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < maxDist) {
                    const opacity = (1 - dist / maxDist) * 0.2;
                    ctx.save();
                    ctx.globalAlpha = opacity;
                    ctx.beginPath();
                    ctx.moveTo(particles[a].x, particles[a].y);
                    ctx.lineTo(particles[b].x, particles[b].y);
                    ctx.strokeStyle = '#6366f1';
                    ctx.lineWidth = 1;
                    ctx.stroke();
                    ctx.restore();
                }
            }
        }
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);

        for (let i = 0; i < particles.length; i++) {
            particles[i].update();
            particles[i].draw();
        }

        connectParticles();
        requestAnimationFrame(animate);
    }

    createParticles();
    animate();
}

/**
 * Shows loading screen overlay during course generation
 */
function initCourseGeneratorLoader() {
    const genForm = document.getElementById('courseGeneratorForm');
    const loadingOverlay = document.getElementById('loadingOverlay');

    if (genForm && loadingOverlay) {
        genForm.addEventListener('submit', (e) => {
            const topicInput = document.getElementById('topicInput');
            if (topicInput && topicInput.value.trim() !== '') {
                loadingOverlay.style.display = 'flex';
            }
        });
    }
}

/**
 * Handles course studio lesson tab switching
 */
function initStudioNavigation() {
    const lessonButtons = document.querySelectorAll('.lesson-item-btn');
    const lessonCards = document.querySelectorAll('.lesson-display-card');

    if (lessonButtons.length > 0) {
        lessonButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const targetLessonId = btn.getAttribute('data-lesson-target');
                
                lessonButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                lessonCards.forEach(card => {
                    if (card.id === targetLessonId) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });

                if (window.innerWidth < 992) {
                    const studioMain = document.getElementById('studioMainWorkspace');
                    if (studioMain) {
                        studioMain.scrollIntoView({ behavior: 'smooth' });
                    }
                }
            });
        });
    }
}

/**
 * Filter courses in dashboard in real-time
 */
function initDashboardSearch() {
    const searchInput = document.getElementById('courseSearchInput');
    const courseCards = document.querySelectorAll('.course-card-wrapper');

    if (searchInput && courseCards.length > 0) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();

            courseCards.forEach(card => {
                const title = card.getAttribute('data-course-title').toLowerCase();
                const category = card.getAttribute('data-course-category').toLowerCase();

                if (title.includes(query) || category.includes(query)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
}

/**
 * Copies code block contents to clipboard
 */
function initCodeCopyButtons() {
    const copyBtns = document.querySelectorAll('.copy-code-btn');

    copyBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const codeBlock = btn.closest('.code-block-container').querySelector('code');
            if (codeBlock) {
                navigator.clipboard.writeText(codeBlock.innerText).then(() => {
                    const originalText = btn.innerText;
                    btn.innerText = 'Copied!';
                    setTimeout(() => {
                        btn.innerText = originalText;
                    }, 2000);
                });
            }
        });
    });
}
