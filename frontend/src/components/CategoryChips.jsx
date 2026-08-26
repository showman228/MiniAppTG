/** Лента бирок. activeId === null означает «Все». */
export default function CategoryChips({ categories, activeId, onSelect }) {
  const chip = (id, label) => (
    <button
      key={id ?? "all"}
      type="button"
      className={activeId === id ? "chip chip--active" : "chip"}
      onClick={() => onSelect(id)}
    >
      {label}
    </button>
  );

  return (
    <nav className="categories" aria-label="Категории товаров">
      <div className="categories__track">
        {chip(null, "Все")}
        {categories.map((category) => chip(category.id, category.name))}
      </div>
    </nav>
  );
}
