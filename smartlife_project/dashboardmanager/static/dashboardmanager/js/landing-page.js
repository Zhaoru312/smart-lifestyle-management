/**
 * Landing Page Management - Custom JavaScript
 * Handles interactive elements for the landing page management interface
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            trigger: 'hover',
            placement: 'top',
            container: 'body'
        });
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl, {
            trigger: 'focus',
            placement: 'top',
            container: 'body',
            html: true
        });
    });
    
    // Handle form submissions with confirmation
    document.addEventListener('submit', async function(e) {
        const form = e.target;
        
        // Only handle forms with data-confirm attribute
        if (!form.hasAttribute('data-confirm')) {
            return true;
        }
        
        // Prevent default form submission
        e.preventDefault();
        e.stopPropagation();
        
        const confirmMessage = form.getAttribute('data-confirm');
        const formData = new FormData(form);
        
        // Show confirmation dialog
        try {
            const result = await Swal.fire({
                title: 'Are you sure?',
                text: confirmMessage,
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, delete it!',
                cancelButtonText: 'Cancel',
                reverseButtons: true,
                focusCancel: true,
                allowOutsideClick: false,
                allowEscapeKey: false
            });
            
            if (!result.isConfirmed) {
                return false;
            }
            
            // If confirmed, proceed with the form submission
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                },
            });
            
            if (response.redirected) {
                // If the response is a redirect, follow it
                window.location.href = response.url;
                return;
            }
            
            if (response.redirected) {
                // If the response is a redirect, follow it
                window.location.href = response.url;
                return;
            }
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                // Remove the row from the table
                const row = form.closest('tr');
                if (row) {
                    row.style.opacity = '0';
                    setTimeout(() => {
                        row.remove();
                        showAlert(data.message || 'Item deleted successfully!', 'success');
                    }, 300);
                } else {
                    showAlert(data.message || 'Item deleted successfully!', 'success');
                    // Reload the page to reflect changes if the row couldn't be found
                    setTimeout(() => window.location.reload(), 1500);
                }
            } else {
                throw new Error(data.message || 'Failed to delete item');
            }
        } catch (error) {
            console.error('Error:', error);
            showAlert(error.message || 'An error occurred while processing your request.', 'error');
        }
    });
    
    // Toggle active status with loading state
    const toggleButtons = document.querySelectorAll('.toggle-active');
    toggleButtons.forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            
            const url = this.dataset.url;
            const row = this.closest('tr');
            const statusBadge = row.querySelector('.status-badge');
            const isActive = statusBadge.classList.contains('bg-success');
            const buttonIcon = this.querySelector('i');
            const originalHTML = this.innerHTML;
            
            // Show loading state
            this.disabled = true;
            this.innerHTML = '<span class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span> Updating...';
            
            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        is_active: !isActive
                    })
                });
                
                const data = await response.json();
                
                if (response.ok && data.success) {
                    // Update UI
                    if (data.is_active) {
                        statusBadge.className = 'badge status-badge bg-success bg-opacity-10 text-success';
                        statusBadge.innerHTML = '<i class="fas fa-circle me-1 small"></i> Active';
                        this.innerHTML = '<i class="fas fa-toggle-on"></i> Deactivate';
                        this.setAttribute('title', 'Deactivate');
                    } else {
                        statusBadge.className = 'badge status-badge bg-secondary bg-opacity-10 text-secondary';
                        statusBadge.innerHTML = '<i class="fas fa-circle me-1 small"></i> Inactive';
                        this.innerHTML = '<i class="fas fa-toggle-off"></i> Activate';
                        this.setAttribute('title', 'Activate');
                    }
                    
                    // Re-initialize tooltip
                    const tooltip = bootstrap.Tooltip.getInstance(this);
                    if (tooltip) {
                        tooltip.dispose();
                    }
                    new bootstrap.Tooltip(this);
                    
                    showAlert('Status updated successfully!', 'success');
                } else {
                    throw new Error(data.message || 'Failed to update status');
                }
            } catch (error) {
                console.error('Error:', error);
                showAlert(error.message || 'An error occurred while updating the status.', 'error');
            } finally {
                // Reset button state
                this.disabled = false;
            }
        });
    });
    
    // Sortable tables with visual feedback
    const sortableTables = document.querySelectorAll('.sortable-table');
    sortableTables.forEach(table => {
        const tbody = table.querySelector('tbody');
        if (!tbody) return;
        
        new Sortable(tbody, {
            animation: 150,
            handle: '.sort-handle',
            ghostClass: 'sortable-ghost',
            chosenClass: 'sortable-chosen',
            dragClass: 'sortable-drag',
            onStart: function() {
                document.body.style.cursor = 'grabbing';
            },
            onEnd: function() {
                document.body.style.cursor = '';
            },
            onSort: async function(evt) {
                const rows = Array.from(tbody.querySelectorAll('tr'));
                const order = rows.map(row => row.dataset.id);
                const url = table.dataset.sortUrl;
                
                if (!url) {
                    console.error('No sort URL specified for sortable table');
                    return;
                }
                
                // Show loading state
                const loadingRow = document.createElement('tr');
                loadingRow.className = 'sortable-loading';
                loadingRow.innerHTML = `
                    <td colspan="100%" class="text-center py-3">
                        <div class="spinner-border spinner-border-sm text-primary me-2" role="status"></div>
                        <span>Updating order...</span>
                    </td>
                `;
                tbody.appendChild(loadingRow);
                
                try {
                    const response = await fetch(url, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken'),
                            'X-Requested-With': 'XMLHttpRequest',
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ order })
                    });
                    
                    if (!response.ok) {
                        throw new Error('Failed to update order');
                    }
                    
                    const data = await response.json();
                    if (data.success) {
                        showAlert('Order updated successfully!', 'success');
                    } else {
                        throw new Error(data.message || 'Failed to update order');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    showAlert(error.message || 'An error occurred while updating the order.', 'error');
                    
                    // Revert the UI if there's an error
                    if (evt && evt.from && evt.item && evt.oldIndex !== undefined) {
                        evt.from.insertBefore(evt.item, evt.from.children[evt.oldIndex]);
                    }
                } finally {
                    // Remove loading state
                    if (loadingRow && loadingRow.parentNode) {
                        loadingRow.remove();
                    }
                }
            }
        });
    });
});

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Helper function to show alerts
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const container = document.querySelector('.container-fluid.py-4');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const alert = bootstrap.Alert.getOrCreateInstance(alertDiv);
            if (alert) {
                alert.close();
            } else {
                // Fallback in case Bootstrap's Alert is not available
                alertDiv.remove();
            }
        }, 5000);
    }
}

function clearSearch(inputId) {
    const input = document.getElementById(inputId);
    if (!input) return;
    
    input.value = '';
    
    // Trigger the input event to refresh the search
    const event = new Event('input', {
        bubbles: true,
        cancelable: true,
    });
    input.dispatchEvent(event);
}

function printSection(cardId) {
    const card = document.getElementById(cardId);
    if (!card) {
        console.error('Card element not found');
        return;
    }
    
    const printWindow = window.open('', '_blank');
    const cssPath = '/static/dashboardmanager/css/landing-page.css';
    
    printWindow.document.write(`
        <html>
            <head>
                <title>Print</title>
                <link rel="stylesheet" href="${cssPath}">
                <style>
                    @media print {
                        body { padding: 20px; }
                        .no-print { display: none !important; }
                    }
                </style>
            </head>
            <body>
                ${card.innerHTML}
                <script>
                    window.onafterprint = function() {
                        window.close();
                    }
                    // Trigger print after the content is loaded
                    window.onload = function() {
                        setTimeout(function() {
                            window.print();
                        }, 500);
                    }
                </script>
            </body>
        </html>
    `);
    printWindow.document.close();
}

function toggleCard(cardId) {
    const cardBody = document.getElementById(cardId + 'Body');
    const icon = document.getElementById(cardId + 'Icon');
    
    if (cardBody.style.display === 'none') {
        cardBody.style.display = 'block';
        icon.className = 'fas fa-minus';
    } else {
        cardBody.style.display = 'none';
        icon.className = 'fas fa-plus';
    }
}

document.getElementById('heroSearch').addEventListener('input', function() {
    const filter = this.value.toLowerCase();
    const rows = document.querySelectorAll('#heroTable tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(filter) ? '' : 'none';
    });
});

document.getElementById('featuresSearch').addEventListener('input', function() {
    const filter = this.value.toLowerCase();
    const rows = document.querySelectorAll('#featuresTable tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(filter) ? '' : 'none';
    });
});

document.getElementById('testimonialsSearch').addEventListener('input', function() {
    const filter = this.value.toLowerCase();
    const rows = document.querySelectorAll('#testimonialsTable tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(filter) ? '' : 'none';
    });
});

document.getElementById('faqsSearch').addEventListener('input', function() {
    const filter = this.value.toLowerCase();
    const rows = document.querySelectorAll('#faqsTable tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(filter) ? '' : 'none';
    });
});
