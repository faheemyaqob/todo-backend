/**
 * Todo Management Handler
 * Handles CRUD operations for todos
 */

const API_BASE = '/todos';
let allTodos = [];

document.addEventListener('DOMContentLoaded', () => {
    // Change body class for styling
    document.body.classList.add('dashboard-page');
    
    // Check authentication
    checkAuthentication();
    
    // Display username
    const username = localStorage.getItem('username');
    if (username) {
        document.getElementById('userName').textContent = username;
    }
    
    // Load todos
    loadTodos();
    
    // Add event listener to form
    const addTodoForm = document.getElementById('addTodoForm');
    if (addTodoForm) {
        addTodoForm.addEventListener('submit', handleAddTodo);
    }
});

/**
 * Check if user is authenticated
 */
function checkAuthentication() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        redirectToLogin();
    }
}

/**
 * Load all todos from API
 */
async function loadTodos() {
    const todosList = document.getElementById('todosList');
    const emptyState = document.getElementById('emptyState');
    
    try {
        const headers = getAuthHeaders();
        if (!headers) return;
        
        console.log('Loading todos with headers:', headers);
        const response = await fetch(API_BASE, { headers });
        console.log('Response status:', response.status);
        
        if (response.status === 401) {
            console.log('Unauthorized, redirecting to login');
            redirectToLogin();
            return;
        }
        
        if (!response.ok) {
            throw new Error(`Failed to load todos: ${response.statusText}`);
        }
        
        allTodos = await response.json();
        console.log('Loaded todos:', allTodos);
        
        if (allTodos.length === 0) {
            console.log('No todos found');
            todosList.style.display = 'none';
            emptyState.style.display = 'block';
        } else {
            console.log('Rendering ' + allTodos.length + ' todos');
            renderTodos();
            emptyState.style.display = 'none';
            todosList.style.display = 'block';
        }
        
    } catch (error) {
        console.error('Error loading todos:', error);
        showStatus('Failed to load todos: ' + error.message, 'error');
        todosList.innerHTML = `
            <div class="error-message">
                Failed to load todos. Please try again.
            </div>
        `;
    }
}

/**
 * Render todos to the DOM
 */
function renderTodos() {
    const todosList = document.getElementById('todosList');
    const emptyState = document.getElementById('emptyState');
    console.log('renderTodos called with:', allTodos);
    
    if (allTodos.length === 0) {
        console.log('No todos, showing empty state');
        todosList.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }
    
    const html = allTodos.map(todo => `
        <div class="todo-item ${todo.completed ? 'completed' : ''}">
            <input 
                type="checkbox" 
                class="todo-checkbox" 
                ${todo.completed ? 'checked' : ''}
                onchange="toggleTodo(${todo.id}, this.checked)"
            >
            <div class="todo-content">
                <p class="todo-title">${escapeHtml(todo.title)}</p>
                ${todo.description ? `<p class="todo-description">${escapeHtml(todo.description)}</p>` : ''}
                <p class="todo-meta">Created: ${formatDate(todo.created_at)}</p>
            </div>
            <div class="todo-actions">
                <button class="btn btn-delete btn-sm" onclick="deleteTodo(${todo.id})">
                    🗑️ Delete
                </button>
            </div>
        </div>
    `).join('');
    
    console.log('Setting innerHTML to:', html);
    todosList.innerHTML = html;
    todosList.style.display = 'block';
    emptyState.style.display = 'none';
}

/**
 * Handle add todo form submission
 */
async function handleAddTodo(e) {
    e.preventDefault();
    
    const title = document.getElementById('todoTitle').value.trim();
    const description = document.getElementById('todoDescription').value.trim();
    
    if (!title) {
        showStatus('Please enter a todo title', 'error');
        return;
    }
    
    try {
        const headers = getAuthHeaders();
        if (!headers) return;
        
        const submitBtn = e.target.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = '⏳ Adding...';
        
        const response = await fetch(API_BASE, {
            method: 'POST',
            headers,
            body: JSON.stringify({
                title,
                description: description || null,
                completed: false
            })
        });
        
        if (response.status === 401) {
            redirectToLogin();
            return;
        }
        
        if (!response.ok) {
            throw new Error(`Failed to add todo: ${response.statusText}`);
        }
        
        const newTodo = await response.json();
        allTodos.unshift(newTodo);
        
        // Clear form
        document.getElementById('todoTitle').value = '';
        document.getElementById('todoDescription').value = '';
        
        // Update UI - use renderTodos to maintain consistency
        renderTodos();
        
        showStatus('✅ Todo added successfully!', 'success');
        
    } catch (error) {
        console.error('Error adding todo:', error);
        showStatus('Failed to add todo: ' + error.message, 'error');
    } finally {
        const submitBtn = e.target.querySelector('button[type="submit"]');
        submitBtn.disabled = false;
        submitBtn.textContent = '➕ Add Todo';
    }
}

/**
 * Toggle todo completion status
 */
async function toggleTodo(id, completed) {
    const todo = allTodos.find(t => t.id === id);
    if (!todo) return;
    
    try {
        const headers = getAuthHeaders();
        if (!headers) return;
        
        const response = await fetch(`${API_BASE}/${id}`, {
            method: 'PUT',
            headers,
            body: JSON.stringify({
                title: todo.title,
                description: todo.description,
                completed
            })
        });
        
        if (response.status === 401) {
            redirectToLogin();
            return;
        }
        
        if (!response.ok) {
            throw new Error(`Failed to update todo: ${response.statusText}`);
        }
        
        // Update in memory
        todo.completed = completed;
        renderTodos();
        
    } catch (error) {
        console.error('Error toggling todo:', error);
        showStatus('Failed to update todo: ' + error.message, 'error');
        // Reload todos to sync state
        loadTodos();
    }
}

/**
 * Delete a todo
 */
async function deleteTodo(id) {
    if (!confirm('Are you sure you want to delete this todo?')) {
        return;
    }
    
    try {
        const headers = getAuthHeaders();
        if (!headers) return;
        
        const response = await fetch(`${API_BASE}/${id}`, {
            method: 'DELETE',
            headers
        });
        
        if (response.status === 401) {
            redirectToLogin();
            return;
        }
        
        if (!response.ok) {
            throw new Error(`Failed to delete todo: ${response.statusText}`);
        }
        
        // Remove from memory
        allTodos = allTodos.filter(t => t.id !== id);
        
        // Update UI
        if (allTodos.length === 0) {
            document.getElementById('todosList').style.display = 'none';
            document.getElementById('emptyState').style.display = 'block';
        } else {
            renderTodos();
        }
        
        showStatus('✅ Todo deleted successfully!', 'success');
        
    } catch (error) {
        console.error('Error deleting todo:', error);
        showStatus('Failed to delete todo: ' + error.message, 'error');
    }
}

/**
 * Show statistics (placeholder)
 */
function showStats() {
    const total = allTodos.length;
    const completed = allTodos.filter(t => t.completed).length;
    const pending = total - completed;
    
    alert(`📊 Statistics\n\nTotal: ${total}\nCompleted: ${completed}\nPending: ${pending}`);
}

/**
 * Show status message
 */
function showStatus(message, type = 'success') {
    const statusElement = document.getElementById('statusMessage');
    if (!statusElement) return;
    
    statusElement.textContent = message;
    statusElement.className = `status-message ${type}`;
    statusElement.style.display = 'block';
    
    // Auto-hide after 3 seconds
    setTimeout(() => {
        statusElement.style.display = 'none';
    }, 3000);
}

/**
 * Get authorization headers
 */
function getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        redirectToLogin();
        return null;
    }
    
    return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };
}

/**
 * Redirect to login
 */
function redirectToLogin() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('username');
    window.location.href = '/';
}

/**
 * Format date for display
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

/**
 * Escape HTML special characters
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * Logout user
 */
function logout() {
    if (confirm('Are you sure you want to logout?')) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('username');
        window.location.href = '/';
    }
}
