// ============================================
// BB84 Adaptive QKD - Frontend JavaScript
// ============================================

// ============================================
// Modal Management Functions
// ============================================

/**
 * Show loading modal
 */
function showLoading() {
    const modal = document.getElementById('loadingModal');
    modal.classList.add('active');
}

/**
 * Hide loading modal
 */
function hideLoading() {
    const modal = document.getElementById('loadingModal');
    modal.classList.remove('active');
}

/**
 * Show results modal with output
 */
function showResults(title, output, color) {
    const modal = document.getElementById('resultsModal');
    const titleEl = document.getElementById('resultsTitle');
    const outputEl = document.getElementById('resultsOutput');
    const colorIndicator = document.getElementById('colorIndicator');
    
    titleEl.textContent = title;
    outputEl.textContent = output;
    colorIndicator.style.backgroundColor = color;
    
    modal.classList.add('active');
}

/**
 * Close results modal
 */
function closeResults() {
    const modal = document.getElementById('resultsModal');
    modal.classList.remove('active');
}

// ============================================
// Experiment Execution
// ============================================

/**
 * Run an experiment and display results
 * @param {string} expId - Experiment ID
 * @param {string} expName - Experiment name
 * @param {string} expColor - Experiment color code
 */
async function runExperiment(expId, expName, expColor) {
    try {
        showLoading();
        
        // Make API request to run experiment
        const response = await fetch(`/api/run/${expId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        hideLoading();
        
        if (data.success) {
            // Display results
            showResults(expName, data.output, expColor);
        } else {
            showResults(
                expName,
                `Error: ${data.error || 'Unknown error occurred'}`,
                '#FF6B6B'
            );
        }
    } catch (error) {
        hideLoading();
        showResults(
            expName,
            `Error: ${error.message}\n\nPlease check the console for more details.`,
            '#FF6B6B'
        );
        console.error('Experiment execution error:', error);
    }
}

// ============================================
// Event Listeners
// ============================================

/**
 * Close modal when clicking outside of it
 */
document.addEventListener('DOMContentLoaded', function() {
    const resultsModal = document.getElementById('resultsModal');
    
    if (resultsModal) {
        resultsModal.addEventListener('click', function(event) {
            // Close if clicking on the modal background (not content)
            if (event.target === resultsModal) {
                closeResults();
            }
        });
    }
    
    const loadingModal = document.getElementById('loadingModal');
    
    if (loadingModal) {
        loadingModal.addEventListener('click', function(event) {
            // Prevent closing loading modal by clicking background
            if (event.target === loadingModal) {
                event.preventDefault();
            }
        });
    }
});

// ============================================
// Utility Functions
// ============================================

/**
 * Copy text to clipboard
 */
function copyToClipboard() {
    const outputEl = document.getElementById('resultsOutput');
    const text = outputEl.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        alert('Results copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

/**
 * Download results as text file
 */
function downloadResults() {
    const titleEl = document.getElementById('resultsTitle');
    const outputEl = document.getElementById('resultsOutput');
    
    const filename = `${titleEl.textContent.replace(/\s+/g, '_')}_results.txt`;
    const text = outputEl.textContent;
    
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);
    
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

/**
 * Smooth scroll to section
 */
function smoothScroll(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// ============================================
// Keyboard Shortcuts
// ============================================

/**
 * Handle keyboard shortcuts
 */
document.addEventListener('keydown', function(event) {
    // Press Escape to close modals
    if (event.key === 'Escape') {
        closeResults();
    }
});

// ============================================
// Animation Enhancements
// ============================================

/**
 * Add animation to cards on scroll
 */
function observeCards() {
    const cards = document.querySelectorAll('.experiment-card, .stat-card, .doc-item');
    
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = 'fadeIn 0.5s ease-in';
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        
        cards.forEach(card => observer.observe(card));
    }
}

// ============================================
// Initialize on Page Load
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    observeCards();
    console.log('BB84 QKD Web Interface Loaded');
});

// ============================================
// API Helper Functions
// ============================================

/**
 * Get all experiments metadata
 */
async function getExperiments() {
    try {
        const response = await fetch('/api/experiments');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch experiments:', error);
        return null;
    }
}

/**
 * Get single experiment details
 */
async function getExperimentDetails(expId) {
    try {
        const response = await fetch(`/api/experiment/${expId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch experiment details:', error);
        return null;
    }
}

// ============================================
// Search and Filter
// ============================================

/**
 * Filter experiments by search term
 */
function searchExperiments(query) {
    const cards = document.querySelectorAll('.experiment-card');
    query = query.toLowerCase();
    
    cards.forEach(card => {
        const title = card.querySelector('.card-title').textContent.toLowerCase();
        const description = card.querySelector('.card-description').textContent.toLowerCase();
        
        if (title.includes(query) || description.includes(query)) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
}

// ============================================
// Real-time Status Updates
// ============================================

/**
 * Update experiment status message
 */
function updateStatus(message) {
    const statusEl = document.querySelector('.status-message');
    if (statusEl) {
        statusEl.textContent = message;
    }
}

// ============================================
// Performance Monitoring
// ============================================

/**
 * Log page load time
 */
window.addEventListener('load', function() {
    const perfData = window.performance.timing;
    const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
    console.log(`Page load time: ${pageLoadTime}ms`);
});
