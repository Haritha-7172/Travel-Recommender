document.addEventListener('DOMContentLoaded', function() {
    
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    
    const animateOnScroll = function() {
        const cards = document.querySelectorAll('.card');
        
        cards.forEach(card => {
            const cardPosition = card.getBoundingClientRect().top;
            const screenPosition = window.innerHeight;
            
            if (cardPosition < screenPosition) {
                card.classList.add('animate__animated', 'animate__fadeInUp');
            }
        });
    };
    
    
    window.addEventListener('scroll', animateOnScroll);
    
    
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const alertInstance = new bootstrap.Alert(alert);
            alertInstance.close();
        }, 5000);
    });
    
    
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarMenu = document.querySelector('#navbarNav');
    
    if (navbarToggler && navbarMenu) {
        document.addEventListener('click', function(event) {
            const isNavbarToggler = navbarToggler.contains(event.target);
            const isNavbarMenu = navbarMenu.contains(event.target);
            
            if (!isNavbarToggler && !isNavbarMenu && navbarMenu.classList.contains('show')) {
                navbarToggler.click();
            }
        });
    }
});
