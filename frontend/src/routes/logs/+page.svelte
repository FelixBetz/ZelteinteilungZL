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
		<div class="col-sm-3">
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
		<div class="col-sm-9">
			<h3>Revisions <span class="badge bg-info">{logs.revisions.length}</span></h3>

			{#if logs.revisions.length == 0}
				<i>keine Einträge</i>
			{/if}
			<div class="row">
				{#each logs.revisions as log, logIndex}
					<div class="col-sm-6">
						<div class="card border-secondary mb-1 position-relative">
							<div class="text-right text-white position-absolute top-0 end-0 me-2">
								<i>Revision {logIndex}</i>
							</div>
							<div class="card-header {log.isError ? ' bg-danger' : ' bg-info'} p-1">
								<div class="text-white">
									<strong>
										ID {log.id}
										<i> {log.fullname ? '(' + log.fullname + ')' : ''} </i>
									</strong>
								</div>
							</div>
							<div class="card-body text-white p-1 ps-3 {log.isError ? ' bg-danger' : 'bg-info'}">
								<!--Revision Error-->
								{#if log.isError}
									<p class="card-text">
										<strong>Error Message: </strong><i>{log.errorMessage}</i><br />
										Eigenschaft <strong>&quot;{log.property}&quot;</strong> wurde nicht zu
										<strong>&quot;{log.newValue}&quot;</strong> geändert
									</p>

									<!--Revison log-->
								{:else}
									<p class="card-text">
										<strong>&quot;{log.property}&quot;</strong>:
										<strong>
											<i>&quot;{log.oldValue}&quot;</i> <i class="bi bi-arrow-right" />
											<i>&quot;{log.newValue}&quot;</i>
										</strong>
									</p>
								{/if}
							</div>
						</div>
					</div>
				{/each}
			</div>
		</div>
	</div>
</div>
