<script lang="ts">
	import { onMount } from 'svelte';
	import { baseUrl } from '$lib/_apiParticipants';
	import NavbarParticipants from '$lib/NavbarParticipants.svelte';
	let randomNumber = 0;

	onMount(() => {
		randomNumber = Math.random();
	});
</script>

<NavbarParticipants />
<!--add radnom number to iframe src, to prevent browser from caching the iframe-->
<iframe
	on:click={() => console.log('asdfasf')}
	id="id_heatmap"
	title="heatmap"
	src={baseUrl + '/maps/heatmap.html?' + randomNumber}
	style="width:100%; height: calc(100vh - 125px) !important; "
/>
