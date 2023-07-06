<script lang="ts">
	import { BASE_URL } from '$lib/api/api';
	import {
		apiGetGenerateOverallList,
		apiGetListsDownloadLinks,
		type List
	} from '$lib/api/apiLists';
	import { onMount } from 'svelte';

	let lists: List[] = [];

	async function generatateOverallList() {
		await apiGetGenerateOverallList();
		getLists();
	}
	async function getLists() {
		lists = await apiGetListsDownloadLinks();
		lists = lists;
	}

	onMount(() => {
		getLists();
	});
</script>

<div class="container-fluid text-white">
	<div class="row">
		<div class="col-sm-3">
			<div
				class="btn btn-primary"
				on:click={generatateOverallList}
				on:keydown={generatateOverallList}
			>
				Generate Overall List
			</div>
		</div>
	</div>
	<div class="row mt-3">
		<div class="sm-3">
			<h3>Lists</h3>
			<ul>
				{#each lists as l}
					<li>
						<a target="_blank" href={BASE_URL + l.link}>{l.name}</a>
					</li>
				{/each}
			</ul>
		</div>
	</div>
</div>
