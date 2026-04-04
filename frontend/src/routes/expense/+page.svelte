<script lang="ts">
	import { addExpense } from '$lib/api';

	let amount = $state(0);
	let description = $state('');
	let message = $state('');

	async function submitExpense() {
		try {
			await addExpense(amount, description);
			message = 'Expense saved';
			amount = 0;
			description = '';
		} catch (error) {
			message = error instanceof Error ? error.message : 'Could not save expense';
		}
	}
</script>

<div class="mx-auto max-w-3xl p-4">
	<h2 class="text-2xl font-bold">Add Expense</h2>

	<div class="grid gap-4">
		<div class="form-control">
			<label class="label" for="amount"><span class="label-text">Amount (SGD)</span></label>
			<input id="amount" type="number" bind:value={amount} min="0" class="input-bordered input" />
		</div>
		<div class="form-control">
			<label class="label" for="description"><span class="label-text">Description</span></label>
			<input id="description" type="text" bind:value={description} class="input-bordered input" />
		</div>
		<button class="btn btn-primary" onclick={submitExpense}>Add Expense</button>
	</div>
	{#if message}
		<p class="mt-2 text-sm text-success">{message}</p>
	{/if}
</div>
