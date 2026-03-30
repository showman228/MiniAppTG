const sideMenu = document.getElementById('sideMenu');
const overlay = document.getElementById('overlay');


// =============================
// ОТКРЫТИЕ БОКОВОГО МЕНЮ
// =============================
function openMenu() {

    if (!sideMenu || !overlay) return;

    sideMenu.classList.add('open');

    overlay.classList.add('show');

    sideMenu.setAttribute('aria-hidden', 'false');
    overlay.setAttribute('aria-hidden', 'false');
}


// =============================
// ЗАКРЫТИЕ БОКОВОГО МЕНЮ
// =============================
function closeMenu() {

    if (!sideMenu || !overlay) return;

    sideMenu.classList.remove('open');

    overlay.classList.remove('show');

    sideMenu.setAttribute('aria-hidden', 'true');
    overlay.setAttribute('aria-hidden', 'true');
}


// =============================
// ИНИЦИАЛИЗАЦИЯ МЕНЮ
// =============================
function initSideMenu() {

    const openMenuButton = document.getElementById('openMenu');

    const closeMenuButton = document.getElementById('closeMenu');


    if (openMenuButton && !openMenuButton.dataset.boundMenu) {

        openMenuButton.addEventListener('click', openMenu);

        openMenuButton.dataset.boundMenu = 'true';
    }


    if (closeMenuButton && !closeMenuButton.dataset.boundMenu) {

        closeMenuButton.addEventListener('click', closeMenu);

        closeMenuButton.dataset.boundMenu = 'true';
    }


    if (overlay && !overlay.dataset.boundMenu) {

        overlay.addEventListener('click', closeMenu);

        overlay.dataset.boundMenu = 'true';
    }
}



window.initSideMenu = initSideMenu;


initSideMenu();