<script lang="ts">
	import { apiGetConfigs, apiPostConfigs, type Configs } from '$lib/_apiParticipants';
	import { onMount } from 'svelte';

	let configs: Configs = { numTents: 9999, zlStart: '1970-08-12' };

	async function getConfigs() {
		configs = await apiGetConfigs();
	}
	async function postConfigs() {
		configs = await apiPostConfigs(configs);
	}

	onMount(() => {
		getConfigs();
	});
</script>

<svelte:head>
	<title>Configs</title>
</svelte:head>
<div class="container">
	<h1>Configs</h1>

	<div class="col-sm-3">
		<div class="mb-3">
			<label for="numTents" class="form-label">Anzahl Zelte:</label>
			<div class="form-floating">
				<input
					type="number"
					class="form-control"
					id="numTents"
					placeholder="Enter lastname"
					bind:value={configs.numTents}
				/>
				<label for="numTents">Anzahl Zelte</label>
			</div>
		</div>

		<div class="mb-3">
			<label for="start" class="form-label">Start des Zeltlagers</label>
			<div class="form-floating">
				<input
					class="form-control"
					type="date"
					placeholder="Enter start"
					id="start"
					bind:value={configs.zlStart}
					on:change={() => {
						let splittedBitdateStr = configs.zlStart.split('-');
						let y = splittedBitdateStr[0];
						let m = splittedBitdateStr[1];
						let d = splittedBitdateStr[2];
						if (configs != undefined) {
							configs.zlStart = y + '-' + m + '-' + d;
						}
					}}
				/>
				<label for="start">Start des Zeltlagers</label>
			</div>
		</div>
		<div class="mb-3">
			<button class="btn btn-primary btn-lg w-100" on:click={postConfigs}>Save</button>
		</div>
	</div>
</div>
