import { getProducts }      from '../api/products.js';
import { getCategories }    from '../api/categories.js';
import { addToCart }        from '../store/cart.js';
import { renderHeader, syncCartBadge } from '../components/header.js';

console.log('[catalog] script loaded');

const PLACEHOLDER = '/assets/images/placeholder.jpg';

// Безопасное экранирование текста, попадающего в innerHTML
function escapeHtml(s) {
    return String(s ?? '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
}

function productCard(p) {
    const img = p.image_url || PLACEHOLDER;
    const cat = p.category && p.category.name ? p.category.name : '';
    return `
        <article class="card product-card" data-id="${p.id}">
            <img src="${escapeHtml(img)}"
                 alt="${escapeHtml(p.name)}"
                 onerror="this.onerror=null;this.src='${PLACEHOLDER}'">
            <div class="product-card__body">
                <span class="badge">${escapeHtml(cat)}</span>
                <h3 class="product-name">${escapeHtml(p.name)}</h3>
                <p class="product-price">${Number(p.price).toLocaleString('ru-RU')} ₽</p>
                <button class="btn btn-primary" data-add="${p.id}">В корзину</button>
            </div>
        </article>
    `;
}

function init() {
    renderHeader();
    syncCartBadge();

    const grid    = document.getElementById('products-grid');
    const countEl = document.getElementById('products-count');
    const list    = document.getElementById('category-list');

    if (!grid || !list) {
        console.error('[catalog] DOM элементы не найдены: grid=%o list=%o', grid, list);
        return;
    }

    let allProducts = [];
    let active = 'all';

    function render() {
        const filtered = active === 'all'
            ? allProducts
            : allProducts.filter((p) => p.category_id === Number(active));

        if (countEl) countEl.textContent = `${filtered.length} товаров`;

        if (!filtered.length) {
            grid.innerHTML = '<p style="padding:20px;color:#888;">Товаров в этой категории нет.</p>';
            return;
        }

        grid.innerHTML = filtered.map(productCard).join('');
        console.log('[catalog] rendered %d cards', filtered.length);
    }

    function bindCategoryClicks() {
        list.querySelectorAll('[data-category]').forEach((btn) => {
            btn.addEventListener('click', () => {
                active = btn.dataset.category;
                list.querySelectorAll('[data-category]').forEach((b) => b.classList.remove('active'));
                btn.classList.add('active');
                render();
            });
        });
    }

    function renderCategories(categories) {
        const items = categories.map((c) =>
            `<li><button class="category-btn" data-category="${c.id}">${escapeHtml(c.name)}</button></li>`
        ).join('');
        list.insertAdjacentHTML('beforeend', items);
        bindCategoryClicks();
    }

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

    grid.innerHTML = '<p style="padding:20px;">Загрузка...</p>';

    Promise.all([getProducts(), getCategories()])
        .then(([products, categories]) => {
            allProducts = Array.isArray(products) ? products : (products?.products ?? []);
            console.log('[catalog] loaded %d products, %d categories', allProducts.length, categories.length);
            renderCategories(categories);
            render();
        })
        .catch((err) => {
            console.error('[catalog] load failed:', err);
            grid.innerHTML = `<p style="padding:20px;color:red;">Не удалось загрузить товары.<br><small>${escapeHtml(err.message)}</small></p>`;
        });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
