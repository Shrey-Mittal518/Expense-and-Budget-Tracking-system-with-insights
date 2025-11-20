// Main JavaScript for AdvancedExpenseTrackerPro

// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('[role="alert"]');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.transition = 'opacity 0.5s';
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 500);
        }, 5000);
    });

    // Set today's date as default for date inputs
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        if (!input.value) {
            input.value = new Date().toISOString().split('T')[0];
        }
    });
});

// Form validation helpers
function validateAmount(amount) {
    return !isNaN(amount) && parseFloat(amount) !== 0;
}

function validateDate(dateString) {
    const date = new Date(dateString);
    return date instanceof Date && !isNaN(date);
}

// Modal helpers
function closeModalOnOutsideClick(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.classList.add('hidden');
            }
        });
    }
}

// Initialize modal outside click handlers
document.addEventListener('DOMContentLoaded', function() {
    ['addModal', 'importModal', 'backupModal'].forEach(closeModalOnOutsideClick);
});

// Number formatting
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

// Chart helpers for forecast visualization
function createSparkline(data, containerId) {
    const container = document.getElementById(containerId);
    if (!container || !data || data.length === 0) return;

    const max = Math.max(...data);
    const min = Math.min(...data);
    const range = max - min;

    data.forEach((value, index) => {
        const bar = document.createElement('div');
        const height = range > 0 ? ((value - min) / range) * 100 : 50;
        bar.style.height = `${height}%`;
        bar.className = 'flex-1 bg-indigo-400 rounded-t hover:bg-indigo-600 transition-colors';
        bar.title = `Day ${index + 1}: ${formatCurrency(value)}`;
        container.appendChild(bar);
    });
}
