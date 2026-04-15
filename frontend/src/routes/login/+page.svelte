<script lang="ts">
	import { requestMagicLink } from '$lib/api';

	let email = $state('');
	let status: 'idle' | 'loading' | 'sent' | 'error' = $state('idle');

	async function handleSubmit() {
		status = 'loading';
		try {
			await requestMagicLink(email);
			status = 'sent';
		} catch {
			status = 'error';
		}
	}
</script>

<div class="flex min-h-screen items-center justify-center bg-base-200">
	<div class="card w-96 bg-base-100 shadow-xl">
		<div class="card-body">
			<h2 class="card-title">Login</h2>
			{#if status === 'sent'}
				<p class="text-success">Check your email inbox/spam for an email from EverythingTracker. Use that link to login securely.</p>
			{:else}
				<p class="text-base-content/60">Enter your email:</p>
				<input
					type="email"
					bind:value={email}
					placeholder="you@example.com"
					class="input input-bordered w-full"
				/>
				{#if status === 'error'}
					<p class="text-error text-sm">Failed to send magic link. Try again.</p>
				{/if}
				<div class="card-actions justify-end">
					<button
						class="btn btn-primary w-full"
						disabled={!email || status === 'loading'}
						onclick={handleSubmit}
					>
						Login
					</button>
				</div>
			{/if}
		</div>
	</div>
</div>
