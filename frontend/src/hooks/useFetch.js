import { useEffect, useState } from "react";

/**
 * GET-запрос с состояниями загрузки и ошибки.
 * request — функция, возвращающая промис. deps — когда перезапрашивать.
 * Передавай request === null, чтобы пропустить запрос (например, гость на /profile).
 */
export function useFetch(request, deps = []) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(Boolean(request));
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!request) {
      setLoading(false);
      return;
    }

    let alive = true;
    setLoading(true);
    setError(null);

    request()
      .then((res) => alive && setData(res))
      .catch((err) => alive && setError(err))
      .finally(() => alive && setLoading(false));

    return () => {
      alive = false;
    };
  }, deps);

  return { data, loading, error };
}
