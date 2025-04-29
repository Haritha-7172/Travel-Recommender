document.addEventListener('DOMContentLoaded', function() {
  
    const searchForm = document.getElementById('search-form');
    
    if (searchForm) {
        
        searchForm.addEventListener('submit', function(event) {
            
            const budgetInput = document.getElementById('budget');
            if (budgetInput && budgetInput.value) {
                const budget = parseFloat(budgetInput.value);
                if (isNaN(budget) || budget < 0) {
                    event.preventDefault();
                    alert('Please enter a valid budget amount.');
                    budgetInput.focus();
                    return;
                }
            }
            
            
            const daysInput = document.getElementById('days');
            if (daysInput && daysInput.value) {
                const days = parseInt(daysInput.value);
                if (isNaN(days) || days <= 0) {
                    event.preventDefault();
                    alert('Please enter a valid number of days.');
                    daysInput.focus();
                    return;
                }
            }
            
            
            if (!event.defaultPrevented) {
                const submitButton = searchForm.querySelector('button[type="submit"]');
                if (submitButton) {
                    
                    const originalText = submitButton.innerHTML;
                    
                    
                    submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Searching...';
                    submitButton.disabled = true;
                    
                    
                    setTimeout(() => {
                        if (submitButton.disabled) {
                            submitButton.innerHTML = originalText;
                            submitButton.disabled = false;
                        }
                    }, 10000);
                }
            }
        });
    }
    
    
    const budgetInput = document.getElementById('budget');
    if (budgetInput) {
        budgetInput.min = 0;
        budgetInput.addEventListener('input', function() {
            if (parseFloat(this.value) < 0) {
                this.value = 0;
            }
        });
    }
    
    const daysInput = document.getElementById('days');
    if (daysInput) {
        daysInput.min = 1;
        daysInput.addEventListener('input', function() {
            if (parseInt(this.value) < 1) {
                this.value = 1;
            }
        });
    }
});
