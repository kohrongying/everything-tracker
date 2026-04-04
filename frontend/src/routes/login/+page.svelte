<script lang="ts">
	import { signInWithGoogle } from '$lib/api';
</script>

<div class="flex min-h-screen items-center justify-center bg-base-200">
	<div class="card w-96 bg-base-100 shadow-xl">
		<div class="card-body">
			<h2 class="card-title">Login</h2>
			<p>Sign in with Google to continue</p>
			<div class="card-actions justify-end">
				<button class="btn btn-primary" onclick={signInWithGoogle}>Sign in with Google</button>
			</div>
		</div>
	</div>
</div>
