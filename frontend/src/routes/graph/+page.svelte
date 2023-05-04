<script lang="ts">
	import { apiGetGraph, type GraphInput, type IData } from '$lib/api/apiGraphs';
	import { onMount } from 'svelte';
	import NetworkGraph from '../../lib/chart/NetworkGraph.svelte';
	import CircleList from '$lib/chart/CircleList.svelte';

	function hasIntersection(setA: Set<string>, setB: Set<string>): boolean {
		for (let elem of setB) {
			if (setA.has(elem)) {
				return true;
			}
		}
		return false;
	}

	let chartData: IData[] = [];
	let groups: Set<string>[] = [];

	function getByName(name: string, array: GraphInput[]) {
		for (let i = 0; i < array.length; i++) {
			if (array[i].name == name) {
				return array[i];
			}
		}
	}

	async function getGraph() {
		let graphData = await apiGetGraph();

		for (let i = 0; i < graphData.length; i++) {
			let name = graphData[i].name;

			let loc_set = new Set<string>();
			loc_set.add(name);

			for (let k = 0; k < graphData[i].friends.length; k++) {
				let friendName = graphData[i].friends[k];

				loc_set.add(friendName);
			}
			groups.push(loc_set);
		}

		for (let i = 0; i < groups.length; i++) {
			for (let k = 0; k < groups.length; k++) {
				if (i != k && hasIntersection(groups[i], groups[k])) {
					groups[i] = new Set([...groups[i], ...groups[k]]);
					groups.splice(k, 1);
					i = 0;
				}
			}
		}

		chartData[0] = { nodes: [], links: [] }; //paricipants with friends
		chartData[1] = { nodes: [], links: [] }; //participants without friends

		for (let i = 0; i < groups.length; i++) {
			let chartIndex = 0;
			if (groups[i].size > 1) {
				chartIndex = 0; //paricipants with friends
			} else {
				chartIndex = 1; //participants without friends
			}

			for (let name of Array.from(groups[i].values())) {
				let loc_element = getByName(name, graphData);
				if (loc_element !== undefined) {
					chartData[chartIndex].nodes.push({ id: loc_element.name, group: i.toString() });

					for (let k = 0; k < loc_element.friends.length; k++) {
						chartData[chartIndex].links.push({
							source: name,
							target: loc_element.friends[k],
							value: 1
						});
					}
				}
			}
		}

		chartData = chartData;
	}
	onMount(() => {
		getGraph();
	});
</script>

<svelte:head>
	<title>Graph</title>
</svelte:head>

<div class="container-fluid">
	{#each chartData as data, index}
		{#if index == 0}
			<NetworkGraph
				nodes={data.nodes}
				links={data.links}
				containerWidth={'80%'}
				containerHeight={'85vh'}
			/>
		{:else}
			<CircleList
				nodes={data.nodes}
				containerWidth={'20%'}
				containerHeight={'85vh'}
				title={'Keine Freunde 😔:'}
			/>
		{/if}
	{/each}
</div>
