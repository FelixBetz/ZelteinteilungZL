<script lang="ts">
	import type { IData, ILink, INode } from '$lib/_apiParticipants';
	import NetworkChart from '$lib/chart/NetworkChart.svelte';
	import { apiGetTmpTodo } from '$lib/_apiParticipants';
	import { onMount } from 'svelte';
	import { group } from 'd3';

	function hasIntersection(setA: Set<string>, setB: Set<string>): boolean {
		for (let elem of setB) {
			if (setA.has(elem)) {
				return true;
			}
		}
		return false;
	}

	let chart: NetworkChart;

	let data: IData = {
		nodes: [],
		links: []
	};

	let groups = [];

	function getGroupIndex(name: string): number {
		for (let i = 0; i < groups.length; i++) {
			if (groups[i].has(name)) {
				return i;
			}
		}

		return -1;
	}

	async function getTmpTodo() {
		let tmpDodos = await apiGetTmpTodo();

		let loc_nodes: INode[] = [];
		let loc_links: ILink[] = [];

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
			for (let k = 0; k < groups.length; k++) {}
		}

		let cnt = 0;
		for (let i = 0; i < groups.length; i++) {
			for (let k = 0; k < groups.length; k++) {
				if (i != k && hasIntersection(groups[i], groups[k])) {
					groups[i] = new Set([...groups[i], ...groups[k]]);

					groups.splice(k, 1);

					i = 0;
				}
			}
		}
		console.log(groups);

		for (let i = 0; i < tmpDodos.length; i++) {
			let name = tmpDodos[i].name;
			let groupIndex = getGroupIndex(name);

			if (groups[groupIndex].size > 1) {
				loc_nodes.push({ id: name, group: groupIndex });
				for (let k = 0; k < tmpDodos[i].friends.length; k++) {
					loc_links.push({ source: name, target: tmpDodos[i].friends[k], value: 1 });
				}
			}
		}
		data.nodes = loc_nodes;
		data.links = loc_links;
	}
	onMount(() => {
		getTmpTodo();
	});
</script>

{#if data.nodes.length > 0}
	<div class="chart" style="margin-top:50px; background-color: green">
		<NetworkChart bind:this={chart} graph={data} />
	</div>
{/if}

<style>
	.chart {
		width: 100%;

		height: calc(100% - 4em);

		margin: 0 auto;
	}
</style>
