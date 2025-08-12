// Django Admin Panel Scroll Pozisiyası Qorunması
document.addEventListener('DOMContentLoaded', function() {
    let scrollPosition = 0;
    let isNavigating = false;
    
    // Scroll pozisiyasını qoruyan funksiya
    function saveScrollPosition() {
        scrollPosition = window.pageYOffset || document.documentElement.scrollTop;
        localStorage.setItem('adminScrollPosition', scrollPosition);
    }
    
    // Scroll pozisiyasını bərpa edən funksiya
    function restoreScrollPosition() {
        const savedPosition = localStorage.getItem('adminScrollPosition');
        if (savedPosition && !isNavigating) {
            setTimeout(() => {
                window.scrollTo(0, parseInt(savedPosition));
            }, 100);
        }
    }
    
    // Link kliklərini izləyən funksiya
    function handleLinkClick(event) {
        const target = event.target.closest('a');
        if (target && !target.target && !target.hasAttribute('download')) {
            // Daxili link-lər üçün scroll pozisiyasını qoruyur
            if (target.href && target.href.includes('/admin/')) {
                isNavigating = true;
                saveScrollPosition();
            }
        }
    }
    
    // Form submit-lərini izləyən funksiya
    function handleFormSubmit(event) {
        if (event.target.tagName === 'FORM') {
            isNavigating = true;
            saveScrollPosition();
        }
    }
    
    // Admin panelində olduğumuzu yoxlayır
    if (window.location.pathname.includes('/admin/')) {
        // Scroll pozisiyasını qoruyur
        window.addEventListener('scroll', saveScrollPosition);
        
        // Link kliklərini izləyir
        document.addEventListener('click', handleLinkClick);
        
        // Form submit-lərini izləyir
        document.addEventListener('submit', handleFormSubmit);
        
        // Səhifə yükləndikdə scroll pozisiyasını bərpa edir
        window.addEventListener('load', restoreScrollPosition);
        
        // DOMContentLoaded-dan sonra scroll pozisiyasını bərpa edir
        setTimeout(restoreScrollPosition, 200);
        
        // Browser back/forward düymələrini izləyir
        window.addEventListener('popstate', function() {
            setTimeout(restoreScrollPosition, 100);
        });
        
        // Admin panelində naviqasiya zamanı scroll pozisiyasını qoruyur
        const adminLinks = document.querySelectorAll('a[href*="/admin/"]');
        adminLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (!this.target && !this.hasAttribute('download')) {
                    isNavigating = true;
                    saveScrollPosition();
                }
            });
        });
        
        // Breadcrumb link-lərini izləyir
        const breadcrumbLinks = document.querySelectorAll('.breadcrumbs a');
        breadcrumbLinks.forEach(link => {
            link.addEventListener('click', function() {
                isNavigating = true;
                saveScrollPosition();
            });
        });
        
        // Pagination link-lərini izləyir
        const paginationLinks = document.querySelectorAll('.paginator a');
        paginationLinks.forEach(link => {
            link.addEventListener('click', function() {
                isNavigating = true;
                saveScrollPosition();
            });
        });
        
        // Filter link-lərini izləyir
        const filterLinks = document.querySelectorAll('.filtered a');
        filterLinks.forEach(link => {
            link.addEventListener('click', function() {
                isNavigating = true;
                saveScrollPosition();
            });
        });
        
        // Action link-lərini izləyir
        const actionLinks = document.querySelectorAll('.actions a');
        actionLinks.forEach(link => {
            link.addEventListener('click', function() {
                isNavigating = true;
                saveScrollPosition();
            });
        });
        
        // Model admin link-lərini izləyir
        const modelLinks = document.querySelectorAll('.model-admin a');
        modelLinks.forEach(link => {
            link.addEventListener('click', function() {
                isNavigating = true;
                saveScrollPosition();
            });
        });
        
        // Səhifə yükləndikdə isNavigating flag-ini false edir
        window.addEventListener('load', function() {
            setTimeout(() => {
                isNavigating = false;
            }, 500);
        });
    }
    
    // Səhifə tərk edilərkən scroll pozisiyasını təmizləyir
    window.addEventListener('beforeunload', function() {
        if (isNavigating) {
            localStorage.removeItem('adminScrollPosition');
        }
    });
});

// Admin panelində scroll pozisiyasını qoruyan əlavə funksiyalar
(function() {
    'use strict';
    
    // Admin panelində scroll pozisiyasını qoruyan funksiya
    function preserveAdminScroll() {
        // Mövcud scroll pozisiyasını qoruyur
        const currentScroll = window.pageYOffset || document.documentElement.scrollTop;
        
        // LocalStorage-də saxlayır
        if (currentScroll > 0) {
            localStorage.setItem('adminScroll_' + window.location.pathname, currentScroll);
        }
        
        // Səhifə yükləndikdə scroll pozisiyasını bərpa edir
        const savedScroll = localStorage.getItem('adminScroll_' + window.location.pathname);
        if (savedScroll) {
            setTimeout(() => {
                window.scrollTo(0, parseInt(savedScroll));
            }, 100);
        }
    }
    
    // Admin panelində olduğumuzu yoxlayır
    if (window.location.pathname.includes('/admin/')) {
        // Səhifə yükləndikdə scroll pozisiyasını bərpa edir
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', preserveAdminScroll);
        } else {
            preserveAdminScroll();
        }
        
        // Scroll pozisiyasını qoruyur
        let scrollTimeout;
        window.addEventListener('scroll', function() {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(function() {
                const currentScroll = window.pageYOffset || document.documentElement.scrollTop;
                if (currentScroll > 0) {
                    localStorage.setItem('adminScroll_' + window.location.pathname, currentScroll);
                }
            }, 100);
        });
    }
})(); 