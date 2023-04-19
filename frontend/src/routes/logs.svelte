<script lang="ts">
	import { apiGetLogs, type Logs } from '$lib/_apiParticipants';
	import { onMount } from 'svelte';
	import { Row, Col, Toast, ToastBody, ToastHeader, Container, Badge } from 'sveltestrap/src';
	let logs: Logs = { errors: [], revisions: [] };

	async function getErrorLogs() {
		logs = await apiGetLogs();
	}

	onMount(() => {
		getErrorLogs();
	});
</script>

<div class="m-5">
	<h1>Logs</h1>
	<Row>
		<Col sm="6">
			<h3>Error Logs <Badge color="danger">{logs.errors.length}</Badge></h3>

			{#if logs.errors.length == 0}
				<i>keine Einträge</i>
			{/if}
			{#each logs.errors as log, logIndex}
				<Toast class="mb-2">
					<ToastHeader icon="danger">Error {logIndex}</ToastHeader>
					<ToastBody>{log}</ToastBody>
				</Toast>
			{/each}
		</Col>
		<Col sm="6">
			<h3>Revisions <Badge color="info">{logs.revisions.length}</Badge></h3>

			{#if logs.revisions.length == 0}
				<i>keine Einträge</i>
			{/if}
			{#each logs.revisions as log, logIndex}
				<Toast class="mb-2">
					<ToastHeader icon="info">Error {logIndex}</ToastHeader>
					<ToastBody>{log}</ToastBody>
				</Toast>
			{/each}
		</Col>
	</Row>
</div>
