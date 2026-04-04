const baseUrl = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';

async function request<T>(path: string, method = 'GET', body?: unknown): Promise<T> {
	const response = await fetch(`${baseUrl}${path}`, {
		method,
		headers: {
			'Content-Type': 'application/json'
		},
		body: body ? JSON.stringify(body) : undefined
	});

	if (!response.ok) {
		throw new Error(`API request failed: ${response.statusText}`);
	}

	return response.json();
}

export function signInWithGoogle() {
	window.location.href = `${baseUrl}/auth/login`;
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
