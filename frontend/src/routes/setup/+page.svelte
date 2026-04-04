<script lang="ts">
	let height = $state(0);
	let weight = $state(0);
	let bmi = $derived.by(() => (height > 0 ? weight / (height / 100) ** 2 : 0));

	function saveProfile() {
		// TODO: Save setup details in backend with BMI calculation
	}
</script>

<div class="flex min-h-screen items-center justify-center bg-base-200">
	<div class="card w-96 bg-base-100 shadow-xl">
		<div class="card-body">
			<h2 class="card-title">Setup</h2>
			<div class="form-control">
				<label class="label" for="height">
					<span class="label-text">Height (cm)</span>
				</label>
				<input id="height" type="number" bind:value={height} class="input-bordered input" min="0" />
			</div>
			<div class="form-control">
				<label class="label" for="weight">
					<span class="label-text">Weight (kg)</span>
				</label>
				<input id="weight" type="number" bind:value={weight} class="input-bordered input" min="0" />
			</div>
			<p class="text-sm opacity-80">BMI: {bmi.toFixed(2)}</p>
			<div class="card-actions justify-end">
				<button class="btn btn-primary" onclick={saveProfile}>Save</button>
			</div>
		</div>
	</div>
</div>
