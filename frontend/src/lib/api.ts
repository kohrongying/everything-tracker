const baseUrl = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';

const TOKEN_KEY = 'everything_tracker_access_token';

export const auth = {
	getToken: () => localStorage.getItem(TOKEN_KEY),
	setToken: (token: string) => localStorage.setItem(TOKEN_KEY, token),
	clearToken: () => localStorage.removeItem(TOKEN_KEY),
	isLoggedIn: () => !!localStorage.getItem(TOKEN_KEY)
};

async function request<T>(path: string, method = 'GET', body?: unknown): Promise<T> {
	const token = auth.getToken();
	const response = await fetch(`${baseUrl}${path}`, {
		method,
		headers: {
			'Content-Type': 'application/json',
			...(token ? { Authorization: `Bearer ${token}` } : {})
		},
		body: body ? JSON.stringify(body) : undefined
	});

	if (!response.ok) {
		throw new Error(`API request failed: ${response.statusText}`);
	}

	return response.json();
}

export async function requestMagicLink(email: string) {
	return request('/auth/magic-link', 'POST', { email });
}

export async function verifyMagicLink(token: string): Promise<string> {
	const res = await request<{ access_token: string }>(`/auth/verify?token=${token}`);
	auth.setToken(res.access_token);
	return res.access_token;
}

export async function addExpense(amount: number, description: string) {
	return request('/expense', 'POST', { amount, description });
}

export async function addFood(name: string, calories: number, protein: number) {
	return request('/food', 'POST', { name, calories, protein });
}

export async function addExercise(name: string, weight: number, reps: number, sets: number) {
	return request('/exercise', 'POST', { name, weight, reps, sets });
}

export async function addFocusSession(durationSeconds: number) {
	return request('/focus', 'POST', { duration_seconds: durationSeconds });
}
