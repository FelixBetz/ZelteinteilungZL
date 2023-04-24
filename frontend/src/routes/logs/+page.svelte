<script lang="ts">
	import { apiGetLogs, type Logs } from '$lib/_apiParticipants';
	import { onMount } from 'svelte';

	let logs: Logs = { errors: [], revisions: [] };

	async function getErrorLogs() {
		logs = await apiGetLogs();
	}

	onMount(() => {
		getErrorLogs();
	});
</script>

<svelte:head>
	<title>Logs</title>
</svelte:head>

<div class="m-5">
	<h1>Logs</h1>
	<div class="row">
		<div class="col-sm-6">
			<h3>Error Logs <span class="badge bg-danger">{logs.errors.length}</span></h3>

			{#if logs.errors.length == 0}
				<i>keine Einträge</i>
			{/if}
			{#each logs.errors as log, logIndex}
				<div class="card border-secondary mb-3" style="max-width: 30rem;">
					<div class="card-header bg-danger">
						<h5 class="card-title text-white">Error {logIndex}</h5>
					</div>
					<div class="card-body text-white bg-danger">
						<p class="card-text">{log}</p>
					</div>
				</div>
			{/each}
		</div>
		<div class="col-sm-6">
			<h3>Revisions <span class="badge bg-info">{logs.revisions.length}</span></h3>

			{#if logs.revisions.length == 0}
				<i>keine Einträge</i>
			{/if}
			{#each logs.revisions as log, logIndex}
				<div class="card border-secondary mb-3" style="max-width: 30rem;">
					<div class="card-header bg-info">
						<h5 class="card-title text-white">Error {logIndex}</h5>
					</div>
					<div class="card-body text-white bg-info">
						<p class="card-text">{log}</p>
					</div>
				</div>
			{/each}
		</div>
	</div>
</div>
