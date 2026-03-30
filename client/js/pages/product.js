import { getProductById }   from '../api/products.js';
import { addToCart }        from '../store/cart.js';
import { renderHeader, syncCartBadge } from '../components/header.js';

renderHeader();
syncCartBadge();

const params    = new URLSearchParams(location.search);
const productId = params.get('id');
const wrap      = document.getElementById('product-content');

if (!productId) {
    wrap.innerHTML = '<p>Товар не найден.</p>';
} else {
    loadProduct(productId);
}

async function loadProduct(id) {
    wrap.innerHTML = '<p style="padding:20px;">Загрузка...</p>';

    try {
        // getProductById(id) → GET /api/products/{id}
        const p = await getProductById(id);

        wrap.innerHTML = `
            <div>
                <img class="product-image"
                     src="${p.image_url || '/assets/images/placeholder.jpg'}"
                     alt="${p.name}">
            </div>
            <div>
                <span class="badge">${p.category?.name || ''}</span>
                <h1 class="page-title">${p.name}</h1>
                <p class="product-price">${p.price} ₽</p>
                <p>${p.description || ''}</p>
                <button class="btn btn-primary" id="add-btn">Добавить в корзину</button>
                <p class="success-msg" id="success-msg">✓ Товар добавлен в корзину</p>
            </div>
        `;

        document.getElementById('add-btn').addEventListener('click', () => {
            addToCart(p);
            const msg = document.getElementById('success-msg');
            msg.classList.add('show');
            setTimeout(() => msg.classList.remove('show'), 1600);
        });

    } catch (err) {
        console.error('[Product]', err);
        wrap.innerHTML = `<p style="color:red;">Товар не найден.<br><small>${err.message}</small></p>`;
    }
}