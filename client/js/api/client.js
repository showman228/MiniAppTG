const BASE_URL = "http://localhost:8000/api"

async function request(method, path, body = null) {
    const options = {
        method,
        headers:{
            "Content-Type": "application/json"
        }
    }

    if (body !== null) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(`${BASE_URL}${path}`, options)

    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`[${response.status}] ${path} — ${errorText}`);
    }

    const contentType = response.headers.get("Content-Type") || "";
    if (!contentType.includes("application/json")) {
        return null;
    }

    return response.json();
}

export const get    = (path)        => request("GET",    path);
export const post   = (path, body)  => request("POST",   path, body);
export const put    = (path, body)  => request("PUT",    path, body);
export const del    = (path, body)  => request("DELETE", path, body);