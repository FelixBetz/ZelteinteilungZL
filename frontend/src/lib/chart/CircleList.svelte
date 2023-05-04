<script lang="ts">
	import * as d3 from 'd3';

	import { onMount } from 'svelte';
	import type { INode } from '$lib/api/apiGraphs';

	export let containerHeight = '100vh';
	export let containerWidth = '100%';
	export let title = '';
	export let nodes: INode[] = [];

	let container: SVGSVGElement;

	let width = 1800;
	let height = 800;

	let node;

	let radius = 10;
	let yOffset = 25;
	let yMargin = 30;

	const colourScale = d3.scaleOrdinal(d3.schemeCategory10);

	onMount(() => {
		const svg = d3.select(container);

		node = svg
			.append('g')
			.attr('fill', 'currentColor')
			.attr('stroke-linecap', 'round')
			.attr('stroke-linejoin', 'round')
			.selectAll('g')
			.data(nodes)
			.join('g');

		node
			.append('circle')
			.attr('cx', 25)
			.attr('cy', (d, i) => yOffset + i * yMargin - radius / 2)
			.attr('stroke', 'white')
			.attr('stroke-width', 1.5)
			.attr('r', radius)
			.attr('fill', (d) => colourScale(d.group));

		node
			.append('text')
			.attr('x', 50)
			.attr('y', (d, i) => i * yMargin + yOffset)
			.text((d) => d.id);

		svg.node();
	});
</script>

<div
	bind:clientWidth={width}
	bind:clientHeight={height}
	style="height: {containerHeight}; width:{containerWidth}; 	float: left; border: 1px black solid"
>
	{#if title != ''}
		<h3>{title}</h3>
	{/if}
	<svg bind:this={container} {width} {height} />
</div>
