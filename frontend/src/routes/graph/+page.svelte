<script lang="ts">
	import type { IData } from '$lib/_apiParticipants';
	import NetworkChart from '$lib/chart/NetworkChart.svelte';
	import { apiGetGraph, type GraphInput } from '$lib/_apiParticipants';
	import { onMount } from 'svelte';

	function hasIntersection(setA: Set<string>, setB: Set<string>): boolean {
		for (let elem of setB) {
			if (setA.has(elem)) {
				return true;
			}
		}
		return false;
	}

	let chart: NetworkChart;
	let chartData: IData[] = [];
	let groups: Set<string>[] = [];

	function getByName(name: string, array: GraphInput[]) {
		for (let i = 0; i < array.length; i++) {
			if (array[i].name == name) {
				return array[i];
			}
		}
		console.log(name, ' not find');
	}

	async function getGraph() {
		let tmpDodos = await apiGetGraph();

		for (let i = 0; i < tmpDodos.length; i++) {
			let name = tmpDodos[i].name;

			let loc_set = new Set<string>();
			loc_set.add(name);

			for (let k = 0; k < tmpDodos[i].friends.length; k++) {
				let friendName = tmpDodos[i].friends[k];

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

		let cnt_index = 1;
		for (let i = 0; i < groups.length; i++) {
			let loc_index = 0;
			if (groups[i].size > 3) {
				loc_index = cnt_index;
				cnt_index++;
			}

			if (undefined == chartData[loc_index]) {
				chartData[loc_index] = { nodes: [], links: [] };
			}
			for (let name of Array.from(groups[i].values())) {
				let loc_element = getByName(name, tmpDodos);
				if (loc_element !== undefined) {
					chartData[loc_index].nodes.push({ id: loc_element.name, group: i });

					for (let k = 0; k < loc_element.friends.length; k++) {
						chartData[loc_index].links.push({
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

<!--
<Row>
	{#each chartData as data}
		<Col sm="2">
			<ul>
				{#each data.nodes as d}
					<li>{d.id} ({d.group})</li>
				{/each}
			</ul>
		</Col>
	{/each}
</Row>
{screen.width}
{screen.height}
<Row>
	{#each chartData as data, index}
		{#if index == 0}
			<Col sm="12">
				<NetworkChart bind:this={chart} graph={data} height={400} width={600} />
			</Col>
		{:else}
			<Col sm="4">
				<NetworkChart bind:this={chart} graph={data} height={200} width={200} />
			</Col>
		{/if}
	{/each}
</Row>-->

{#each chartData as data, index}
	{#if index == 0}
		<NetworkChart bind:this={chart} graph={data} height={800} width={600} />
	{:else}
		<NetworkChart bind:this={chart} graph={data} height={400} width={600} />
	{/if}
{/each}
