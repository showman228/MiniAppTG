import { useState } from "react";

import CategoryChips from "../components/CategoryChips";
import ProductCard from "../components/ProductCard";
import Notice from "../components/Notice";
import { useFetch } from "../hooks/useFetch";
import { getCategories } from "../api/categories";
import { getProducts, getProductsByCategory } from "../api/products";
import { pluralizeTovar } from "../utils/format";

export default function HomePage() {
  const [categoryId, setCategoryId] = useState(null); // null — «Все»

  const categories = useFetch(getCategories, []);
  const products = useFetch(
    () => (categoryId === null ? getProducts() : getProductsByCategory(categoryId)),
    [categoryId],
  );

  const activeCategory = categories.data?.find((c) => c.id === categoryId);
  const items = products.data || [];

  return (
    <>
      <section className="hero">
        <div className="hero__inner">
          <p className="hero__eyebrow">Мини-магазин в Telegram</p>
          <h1 className="hero__title">
            Вещи по делу,
            <br />
            без лишнего
          </h1>
          <p className="hero__tagline">
            Одежда, аксессуары и гаджеты — прямо в чате, без установки приложений.
          </p>
        </div>
      </section>

      <CategoryChips
        categories={categories.data || []}
        activeId={categoryId}
        onSelect={setCategoryId}
      />

      <section className="products">
        <div className="products__head">
          <h2>{activeCategory ? activeCategory.name : "Все товары"}</h2>
          {!products.loading && !products.error && (
            <span className="products__count">
              {items.length} {pluralizeTovar(items.length)}
            </span>
          )}
        </div>

        {products.loading && <Notice text="Загружаем товары…" />}
        {products.error && <Notice text="Не удалось загрузить товары" variant="error" />}
        {!products.loading && !products.error && items.length === 0 && (
          <Notice text="В этой категории пока пусто" />
        )}

        {items.length > 0 && (
          <div className="products__grid">
            {items.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}
      </section>
    </>
  );
}
