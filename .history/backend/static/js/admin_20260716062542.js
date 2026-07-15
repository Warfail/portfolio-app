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

async function loadExperiences() {
    try {
        const response = await apiRequest(`${API_BASE}/experience`);
        const experiences = await response.json();
        
        const container = document.getElementById('experience-list');
        if (experiences.length === 0) {
            container.innerHTML = '<p style="color: var(--body-text-muted);">No experiences added yet. Add your first experience above!</p>';
            return;
        }
        
        container.innerHTML = experiences.map(exp => `
            <div class="admin-item" data-id="${exp.id}">
                <div class="admin-item-content" style="display:flex;align-items:center;gap:16px;">
                    ${exp.image_url ? 
                        `<img src="${exp.image_url}" style="width:50px;height:50px;object-fit:cover;border-radius:8px;" />` :
                        `<div style="width:50px;height:50px;border-radius:8px;background:#f0f0f0;display:flex;align-items:center;justify-content:center;font-size:20px;color:#999;"><i class="fas fa-building"></i></div>`
                    }
                    <div>
                        <h4>${exp.position} at ${exp.company}</h4>
                        <div class="meta">${new Date(exp.start_date).toLocaleDateString()} - ${exp.is_current ? 'Present' : new Date(exp.end_date).toLocaleDateString()}</div>
                    </div>
                </div>
                <div class="admin-item-actions">
                    <button class="edit-btn" onclick="editExperience(${exp.id})">✏️ Edit</button>
                    <button class="delete-btn" onclick="deleteExperience(${exp.id})">🗑️ Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading experiences:', error);
    }
}

// ==================== SKILLS MANAGEMENT ====================
async function loadSkills() {
    try {
        const response = await apiRequest(`${API_BASE}/skills`);
        const skills = await response.json();
        
        const container = document.getElementById('skills-list');
        if (skills.length === 0) {
            container.innerHTML = '<p style="color: var(--body-text-muted);">No skills added yet. Add your first skill above!</p>';
            return;
        }
        
        container.innerHTML = skills.map(skill => `
            <div class="admin-item" data-id="${skill.id}">
                <div class="admin-item-content">
                    <h4>${skill.name}</h4>
                    <div class="meta">${skill.category} ${skill.level ? `• ${skill.level}%` : ''}</div>
                </div>
                <div class="admin-item-actions">
                    <button class="edit-btn" onclick="editSkill(${skill.id})">✏️ Edit</button>
                    <button class="delete-btn" onclick="deleteSkill(${skill.id})">🗑️ Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading skills:', error);
    }
}

async function editSkill(id) {
    try {
        const response = await apiRequest(`${API_BASE}/skills/${id}`);
        const skill = await response.json();
        
        document.getElementById('skill-name').value = skill.name;
        document.getElementById('skill-category').value = skill.category;
        document.getElementById('skill-level').value = skill.level || '';
        document.getElementById('skill-edit-id').value = id;
        
        document.getElementById('skill-submit-btn').textContent = 'Update Skill';
        document.getElementById('skill-cancel-btn').style.display = 'inline-block';
        
        document.getElementById('skill-form').scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        console.error('Error fetching skill:', error);
        alert('Failed to load skill data.');
    }
}

function cancelSkillEdit() {
    document.getElementById('skill-form').reset();
    document.getElementById('skill-edit-id').value = '';
    document.getElementById('skill-submit-btn').textContent = 'Add Skill';
    document.getElementById('skill-cancel-btn').style.display = 'none';
}

// Experience image upload with better preview
document.getElementById('exp-image').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Show preview immediately
    const reader = new FileReader();
    reader.onload = function(event) {
        document.getElementById('exp-image-preview').innerHTML = `
            <div style="position:relative;display:inline-block;">
                <img src="${event.target.result}" alt="Experience Photo" style="max-width:200px;border-radius:8px;border:2px solid var(--teal-primary);">
                <button type="button" onclick="removeExpImage()" style="position:absolute;top:-8px;right:-8px;background:#dc3545;color:white;border:none;border-radius:50%;width:24px;height:24px;cursor:pointer;font-size:14px;line-height:24px;text-align:center;">×</button>
            </div>
        `;
    };
    reader.readAsDataURL(file);

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await apiRequest(`${API_BASE}/upload/image`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (response.ok) {
            const imageUrl = data.url;
            document.getElementById('exp-image-preview').dataset.imageUrl = imageUrl;
            
            // If in edit mode, update the experience
            const editId = document.getElementById('exp-edit-id').value;
            if (editId) {
                const expData = {
                    company: document.getElementById('exp-company').value,
                    position: document.getElementById('exp-position').value,
                    location: document.getElementById('exp-location').value,
                    start_date: document.getElementById('exp-start-date').value,
                    end_date: document.getElementById('exp-end-date').value || null,
                    is_current: document.getElementById('exp-current').checked,
                    description: document.getElementById('exp-description').value,
                    achievements: document.getElementById('exp-achievements').value.split(',').map(s => s.trim()).filter(s => s),
                    image_url: imageUrl
                };

                const response2 = await apiRequest(`${API_BASE}/experience/${editId}`, {
                    method: 'PUT',
                    body: JSON.stringify(expData)
                });

                if (response2.ok) {
                    loadExperiences();
                    alert('Photo uploaded successfully!');
                }
            }
        }
    } catch (error) {
        console.error('Error uploading photo:', error);
        alert('Failed to upload photo.');
    }
});

// Remove experience photo
async function removeExpImage() {
    const preview = document.getElementById('exp-image-preview');
    const img = preview.querySelector('img');
    if (img) {
        const publicId = img.src.split('/').pop().split('.')[0];
        try {
            await apiRequest(`${API_BASE}/upload/image/${publicId}`, { method: 'DELETE' });
        } catch (error) {
            console.error('Error deleting image:', error);
        }
    }
    
    preview.innerHTML = '';
    delete preview.dataset.imageUrl;
    
    const editId = document.getElementById('exp-edit-id').value;
    if (editId) {
        const expData = {
            company: document.getElementById('exp-company').value,
            position: document.getElementById('exp-position').value,
            location: document.getElementById('exp-location').value,
            start_date: document.getElementById('exp-start-date').value,
            end_date: document.getElementById('exp-end-date').value || null,
            is_current: document.getElementById('exp-current').checked,
            description: document.getElementById('exp-description').value,
            achievements: document.getElementById('exp-achievements').value.split(',').map(s => s.trim()).filter(s => s),
            image_url: ''
        };

        await apiRequest(`${API_BASE}/experience/${editId}`, {
            method: 'PUT',
            body: JSON.stringify(expData)
        });
        loadExperiences();
        alert('Photo removed successfully!');
    }
}

// Update editExperience to show photos
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
        document.getElementById('exp-edit-id').value = id;
        
        if (exp.image_url) {
            document.getElementById('exp-image-preview').innerHTML = `
                <div style="position:relative;display:inline-block;">
                    <img src="${exp.image_url}" alt="Experience Photo" style="max-width:200px;border-radius:8px;border:2px solid var(--teal-primary);">
                    <button type="button" onclick="removeExpImage()" style="position:absolute;top:-8px;right:-8px;background:#dc3545;color:white;border:none;border-radius:50%;width:24px;height:24px;cursor:pointer;font-size:14px;line-height:24px;text-align:center;">×</button>
                </div>
            `;
            document.getElementById('exp-image-preview').dataset.imageUrl = exp.image_url;
        } else {
            document.getElementById('exp-image-preview').innerHTML = '';
        }
        
        document.getElementById('exp-submit-btn').textContent = 'Update Experience';
        document.getElementById('exp-cancel-btn').style.display = 'inline-block';
        
        document.getElementById('experience-form').scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        console.error('Error fetching experience:', error);
        alert('Failed to load experience data.');
    }
}
function cancelExperienceEdit() {
    document.getElementById('experience-form').reset();
    document.getElementById('exp-edit-id').value = '';
    document.getElementById('exp-submit-btn').textContent = 'Save Experience';
    document.getElementById('exp-cancel-btn').style.display = 'none';
    document.getElementById('exp-image-preview').innerHTML = '';
}

// Experience image upload
document.getElementById('exp-image').addEventListener('change', async (e) => {
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
            const imageUrl = data.url;
            document.getElementById('exp-image-preview').innerHTML = `
                <img src="${imageUrl}" alt="Company Logo" style="max-width:150px;border-radius:8px;">
                <button type="button" onclick="removeExpImage()" class="btn btn-secondary" style="margin-top:8px;padding:4px 12px;font-size:12px;">Remove Image</button>
            `;
            
            // Store the image URL in a hidden field or data attribute
            document.getElementById('exp-image-preview').dataset.imageUrl = imageUrl;
            
            // If in edit mode, update the experience with the image URL
            const editId = document.getElementById('exp-edit-id').value;
            if (editId) {
                const expData = {
                    company: document.getElementById('exp-company').value,
                    position: document.getElementById('exp-position').value,
                    location: document.getElementById('exp-location').value,
                    start_date: document.getElementById('exp-start-date').value,
                    end_date: document.getElementById('exp-end-date').value || null,
                    is_current: document.getElementById('exp-current').checked,
                    description: document.getElementById('exp-description').value,
                    achievements: document.getElementById('exp-achievements').value.split(',').map(s => s.trim()).filter(s => s),
                    image_url: imageUrl
                };

                const response2 = await apiRequest(`${API_BASE}/experience/${editId}`, {
                    method: 'PUT',
                    body: JSON.stringify(expData)
                });

                if (response2.ok) {
                    loadExperiences();
                    alert('Company image uploaded successfully!');
                }
            }
        }
    } catch (error) {
        console.error('Error uploading image:', error);
        alert('Failed to upload image.');
    }
});

// Remove experience image
async function removeExpImage() {
    const preview = document.getElementById('exp-image-preview');
    const img = preview.querySelector('img');
    if (img) {
        const publicId = img.src.split('/').pop().split('.')[0];
        try {
            await apiRequest(`${API_BASE}/upload/image/${publicId}`, { method: 'DELETE' });
        } catch (error) {
            console.error('Error deleting image:', error);
        }
    }
    
    preview.innerHTML = '';
    delete preview.dataset.imageUrl;
    
    const editId = document.getElementById('exp-edit-id').value;
    if (editId) {
        const expData = {
            company: document.getElementById('exp-company').value,
            position: document.getElementById('exp-position').value,
            location: document.getElementById('exp-location').value,
            start_date: document.getElementById('exp-start-date').value,
            end_date: document.getElementById('exp-end-date').value || null,
            is_current: document.getElementById('exp-current').checked,
            description: document.getElementById('exp-description').value,
            achievements: document.getElementById('exp-achievements').value.split(',').map(s => s.trim()).filter(s => s),
            image_url: ''
        };

        await apiRequest(`${API_BASE}/experience/${editId}`, {
            method: 'PUT',
            body: JSON.stringify(expData)
        });
        loadExperiences();
        alert('Image removed successfully!');
    }
}

// Update experience form submission
document.getElementById('experience-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const editId = document.getElementById('exp-edit-id').value;
    const imageUrl = document.getElementById('exp-image-preview').dataset.imageUrl || '';
    const expData = {
        company: document.getElementById('exp-company').value,
        position: document.getElementById('exp-position').value,
        location: document.getElementById('exp-location').value,
        start_date: document.getElementById('exp-start-date').value,
        end_date: document.getElementById('exp-end-date').value || null,
        is_current: document.getElementById('exp-current').checked,
        description: document.getElementById('exp-description').value,
        achievements: document.getElementById('exp-achievements').value.split(',').map(s => s.trim()).filter(s => s),
        image_url: imageUrl
    };
    
    try {
        const url = editId ? `${API_BASE}/experience/${editId}` : `${API_BASE}/experience`;
        const method = editId ? 'PUT' : 'POST';
        
        const response = await apiRequest(url, {
            method,
            body: JSON.stringify(expData)
        });
        
        if (response.ok) {
            document.getElementById('experience-form').reset();
            document.getElementById('exp-edit-id').value = '';
            document.getElementById('exp-submit-btn').textContent = 'Save Experience';
            document.getElementById('exp-cancel-btn').style.display = 'none';
            document.getElementById('exp-image-preview').innerHTML = '';
            loadExperiences();
            alert(editId ? 'Experience updated successfully!' : 'Experience added successfully!');
        }
    } catch (error) {
        console.error('Error saving experience:', error);
        alert('Failed to save experience.');
    }
});

document.getElementById('exp-cancel-btn').addEventListener('click', cancelExperienceEdit);

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

// ==================== PROJECTS MANAGEMENT ====================
async function loadProjects() {
    try {
        const response = await apiRequest(`${API_BASE}/projects`);
        const projects = await response.json();
        
        const container = document.getElementById('projects-list');
        if (projects.length === 0) {
            container.innerHTML = '<p style="color: var(--body-text-muted);">No projects added yet. Add your first project above!</p>';
            return;
        }
        
        container.innerHTML = projects.map(project => `
            <div class="admin-item" data-id="${project.id}">
                <div class="admin-item-content">
                    <h4>${project.title}</h4>
                    <div class="meta">${project.technologies ? project.technologies.join(', ') : ''} ${project.featured ? '⭐ Featured' : ''}</div>
                    ${project.image_url ? `<img src="${project.image_url}" style="max-width:100px;margin-top:8px;border-radius:4px;" />` : ''}
                </div>
                <div class="admin-item-actions">
                    <button class="edit-btn" onclick="editProject(${project.id})">✏️ Edit</button>
                    <button class="delete-btn" onclick="deleteProject(${project.id})">🗑️ Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading projects:', error);
    }
}

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
        document.getElementById('project-edit-id').value = id;
        
        if (project.image_url) {
            document.getElementById('project-image-preview').innerHTML = `
                <img src="${project.image_url}" alt="Project" style="max-width:200px;border-radius:8px;">
            `;
        }
        
        document.getElementById('project-submit-btn').textContent = 'Update Project';
        document.getElementById('project-cancel-btn').style.display = 'inline-block';
        
        document.getElementById('project-form').scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        console.error('Error fetching project:', error);
        alert('Failed to load project data.');
    }
}

function cancelProjectEdit() {
    document.getElementById('project-form').reset();
    document.getElementById('project-edit-id').value = '';
    document.getElementById('project-submit-btn').textContent = 'Save Project';
    document.getElementById('project-cancel-btn').style.display = 'none';
    document.getElementById('project-image-preview').innerHTML = '';
}

document.getElementById('project-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const editId = document.getElementById('project-edit-id').value;
    const projectData = {
        title: document.getElementById('project-title').value,
        description: document.getElementById('project-description').value,
        technologies: document.getElementById('project-technologies').value.split(',').map(s => s.trim()).filter(s => s),
        project_url: document.getElementById('project-url').value,
        github_url: document.getElementById('project-github').value,
        featured: document.getElementById('project-featured').checked
    };
    
    try {
        const url = editId ? `${API_BASE}/projects/${editId}` : `${API_BASE}/projects`;
        const method = editId ? 'PUT' : 'POST';
        
        const response = await apiRequest(url, {
            method,
            body: JSON.stringify(projectData)
        });
        
        if (response.ok) {
            document.getElementById('project-form').reset();
            document.getElementById('project-edit-id').value = '';
            document.getElementById('project-submit-btn').textContent = 'Save Project';
            document.getElementById('project-cancel-btn').style.display = 'none';
            document.getElementById('project-image-preview').innerHTML = '';
            loadProjects();
            alert(editId ? 'Project updated successfully!' : 'Project added successfully!');
        }
    } catch (error) {
        console.error('Error saving project:', error);
        alert('Failed to save project.');
    }
});

document.getElementById('project-cancel-btn').addEventListener('click', cancelProjectEdit);

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
            // Save image URL temporarily
            const imageUrl = data.url;
            document.getElementById('project-image-preview').innerHTML = `
                <img src="${imageUrl}" alt="Project" style="max-width:200px;border-radius:8px;">
            `;
            
            // Update the project with the image URL
            const editId = document.getElementById('project-edit-id').value;
            const url = editId ? `${API_BASE}/projects/${editId}` : `${API_BASE}/projects`;
            const method = editId ? 'PUT' : 'POST';
            
            const title = document.getElementById('project-title').value;
            const description = document.getElementById('project-description').value;
            const technologies = document.getElementById('project-technologies').value.split(',').map(s => s.trim()).filter(s => s);
            const project_url = document.getElementById('project-url').value;
            const github_url = document.getElementById('project-github').value;
            const featured = document.getElementById('project-featured').checked;

            const response2 = await apiRequest(url, {
                method,
                body: JSON.stringify({ title, description, technologies, image_url: imageUrl, project_url, github_url, featured })
            });

            if (response2.ok) {
                loadProjects();
                alert('Project image uploaded successfully!');
            }
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
        if (contacts.length === 0) {
            container.innerHTML = '<p style="color: var(--body-text-muted);">No messages yet.</p>';
            return;
        }

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