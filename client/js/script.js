const API_BASE_URL = "http://127.0.0.1:8000";

async function loadCategories() {
    try {
        const response = await fetch(`${API_BASE_URL}/category/`)
        const categories = await response.json();

        const track = document.querySelector(".categories__track");

        categories.forEach(category => {
            const input = document.createElement("input");
            input.type = 'radio';
            input.name = 'category';        
            input.id = `cat-${category.slug}`;
            input.className = 'visually-hidden';
            input.dataset.categorySlug = category.slug;

            const label = document.createElement("label");
            label.setAttribute('for', `cat-${category.slug}`);
            label.className = 'chip';
            label.dataset.categorySlug = category.slug; 
            label.textContent = category.name;

            track.appendChild(input);
            track.appendChild(label);
        });
    }
    catch(error) {
        console.error('Не удалось загрузить категории:', error);
    }   
}

function formatPrice(price) {
    return `${price.toLocaleString('ru-RU')} ₽`;
}

function pluralizeTovar(count) {
    const mod10 = count % 10;
    const mod100 = count % 100;

    if (mod10 === 1 && mod100 !== 11) return 'товар';
    if ([2, 3, 4].includes(mod10) && ![12, 13, 14].includes(mod100)) return 'товара';
    return 'товаров';
}

function createProductCard(product) {
    const article = document.createElement('article');
    article.className = 'product-card';
    article.dataset.categorySlug = product.category.slug;

    const media = document.createElement('div');
    media.className = 'product-card__media';
    if (product.image_url) {
        const img = document.createElement('img');
        img.src = `${API_BASE_URL}${product.image_url}`;
        img.alt = product.name;
        img.loading = 'lazy';
        media.appendChild(img);
    }

    const body = document.createElement('div');
    body.className = 'product-card__body';

    const name = document.createElement('h3');
    name.className = 'product-card__name';
    name.textContent = product.name;

    const row = document.createElement('div');
    row.className = 'product-card__row';

    const price = document.createElement('span');
    price.className = 'product-card__price';
    price.textContent = formatPrice(product.price);

    const addButton = document.createElement('button');
    addButton.className = 'product-card__add';
    addButton.type = 'button';
    addButton.dataset.productId = product.id;
    addButton.textContent = 'В корзину';

    row.appendChild(price);
    row.appendChild(addButton);
    body.appendChild(name);
    body.appendChild(row);

    article.appendChild(media);
    article.appendChild(body);

    return article;
}

async function loadProducts() {
    try {
        const response = await fetch(`${API_BASE_URL}/products/`);
        const products = await response.json();

        const grid = document.querySelector(".products__grid");
        const count = document.querySelector(".products__count");

        grid.innerHTML = '';
        products.forEach(product => {
            grid.appendChild(createProductCard(product));
        });

        if (count) {
            count.textContent = `${products.length} ${pluralizeTovar(products.length)}`;
        }
    }
    catch(error) {
        console.error("не удалось загрузить товары", error);
    }
}

function filterProductsByCategory(slug) {
    const cards = document.querySelectorAll('.product-card');
    let visibleCount = 0;

    cards.forEach(card => {
        const isVisible = slug === 'all' || card.dataset.categorySlug === slug;
        card.hidden = !isVisible;
        if (isVisible) visibleCount++;
    });

    const count = document.querySelector('.products__count');
    if (count) {
        count.textContent = `${visibleCount} ${pluralizeTovar(visibleCount)}`;
    }
}

document.querySelector('.categories__track').addEventListener('change', (event) => {
    if (event.target.name !== 'category') return;
    filterProductsByCategory(event.target.dataset.categorySlug);
});

loadCategories();
loadProducts();