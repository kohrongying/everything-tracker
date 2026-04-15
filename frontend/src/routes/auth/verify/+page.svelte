<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import { verifyMagicLink } from '$lib/api';

	let status: 'verifying' | 'success' | 'error' = $state('verifying');

	onMount(async () => {
		const token = page.url.searchParams.get('token');
		if (!token) {
			status = 'error';
			return;
		}
		try {
			await verifyMagicLink(token);
			status = 'success';
			goto('/');
		} catch {
			status = 'error';
		}
	});
</script>

<div class="flex min-h-screen items-center justify-center bg-base-200">
	<div class="card w-96 bg-base-100 shadow-xl">
		<div class="card-body items-center text-center">
			{#if status === 'verifying'}
				<span class="loading loading-spinner loading-lg"></span>
				<p>Verifying your magic link...</p>
			{:else if status === 'success'}
				<p class="text-success">Verified! Redirecting...</p>
			{:else}
				<p class="text-error">Invalid or expired link.</p>
				<a href="/login" class="btn btn-primary mt-2">Back to Login</a>
			{/if}
		</div>
	</div>
</div>
