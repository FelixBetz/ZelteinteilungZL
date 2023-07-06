<script lang="ts">
	import { apiGetLogs, type Logs } from '$lib/api/apiLogs';
	import { onMount } from 'svelte';
	import Masonry from 'svelte-bricks';

	let logs: Logs = { errors: [], revisions: [] };

	interface Revsions {
		id: number;
		indices: number[];
	}

	let revisionIdx: Revsions[] = [];

	$: createRevisionIdx(logs);
	function createRevisionIdx(logs: Logs) {
		let paricipantsIds = new Set<number>();

		logs.revisions.forEach((l) => {
			paricipantsIds.add(l.id);
		});

		revisionIdx = [];
		Array.from(paricipantsIds).forEach((el) => {
			revisionIdx[revisionIdx.length] = { id: el, indices: [] };
		});

		logs.revisions.forEach((logs, idx) => {
			revisionIdx.forEach((revison) => {
				if (logs.id == revison.id) {
					revison.indices.push(idx);
				}
			});
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

<div class="container-fluid text-white">
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
					<div class="card border-light bg-dark border-2 border mb-1 position-relative">
						<div class="text-right position-absolute top-0 end-0 me-2">
							<i>
								{item.indices.length > 1 ? 'Revisions' : 'Revision'}
								{#each item.indices as num, idx}
									{#if idx != item.indices.length - 1}
										{num},
									{:else}
										{num}
									{/if}
								{/each}
							</i>
						</div>
						<div
							class="card-header bg-dark {item.indices.reduce(
								(acc, val) => acc || logs.revisions[val].isError,
								false
							)
								? ' bg-danger '
								: ' bg-info'} p-1 rounded-top border-2 border-bottom border-light"
						>
							<div>
								<strong>
									<a class="link-light" href="/participant/{item.id}" target="_blanks"
										>ID {item.id}

										<i>
											{logs.revisions[item.indices[0]].fullname
												? '(' + logs.revisions[item.indices[0]].fullname + ')'
												: ''}
										</i></a
									>
								</strong>
							</div>
						</div>
						<div class="card-body text-white p-0">
							{#each item.indices as revsionIdx, idx}
								<div
									class="bg-info ps-3 pe-1
									{logs.revisions[revsionIdx].isError ? ' bg-danger' : 'bg-dark'} 
									{idx == item.indices.length - 1 ? ' rounded-bottom' : 'border-light border-1 border-bottom'}"
								>
									<!--Revision Error-->
									{#if logs.revisions[revsionIdx].isError}
										<p class="card-text">
											<strong>Error Message: </strong><i
												>{logs.revisions[revsionIdx].errorMessage}</i
											><br />
											Eigenschaft
											<strong>&quot;{logs.revisions[revsionIdx].property}&quot;</strong>
											wurde nicht zu
											<strong>&quot;{logs.revisions[revsionIdx].newValue}&quot;</strong> geändert
										</p>

										<!--Revison log-->
									{:else}
										<p class="card-text">
											<strong>&quot;{logs.revisions[revsionIdx].property}&quot;</strong>:
											<strong>
												<i>&quot;{logs.revisions[revsionIdx].oldValue}&quot;</i>
												<i class="bi bi-arrow-right" />
												<i>&quot;{logs.revisions[revsionIdx].newValue}&quot;</i>
											</strong>
										</p>
									{/if}
								</div>
							{/each}
						</div>
					</div>
				</Masonry>
			</div>
		</div>
	</div>
</div>
