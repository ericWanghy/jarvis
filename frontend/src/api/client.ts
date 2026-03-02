export const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:3721';

export interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  error: string | null;
  meta?: Record<string, any>;
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    // Try to parse error message from JSON
    try {
      const json = await res.json();
      throw new Error(json.error || `API Error: ${res.status} ${res.statusText}`);
    } catch (e) {
      throw new Error(`API Error: ${res.status} ${res.statusText}`);
    }
  }

  const json: ApiResponse<T> = await res.json();
  if (!json.success) {
    throw new Error(json.error || 'Unknown API error');
  }

  return json.data!;
}

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`);
  return handleResponse<T>(res);
}

export async function apiPost<T>(path: string, body?: unknown): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  });
  return handleResponse<T>(res);
}

export async function apiPut<T>(path: string, body?: unknown): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  });
  return handleResponse<T>(res);
}

export async function apiDelete<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: 'DELETE',
  });
  return handleResponse<T>(res);
}
