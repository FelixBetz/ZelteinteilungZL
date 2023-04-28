<script lang="ts">
	import { onMount } from 'svelte';
	import NavbarParticipants from '$lib/NavbarParticipants.svelte';
	import { BASE_URL } from '$lib/api/api';
	let randomNumber = 0;

	onMount(() => {
		randomNumber = Math.random();
	});
</script>

<svelte:head>
	<title>Heatmap</title>
</svelte:head>

<div class="container-fluid">
	<NavbarParticipants />
	<!--add radnom number to iframe src, to prevent browser from caching the iframe-->
	<iframe
		id="id_heatmap"
		title="heatmap"
		src={BASE_URL + '/maps/heatmap.html?' + randomNumber}
		style="width:100%; height: calc(100vh - 125px) !important; "
	/>
</div>
