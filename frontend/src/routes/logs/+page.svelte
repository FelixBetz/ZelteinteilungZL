<script lang="ts">
	import { apiGetLogs, type Logs } from '$lib/api/apiLogs';
	import { onMount } from 'svelte';
	import Masonry from 'svelte-bricks';

	let logs: Logs = { errors: [], revisions: [] };

	let revisionIdx: number[] = [1, 2];

	$: createRevisionIdx(logs);
	function createRevisionIdx(logs: Logs) {
		revisionIdx = [];
		logs.revisions.forEach((revision, idx) => {
			console.log(idx);
			revisionIdx[revisionIdx.length] = idx;
		});
	}

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

<div class="container-fluid">
	<h1>Logs</h1>
	<div class="row">
		<div class="col-sm-2">
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
		<div class="col-sm-10">
			<h3>Revisions <span class="badge bg-info">{logs.revisions.length}</span></h3>

			{#if logs.revisions.length == 0}
				<i>keine Einträge</i>
			{/if}
			<div class="row">
				<Masonry items={revisionIdx} minColWidth={500} maxColWidth={500} gap={6} let:item>
					<div class="">
						<div class="card border-secondary mb-1 position-relative">
							<div class="text-right text-white position-absolute top-0 end-0 me-2">
								<i>Revision {item}</i>
							</div>
							<div
								class="card-header {logs.revisions[item].isError ? ' bg-danger' : ' bg-info'} p-1"
							>
								<div class="text-white">
									<strong>
										ID {logs.revisions[item].id}
										<i>
											{logs.revisions[item].fullname
												? '(' + logs.revisions[item].fullname + ')'
												: ''}
										</i>
									</strong>
								</div>
							</div>
							<div
								class="card-body text-white p-1 ps-3 {logs.revisions[item].isError
									? ' bg-danger'
									: 'bg-info'}"
							>
								<!--Revision Error-->
								{#if logs.revisions[item].isError}
									<p class="card-text">
										<strong>Error Message: </strong><i>{logs.revisions[item].errorMessage}</i><br />
										Eigenschaft <strong>&quot;{logs.revisions[item].property}&quot;</strong> wurde
										nicht zu
										<strong>&quot;{logs.revisions[item].newValue}&quot;</strong> geändert
									</p>

									<!--Revison log-->
								{:else}
									<p class="card-text">
										<strong>&quot;{logs.revisions[item].property}&quot;</strong>:
										<strong>
											<i>&quot;{logs.revisions[item].oldValue}&quot;</i>
											<i class="bi bi-arrow-right" />
											<i>&quot;{logs.revisions[item].newValue}&quot;</i>
										</strong>
									</p>
								{/if}
							</div>
						</div>
					</div>
				</Masonry>
			</div>
		</div>
	</div>
</div>
