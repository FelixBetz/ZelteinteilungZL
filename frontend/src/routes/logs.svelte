<script lang="ts">
	import { apiGetLogs, type Logs } from '$lib/_apiParticipants';
	import { onMount } from 'svelte';
	import { Row, Col } from 'sveltestrap/src';
	let logs: Logs = { errors: [], revisions: [] };

	async function getErrorLogs() {
		logs = await apiGetLogs();
	}

	onMount(() => {
		getErrorLogs();
	});
</script>

<h1>Logs</h1>
<Row>
	<Col sm="3">
		<h3>Error Logs</h3>
		<ul>
			{#if logs.errors.length == 0}
				<li>keine Einträge</li>
			{/if}
			{#each logs.errors as log, logIndex}
				<li><strong>{logIndex}: </strong> {log}</li>
			{/each}
		</ul>
	</Col>
	<Col sm="3">
		<h3>Revisions</h3>
		<ul>
			{#if logs.revisions.length == 0}
				<li>keine Einträge</li>
			{/if}
			{#each logs.revisions as log, logIndex}
				<li><strong>{logIndex}: </strong> {log}</li>
			{/each}
		</ul>
	</Col>
</Row>
