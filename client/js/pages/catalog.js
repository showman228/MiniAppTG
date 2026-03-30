import { getProducts }      from '../api/products.js';
import { getCategories }    from '../api/categories.js';
import { addToCart }        from '../store/cart.js';
import { renderHeader, syncCartBadge } from '../components/header.js';

renderHeader();
syncCartBadge();

const grid    = document.getElementById('products-grid');
const countEl = document.getElementById('products-count');
const buttons = document.querySelectorAll('[data-category]');

let allProducts = [];   // все товары с бэкенда
let active = 'all';     // текущая выбранная категория

// Фильтрует и рендерит карточки товаров
function render() {
    const filtered = active === 'all'
        ? allProducts
        : allProducts.filter((p) => p.category_id === Number(active));

    countEl.textContent = `${filtered.length} товаров`;

    if (!filtered.length) {
        grid.innerHTML = '<p style="padding:20px;color:#888;">Товаров в этой категории нет.</p>';
        return;
    }

    grid.innerHTML = filtered.map((p) => `
        <article class="card product-card" data-id="${p.id}">
            <img src="${p.image_url || '/assets/images/placeholder.jpg'}" alt="${p.name}">
            <div class="product-card__body">
                <span class="badge">${p.category?.name || ''}</span>
                <h3 class="product-name">${p.name}</h3>
                <p class="product-price">${p.price} ₽</p>
                <button class="btn btn-primary" data-add="${p.id}">В корзину</button>
            </div>
        </article>
    `).join('');
}

// Клик по карточке — переход на товар, клик по кнопке — добавить в корзину
grid.addEventListener('click', (e) => {
    const addBtn = e.target.closest('[data-add]');
    if (addBtn) {
        e.stopPropagation();
        const product = allProducts.find((p) => p.id === Number(addBtn.dataset.add));
        if (product) addToCart(product);
        return;
    }
    const card = e.target.closest('.product-card');
    if (card) location.href = `/product.html?id=${card.dataset.id}`;
});

// Клик по кнопкам категорий
buttons.forEach((btn) => {
    btn.addEventListener('click', () => {
        active = btn.dataset.category;
        buttons.forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
        render();
    });
});

// Загрузка товаров с бэкенда
async function init() {
    grid.innerHTML = '<p style="padding:20px;">Загрузка...</p>';
    try {
        // getProducts() → GET /api/products/ → возвращает { products: [...], total: N }
        const data = await getProducts();
        allProducts = data.products ?? data; // на случай если бэкенд вернёт просто массив
        render();
    } catch (err) {
        console.error('[Catalog]', err);
        grid.innerHTML = `<p style="padding:20px;color:red;">Не удалось загрузить товары.<br><small>${err.message}</small></p>`;
    }
}

init();