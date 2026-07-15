const API_BASE = '/api';
let token = localStorage.getItem('access_token');

if (!token) {
    window.location.href = '/login';
}

async function apiRequest(url, options = {}) {
    const headers = {
        'Authorization': `Bearer ${token}`,
        ...options.headers
    };

    if (!(options.body instanceof FormData)) {
        headers['Content-Type'] = 'application/json';
    }

    const response = await fetch(url, {
        ...options,
        headers
    });

    if (response.status === 401) {
        localStorage.removeItem('access_token');
        window.location.href = '/login';
        throw new Error('Unauthorized');
    }

    return response;
}

// ==================== Sidebar Navigation ====================
document.querySelectorAll('.sidebar-menu li').forEach(item => {
    item.addEventListener('click', () => {
        document.querySelectorAll('.sidebar-menu li').forEach(li => li.classList.remove('active'));
        item.classList.add('active');

        const section = item.dataset.section;
        document.querySelectorAll('.admin-section').forEach(s => s.classList.remove('active'));
        document.getElementById(`${section}-section`).classList.add('active');
    });
});

// ==================== Profile Management ====================
async function loadProfile() {
    try {
        const response = await apiRequest(`${API_BASE}/profile`);
        const profile = await response.json();

        document.getElementById('admin-name').value = profile.name || '';
        document.getElementById('admin-title').value = profile.title || '';
        document.getElementById('admin-about').value = profile.about || '';
        document.getElementById('admin-email').value = profile.email || '';
        document.getElementById('admin-phone').value = profile.phone || '';
        document.getElementById('admin-location').value = profile.location || '';
        document.getElementById('admin-linkedin').value = profile.linkedin || '';
        document.getElementById('admin-github').value = profile.github || '';

        if (profile.profile_image) {
            document.getElementById('profile-image-preview').innerHTML = `
                <img src="${profile.profile_image}" alt="Profile">
                <button type="button" onclick="removeProfileImage()" class="btn btn-secondary" style="margin-top:8px;padding:4px 12px;font-size:12px;">Remove</button>
            `;
        }
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

document.getElementById('profile-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = {
        name: document.getElementById('admin-name').value,
        title: document.getElementById('admin-title').value,
        about: document.getElementById('admin-about').value,
        email: document.getElementById('admin-email').value,
        phone: document.getElementById('admin-phone').value,
        location: document.getElementById('admin-location').value,
        linkedin: document.getElementById('admin-linkedin').value,
        github: document.getElementById('admin-github').value
    };

    try {
        const response = await apiRequest(`${API_BASE}/profile`, {
            method: 'PUT',
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            alert('Profile updated successfully!');
            loadProfile();
        }
    } catch (error) {
        console.error('Error updating profile:', error);
        alert('Failed to update profile.');
    }
});

document.getElementById('admin-profile-image').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await apiRequest(`${API_BASE}/upload/image`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (response.ok) {
            await apiRequest(`${API_BASE}/profile`, {
                method: 'PUT',
                body: JSON.stringify({ profile_image: data.url })
            });

            document.getElementById('profile-image-preview').innerHTML = `
                <img src="${data.url}" alt="Profile">
                <button type="button" onclick="removeProfileImage()" class="btn btn-secondary" style="margin-top:8px;padding:4px 12px;font-size:12px;">Remove</button>
            `;
            alert('Profile image uploaded successfully!');
        }
    } catch (error) {
        console.error('Error uploading image:', error);
        alert('Failed to upload image.');
    }
});

async function removeProfileImage() {
    const img = document.getElementById('profile-image-preview').querySelector('img');
    if (img) {
        const publicId = img.src.split('/').pop().split('.')[0];
        try {
            await apiRequest(`${API_BASE}/upload/image/${publicId}`, { method: 'DELETE' });
        } catch (error) {
            console.error('Error deleting image:', error);
        }
    }

    await apiRequest(`${API_BASE}/profile`, {
        method: 'PUT',
        body: JSON.stringify({ profile_image: '' })
    });

    document.getElementById('profile-image-preview').innerHTML = '';
    alert('Profile image removed.');
}

// ==================== Skills Management ====================
async function loadSkills() {
    try {
        const response = await apiRequest(`${API_BASE}/skills`);
        const skills = await response.json();

        const container = document.getElementById('skills-list');
        container.innerHTML = skills.map(skill => `
            <div class="admin-item" data-id="${skill.id}">
                <div class="admin-item-content">
                    <h4>${skill.name}</h4>
                    <div class="meta">${skill.category} ${skill.level ? `• ${skill.level}%` : ''}</div>
                </div>
                <div class="admin-item-actions">
                    <button class="edit-btn" onclick="editSkill(${skill.id})">Edit</button>
                    <button class="delete-btn" onclick="deleteSkill(${skill.id})">Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading skills:', error);
    }
}

document.getElementById('skill-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const skillData = {
        name: document.getElementById('skill-name').value,
        category: document.getElementById('skill-category').value,
        level: document.getElementById('skill-level').value ? parseInt(document.getElementById('skill-level').value) : null
    };

    try {
        const response = await apiRequest(`${API_BASE}/skills`, {
            method: 'POST',
            body: JSON.stringify(skillData)
        });

        if (response.ok) {
            document.getElementById('skill-form').reset();
            loadSkills();
            alert('Skill added successfully!');
        }
    } catch (error) {
        console.error('Error adding skill:', error);
        alert('Failed to add skill.');
    }
});

async function editSkill(id) {
    try {
        const response = await apiRequest(`${API_BASE}/skills/${id}`);
        const skill = await response.json();

        document.getElementById('skill-name').value = skill.name;
        document.getElementById('skill-category').value = skill.category;
        document.getElementById('skill-level').value = skill.level || '';

        const form = document.getElementById('skill-form');
        const submitBtn = form.querySelector('button[type="submit"]');
        submitBtn.textContent = 'Update Skill';
        form.dataset.editId = id;

        form.onsubmit = async (e) => {
            e.preventDefault();
            const updatedData = {
                name: document.getElementById('skill-name').value,
                category: document.getElementById('skill-category').value,
                level: document.getElementById('skill-level').value ? parseInt(document.getElementById('skill-level').value) : null
            };

            try {
                const resp = await apiRequest(`${API_BASE}/skills/${id}`, {
                    method: 'PUT',
                    body: JSON.stringify(updatedData)
                });

                if (resp.ok) {
                    form.reset();
                    submitBtn.textContent = 'Add Skill';
                    form.dataset.editId = '';
                    form.onsubmit = null;
                    loadSkills();
                    alert('Skill updated successfully!');
                }
            } catch (error) {
                console.error('Error updating skill:', error);
                alert('Failed to update skill.');
            }
        };
    } catch (error) {
        console.error('Error fetching skill:', error);
    }
}

async function deleteSkill(id) {
    if (!confirm('Are you sure you want to delete this skill?')) return;

    try {
        const response = await apiRequest(`${API_BASE}/skills/${id}`, { method: 'DELETE' });
        if (response.ok) {
            loadSkills();
            alert('Skill deleted successfully!');
        }
    } catch (error) {
        console.error('Error deleting skill:', error);
        alert('Failed to delete skill.');
    }
}

// ==================== Experience Management ====================
async function loadExperiences() {
    try {
        const response = await apiRequest(`${API_BASE}/experience`);
        const experiences = await response.json();

        const container = document.getElementById('experience-list');
        container.innerHTML = experiences.map(exp => `
            <div class="admin-item" data-id="${exp.id}">
                <div class="admin-item-content">
                    <h4>${exp.position} at ${exp.company}</h4>
                    <div class="meta">${new Date(exp.start_date).toLocaleDateString()} - ${exp.is_current ? 'Present' : new Date(exp.end_date).toLocaleDateString()}</div>
                </div>
                <div class="admin-item-actions">
                    <button class="edit-btn" onclick="editExperience(${exp.id})">Edit</button>
                    <button class="delete-btn" onclick="deleteExperience(${exp.id})">Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading experiences:', error);
    }
}

document.getElementById('experience-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const form = e.target;
    const isEdit = form.dataset.editId;
    const url = isEdit ? `${API_BASE}/experience/${form.dataset.editId}` : `${API_BASE}/experience`;
    const method = isEdit ? 'PUT' : 'POST';

    const expData = {
        company: document.getElementById('exp-company').value,
        position: document.getElementById('exp-position').value,
        location: document.getElementById('exp-location').value,
        start_date: document.getElementById('exp-start-date').value,
        end_date: document.getElementById('exp-end-date').value || null,
        is_current: document.getElementById('exp-current').checked,
        description: document.getElementById('exp-description').value,
        achievements: document.getElementById('exp-achievements').value.split(',').map(s => s.trim()).filter(s => s)
    };

    try {
        const response = await apiRequest(url, { method, body: JSON.stringify(expData) });
        if (response.ok) {
            form.reset();
            form.dataset.editId = '';
            form.querySelector('button[type="submit"]').textContent = 'Save Experience';
            loadExperiences();
            alert(isEdit ? 'Experience updated successfully!' : 'Experience added successfully!');
        }
    } catch (error) {
        console.error('Error saving experience:', error);
        alert('Failed to save experience.');
    }
});

async function editExperience(id) {
    try {
        const response = await apiRequest(`${API_BASE}/experience/${id}`);
        const exp = await response.json();

        document.getElementById('exp-company').value = exp.company;
        document.getElementById('exp-position').value = exp.position;
        document.getElementById('exp-location').value = exp.location || '';
        document.getElementById('exp-start-date').value = exp.start_date ? exp.start_date.split('T')[0] : '';
        document.getElementById('exp-end-date').value = exp.end_date ? exp.end_date.split('T')[0] : '';
        document.getElementById('exp-current').checked = exp.is_current;
        document.getElementById('exp-description').value = exp.description || '';
        document.getElementById('exp-achievements').value = exp.achievements ? exp.achievements.join(', ') : '';

        const form = document.getElementById('experience-form');
        form.dataset.editId = id;
        form.querySelector('button[type="submit"]').textContent = 'Update Experience';
    } catch (error) {
        console.error('Error fetching experience:', error);
    }
}

async function deleteExperience(id) {
    if (!confirm('Are you sure you want to delete this experience?')) return;

    try {
        const response = await apiRequest(`${API_BASE}/experience/${id}`, { method: 'DELETE' });
        if (response.ok) {
            loadExperiences();
            alert('Experience deleted successfully!');
        }
    } catch (error) {
        console.error('Error deleting experience:', error);
        alert('Failed to delete experience.');
    }
}

// ==================== Projects Management ====================
async function loadProjects() {
    try {
        const response = await apiRequest(`${API_BASE}/projects`);
        const projects = await response.json();

        const container = document.getElementById('projects-list');
        container.innerHTML = projects.map(project => `
            <div class="admin-item" data-id="${project.id}">
                <div class="admin-item-content">
                    <h4>${project.title}</h4>
                    <div class="meta">${project.technologies ? project.technologies.join(', ') : ''} ${project.featured ? '⭐ Featured' : ''}</div>
                </div>
                <div class="admin-item-actions">
                    <button class="edit-btn" onclick="editProject(${project.id})">Edit</button>
                    <button class="delete-btn" onclick="deleteProject(${project.id})">Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading projects:', error);
    }
}

document.getElementById('project-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const form = e.target;
    const isEdit = form.dataset.editId;
    const url = isEdit ? `${API_BASE}/projects/${form.dataset.editId}` : `${API_BASE}/projects`;
    const method = isEdit ? 'PUT' : 'POST';

    const projectData = {
        title: document.getElementById('project-title').value,
        description: document.getElementById('project-description').value,
        technologies: document.getElementById('project-technologies').value.split(',').map(s => s.trim()).filter(s => s),
        project_url: document.getElementById('project-url').value,
        github_url: document.getElementById('project-github').value,
        featured: document.getElementById('project-featured').checked
    };

    try {
        const response = await apiRequest(url, { method, body: JSON.stringify(projectData) });
        if (response.ok) {
            form.reset();
            form.dataset.editId = '';
            form.querySelector('button[type="submit"]').textContent = 'Save Project';
            document.getElementById('project-image-preview').innerHTML = '';
            loadProjects();
            alert(isEdit ? 'Project updated successfully!' : 'Project added successfully!');
        }
    } catch (error) {
        console.error('Error saving project:', error);
        alert('Failed to save project.');
    }
});

async function editProject(id) {
    try {
        const response = await apiRequest(`${API_BASE}/projects/${id}`);
        const project = await response.json();

        document.getElementById('project-title').value = project.title;
        document.getElementById('project-description').value = project.description;
        document.getElementById('project-technologies').value = project.technologies ? project.technologies.join(', ') : '';
        document.getElementById('project-url').value = project.project_url || '';
        document.getElementById('project-github').value = project.github_url || '';
        document.getElementById('project-featured').checked = project.featured;

        if (project.image_url) {
            document.getElementById('project-image-preview').innerHTML = `<img src="${project.image_url}" alt="Project">`;
        }

        const form = document.getElementById('project-form');
        form.dataset.editId = id;
        form.querySelector('button[type="submit"]').textContent = 'Update Project';
    } catch (error) {
        console.error('Error fetching project:', error);
    }
}

async function deleteProject(id) {
    if (!confirm('Are you sure you want to delete this project?')) return;

    try {
        const response = await apiRequest(`${API_BASE}/projects/${id}`, { method: 'DELETE' });
        if (response.ok) {
            loadProjects();
            alert('Project deleted successfully!');
        }
    } catch (error) {
        console.error('Error deleting project:', error);
        alert('Failed to delete project.');
    }
}

document.getElementById('project-image').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await apiRequest(`${API_BASE}/upload/image`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (response.ok) {
            document.getElementById('project-image-preview').innerHTML = `<img src="${data.url}" alt="Project">`;

            const form = document.getElementById('project-form');
            const isEdit = form.dataset.editId;
            const url = isEdit ? `${API_BASE}/projects/${form.dataset.editId}` : `${API_BASE}/projects`;
            const method = isEdit ? 'PUT' : 'POST';

            const title = document.getElementById('project-title').value;
            const description = document.getElementById('project-description').value;
            const technologies = document.getElementById('project-technologies').value.split(',').map(s => s.trim()).filter(s => s);
            const project_url = document.getElementById('project-url').value;
            const github_url = document.getElementById('project-github').value;
            const featured = document.getElementById('project-featured').checked;

            await apiRequest(url, {
                method,
                body: JSON.stringify({ title, description, technologies, image_url: data.url, project_url, github_url, featured })
            });

            loadProjects();
            alert('Project image uploaded successfully!');
        }
    } catch (error) {
        console.error('Error uploading project image:', error);
        alert('Failed to upload image.');
    }
});

// ==================== Contacts Management ====================
async function loadContacts() {
    try {
        const response = await apiRequest(`${API_BASE}/contact`);
        const contacts = await response.json();

        const container = document.getElementById('contacts-list');
        container.innerHTML = contacts.map(contact => `
            <div class="admin-item" data-id="${contact.id}">
                <div class="admin-item-content">
                    <h4>${contact.subject}</h4>
                    <div class="meta">
                        From: ${contact.name} (${contact.email}) • 
                        ${new Date(contact.created_at).toLocaleString()} • 
                        ${contact.is_read ? '✅ Read' : '📩 Unread'}
                    </div>
                    <p style="margin-top:8px;color:var(--body-text-muted);">${contact.message}</p>
                </div>
                <div class="admin-item-actions">
                    ${!contact.is_read ? `<button class="edit-btn" onclick="markContactRead(${contact.id})">Mark Read</button>` : ''}
                    <button class="delete-btn" onclick="deleteContact(${contact.id})">Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading contacts:', error);
    }
}

async function markContactRead(id) {
    try {
        const response = await apiRequest(`${API_BASE}/contact/${id}/read`, { method: 'PUT' });
        if (response.ok) {
            loadContacts();
            alert('Contact marked as read.');
        }
    } catch (error) {
        console.error('Error marking contact as read:', error);
    }
}

async function deleteContact(id) {
    if (!confirm('Are you sure you want to delete this message?')) return;

    try {
        const response = await apiRequest(`${API_BASE}/contact/${id}`, { method: 'DELETE' });
        if (response.ok) {
            loadContacts();
            alert('Message deleted successfully!');
        }
    } catch (error) {
        console.error('Error deleting contact:', error);
        alert('Failed to delete message.');
    }
}

// ==================== Logout ====================
document.getElementById('logout-btn').addEventListener('click', () => {
    localStorage.removeItem('access_token');
    window.location.href = '/login';
});

// ==================== Init ====================
document.addEventListener('DOMContentLoaded', () => {
    loadProfile();
    loadSkills();
    loadExperiences();
    loadProjects();
    loadContacts();

    document.getElementById('exp-start-date').value = new Date().toISOString().split('T')[0];
});