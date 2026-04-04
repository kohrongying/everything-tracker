<script lang="ts">
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';

	let { title = '', description = '', href = '', icon: IconComponent } = $props();

	function handleClick() {
		if (href) {
			void goto(resolve(href));
		}
	}
</script>

<a
	href={resolve(href)}
	onclick={(e) => {
		e.preventDefault();
		handleClick();
	}}
	class="card cursor-pointer bg-base-200 shadow-md transition-all duration-300 hover:scale-105 hover:shadow-lg"
>
	<div class="card-body items-center text-center">
		{#if IconComponent}
			<div class="mb-2 flex h-16 w-16 items-center justify-center rounded-xl bg-primary/10">
				<IconComponent class="h-8 w-8 text-primary" />
			</div>
		{/if}
		<h3 class="card-title text-lg">{title}</h3>
		<p class="text-sm text-base-content/70">{description}</p>
	</div>
</a>
