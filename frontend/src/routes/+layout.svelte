<script lang="ts">
	import './layout.css';
	import { resolve } from '$app/paths';
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="flex min-h-screen flex-col bg-base-100">
	<!-- Navbar -->
	<nav class="navbar bg-base-200 shadow-md">
		<div class="flex-1">
			<a href={resolve('/')} class="btn text-xl font-bold btn-ghost">Everything Tracker</a>
		</div>
		<div class="flex-none gap-2">
			<div class="dropdown dropdown-end">
				<div tabindex="0" role="button" class="btn avatar btn-circle btn-ghost">
					<div class="flex w-10 items-center justify-center rounded-full bg-primary text-white">
						<span>U</span>
					</div>
				</div>
				<ul
					role="menu"
					tabindex="0"
					class="dropdown-content menu z-[1] w-52 rounded-box bg-base-100 p-2 shadow"
				>
					<li><a href={resolve('/')}>Home</a></li>
					<li><a href={resolve('/setup')}>Profile</a></li>
					<li><a href={resolve('/login')}>Logout</a></li>
				</ul>
			</div>
		</div>
	</nav>

	<!-- Main Content -->
	<main class="flex-1">
		{@render children()}
	</main>

	<!-- Footer -->
	<footer class="footer border-t border-base-300 bg-base-200 p-6 text-base-content">
		<div class="flex-1">
			<h2 class="text-lg font-bold">Everything Tracker</h2>
			<p class="text-sm opacity-70">Track your lifestyle, one entry at a time.</p>
		</div>
		<div>
			<p class="text-sm opacity-70">&copy; 2026. All rights reserved.</p>
		</div>
	</footer>
</div>
