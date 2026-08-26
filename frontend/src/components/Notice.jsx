import { Link } from "react-router-dom";

/** Единый блок для состояний «загрузка», «ошибка» и «пусто». */
export default function Notice({ text, variant, backLink = false }) {
  return (
    <p className={variant === "error" ? "notice notice--error" : "notice"}>
      {text}
      {backLink && (
        <>
          <br />
          <Link to="/" className="notice__action">
            Вернуться к товарам
          </Link>
        </>
      )}
    </p>
  );
}
