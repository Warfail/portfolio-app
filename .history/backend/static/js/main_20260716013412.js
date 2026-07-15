const API_BASE = '/api';

// ==================== Load Profile ====================
async function loadProfile() {
    try {
        const response = await fetch(`${API_BASE}/profile/public`);
        const profile = await response.json();

        // Hero
        document.getElementById('heroName').innerHTML = `${profile.name}<br /><span style="color: var(--teal-primary);">${profile.title.split(' ').pop() || ''}</span>`;
        document.getElementById('heroTitle').textContent = profile.title;

        // About
        const aboutText = document.getElementById('aboutText');
        aboutText.innerHTML = profile.about.split('\n').filter(p => p.trim()).map(p => `<p>${p}</p>`).join('');

        // Stats
        const stats = document.getElementById('aboutStats');
        stats.innerHTML = `
            <div class="stat-item">
                <div class="stat-number">3+</div>
                <div class="stat-label">Years in IT Infrastructure</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">1500+</div>
                <div class="stat-label">IT Assets Managed</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">350+</div>
                <div class="stat-label">Workstations Supported</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">4</div>
                <div class="stat-label">Companies Served</div>
            </div>
        `;

        // Nav CTA
        document.getElementById('navCta').href = '#contact';
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

// ==================== Load Skills ====================
async function loadSkills() {
    try {
        const response = await fetch(`${API_BASE}/skills`);
        const skills = await response.json();

        const categories = {};
        skills.forEach(skill => {
            if (!categories[skill.category]) {
                categories[skill.category] = [];
            }
            categories[skill.category].push(skill.name);
        });

        const container = document.getElementById('skillsContainer');
        container.innerHTML = Object.entries(categories).map(([category, items]) => `
            <div class="skill-category">
                <h3>${category}</h3>
                <div class="skill-tags">
                    ${items.map(name => `<span class="skill-tag">${name}</span>`).join('')}
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading skills:', error);
    }
}

// ==================== Load Experiences ====================
async function loadExperiences() {
    try {
        const response = await fetch(`${API_BASE}/experience`);
        const experiences = await response.json();

        const container = document.getElementById('experienceContainer');
        container.innerHTML = experiences.map(exp => `
            <div class="timeline-item">
                <div class="timeline-header">
                    <div class="company">${exp.company}</div>
                    <div class="role">${exp.position}</div>
                    <div class="period">
                        ${new Date(exp.start_date).toLocaleDateString('en-US', { month: 'long', year: 'numeric' })} -
                        ${exp.is_current ? 'Present' : new Date(exp.end_date).toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}
                        ${exp.location ? ` • ${exp.location}` : ''}
                    </div>
                </div>
                <div class="timeline-body">
                    ${exp.achievements && exp.achievements.length ? `
                        <ul>
                            ${exp.achievements.map(a => `<li>${a}</li>`).join('')}
                        </ul>
                    ` : ''}
                    ${exp.description ? `<p style="color: var(--body-text-muted); margin-top: var(--space-md);">${exp.description}</p>` : ''}
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading experiences:', error);
    }
}

// ==================== Load Projects ====================
async function loadProjects() {
    try {
        const response = await fetch(`${API_BASE}/projects`);
        const projects = await response.json();

        const container = document.getElementById('projectsContainer');
        container.innerHTML = projects.map(project => `
            <div class="project-card">
                <h3>${project.title}</h3>
                <p>${project.description}</p>
                ${project.technologies && project.technologies.length ? `
                    <div class="project-tech">
                        ${project.technologies.map(tech => `<span>${tech}</span>`).join('')}
                    </div>
                ` : ''}
                ${project.project_url || project.github_url ? `
                    <a href="${project.project_url || project.github_url}" target="_blank" class="project-link">
                        View Project <i class="fas fa-arrow-right"></i>
                    </a>
                ` : ''}
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading projects:', error);
    }
}

// ==================== Contact Form ====================
document.getElementById('contact-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('contact-name').value;
    const email = document.getElementById('contact-email').value;
    const subject = document.getElementById('contact-subject').value;
    const message = document.getElementById('contact-message').value;

    const formMessage = document.getElementById('form-message');
    formMessage.className = 'form-message';
    formMessage.style.display = 'none';

    try {
        const response = await fetch(`${API_BASE}/contact`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, subject, message })
        });

        const data = await response.json();

        if (response.ok) {
            formMessage.className = 'form-message success';
            formMessage.textContent = 'Thank you for your message! I\'ll get back to you soon.';
            formMessage.style.display = 'block';
            document.getElementById('contact-form').reset();
        } else {
            formMessage.className = 'form-message error';
            formMessage.textContent = data.detail || 'Something went wrong. Please try again.';
            formMessage.style.display = 'block';
        }
    } catch (error) {
        formMessage.className = 'form-message error';
        formMessage.textContent = 'Network error. Please try again.';
        formMessage.style.display = 'block';
    }
});

// ==================== Mobile Nav ====================
const toggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');

toggle.addEventListener('click', () => {
    navLinks.classList.toggle('is-open');
    const isOpen = navLinks.classList.contains('is-open');
    toggle.setAttribute('aria-expanded', isOpen);
    toggle.innerHTML = isOpen ? '<i class="fas fa-times"></i>' : '<i class="fas fa-bars"></i>';
});

document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.innerHTML = '<i class="fas fa-bars"></i>';
    });
});

// ==================== Init ====================
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('footerYear').textContent = new Date().getFullYear();
    loadProfile();
    loadSkills();
    loadExperiences();
    loadProjects();
});