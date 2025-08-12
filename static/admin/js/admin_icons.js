// Admin Panel İkonları və Scroll Pozisiyası Qorunması
document.addEventListener('DOMContentLoaded', function() {
    // Təsdiqləmə və Səlahiyyət caption-ına ikon əlavə et
    const allH2s = document.querySelectorAll('h2');
    allH2s.forEach(function(h2) {
        if (h2.textContent.includes('Təsdiqləmə və Səlahiyyət')) {
            h2.innerHTML = '👥 Təsdiqləmə və Səlahiyyət';
        }
    });
    
    // Admin panelində scroll pozisiyasını qoruyan funksiyalar
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
            link.addEventListener('yıklə', function() {
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
                // Filter link-lərinə xüsusi class əlavə edir
                this.classList.add('admin-nav-links');
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
        
        // Admin panelində scroll pozisiyasını qoruyan əlavə funksiyalar
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
        
        // Admin panelində scroll pozisiyasını qoruyan CSS class-ları əlavə edir
        document.body.classList.add('admin-scroll-preserve');
        document.body.classList.add('admin-content');
        
        // Admin panelində naviqasiya zamanı scroll pozisiyasını qoruyan stillər
        const adminContent = document.querySelector('#content');
        if (adminContent) {
            adminContent.classList.add('scroll-preserve-container');
        }
        
        // Admin panelində form-larə scroll pozisiyasını qoruyan stillər
        const adminForms = document.querySelectorAll('form');
        adminForms.forEach(form => {
            form.classList.add('admin-form');
        });
        
        // Admin panelində breadcrumb scroll pozisiyasını qoruyan stillər
        const breadcrumbs = document.querySelector('.breadcrumbs');
        if (breadcrumbs) {
            breadcrumbs.classList.add('admin-navigation');
        }
        
        // Admin panelində pagination scroll pozisiyasını qoruyan stillər
        const paginator = document.querySelector('.paginator');
        if (paginator) {
            paginator.classList.add('admin-navigation');
        }
    }
    
    // Səhifə tərk edilərkən scroll pozisiyasını təmizləyir
    window.addEventListener('beforeunload', function() {
        if (isNavigating) {
            localStorage.removeItem('adminScrollPosition');
        }
    });
}); 