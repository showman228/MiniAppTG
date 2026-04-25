// Базовый префикс — nginx проксирует /api/ → FastAPI
const BASE_URL = "/api";

async function request(method, path, body = null) {
    const url = `${BASE_URL}${path}`;
    const options = {
        method,
        headers: { "Accept": "application/json" },
    };

    if (body !== null) {
        options.headers["Content-Type"] = "application/json";
        options.body = JSON.stringify(body);
    }

    let response;
    try {
        response = await fetch(url, options);
    } catch (e) {
        throw new Error(`Network error при запросе ${method} ${url}: ${e.message}`);
    }

    if (!response.ok) {
        const errorText = await response.text().catch(() => "");
        throw new Error(`[${response.status}] ${method} ${url} — ${errorText.slice(0, 200)}`);
    }

    const ct = response.headers.get("Content-Type") || "";
    if (!ct.includes("application/json")) return null;
    return response.json();
}

export const get  = (path)       => request("GET",    path);
export const post = (path, body) => request("POST",   path, body);
export const put  = (path, body) => request("PUT",    path, body);
export const del  = (path, body) => request("DELETE", path, body);
