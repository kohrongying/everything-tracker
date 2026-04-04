<script lang="ts">
	import { resolve } from '$app/paths';
	import SectionCard from '$lib/ui/SectionCard.svelte';
	import { Wallet, Apple, Dumbbell, Zap } from 'lucide-svelte';
</script>

<!-- Hero Section -->
<div class="hero min-h-[500px] bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600">
	<div class="hero-content text-center text-white">
		<div class="max-w-2xl">
			<h1 class="text-5xl font-black sm:text-6xl">Everything Tracker</h1>
			<p class="mt-6 text-lg font-light sm:text-xl">
				Your all-in-one lifestyle companion. Track spending, nutrition, fitness, and focus in
				real-time.
			</p>
			<div class="mt-8 flex flex-col gap-3 sm:flex-row sm:justify-center">
				<a href={resolve('/login')} class="btn btn-primary">Sign In</a>
				<a href={resolve('/setup')} class="btn btn-outline btn-primary">Setup Profile</a>
			</div>
		</div>
	</div>
</div>

<!-- Main Content -->
<div class="mx-auto w-full max-w-6xl px-6 py-16">
	<!-- Tracking Categories Header -->
	<div class="mb-12">
		<h2 class="mb-4 text-3xl font-bold">Track Everything</h2>
		<p class="text-base-content/70">
			Choose a category to start tracking and maintaining your lifestyle goals.
		</p>
	</div>

	<!-- Cards Grid -->
	<div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
		<SectionCard
			title="Expenses"
			description="Track spending in SGD"
			href="/expense"
			icon={Wallet}
		/>
		<SectionCard title="Meals" description="Log nutrition and calories" href="/food" icon={Apple} />
		<SectionCard
			title="Workouts"
			description="Record exercises and weights"
			href="/exercise"
			icon={Dumbbell}
		/>
		<SectionCard
			title="Focus Sessions"
			description="Deep work with distraction tracking"
			href="/focus"
			icon={Zap}
		/>
	</div>
</div>
