/** Cliente HTTP hacia el backend FastAPI. */

// En desarrollo usamos rutas relativas + proxy de Vite (evita CORS / Failed to fetch).
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";

async function request(path, options = {}) {
  let response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, options);
  } catch {
    throw new Error(
      "No se pudo conectar con el backend. Verificá que uvicorn esté corriendo en el puerto 8000.",
    );
  }

  const contentType = response.headers.get("content-type") || "";
  const isJson = contentType.includes("application/json");
  const payload = isJson ? await response.json() : await response.text();

  if (!response.ok) {
    const detail =
      typeof payload === "object" && payload?.detail
        ? payload.detail
        : "Error al comunicar con el backend";
    throw new Error(detail);
  }

  return payload;
}

export async function healthCheck() {
  return request("/health");
}

export async function getIndexStatus() {
  return request("/status");
}

export async function uploadDocument(file) {
  const formData = new FormData();
  formData.append("file", file);

  return request("/upload", {
    method: "POST",
    body: formData,
  });
}

export async function askQuestion(query, threadId) {
  return request("/query", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query,
      thread_id: threadId || undefined,
    }),
  });
}
