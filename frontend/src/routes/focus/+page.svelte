<script lang="ts">
	import { addFocusSession } from '$lib/api';

	let seconds = $state(0);
	let isActive = $state(false);
	let timer: number;
	let message = $state('');

	function startSession() {
		isActive = true;
		timer = window.setInterval(() => {
			seconds += 1;
		}, 1000);
	}

	async function stopSession() {
		isActive = false;
		window.clearInterval(timer);
		try {
			await addFocusSession(seconds);
			message = 'Focus session saved';
		} catch (error) {
			message = error instanceof Error ? error.message : 'Could not save focus session';
		}
	}

	function handleVisibilityChange() {
		if (document.hidden && isActive) {
			void stopSession();
		}
	}

	if (typeof window !== 'undefined') {
		document.addEventListener('visibilitychange', handleVisibilityChange);
	}
</script>

<div class="mx-auto max-w-3xl p-4">
	<h2 class="text-2xl font-bold">In Progress</h2>
</div>
