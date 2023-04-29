<script lang="ts">
	import type { DateGraphData } from '$lib/helpers';
	import * as d3 from 'd3';
	import { onMount } from 'svelte';

	export let containerHeight = '100vh';
	export let containerWidth = '100%';

	let container: SVGSVGElement;

	const margin = { top: 20, right: 20, bottom: 30, left: 50 };
	const width = 800 - margin.left - margin.right;
	const height = 300 - margin.top - margin.bottom;

	export let data: DateGraphData[] = [];

	onMount(() => {
		const svg = d3
			.select(container)
			.attr('width', width + margin.left + margin.right)
			.attr('height', height + margin.top + margin.bottom);

		const chartGroup = svg
			.append('g')
			.attr('transform', `translate(${margin.left}, ${margin.top})`);

		const x = d3
			.scaleTime()
			.domain(d3.extent(data, (d) => d.date))
			.range([0, width]);

		const y = d3
			.scaleLinear()
			.domain([0, d3.max(data, (d) => d.num)])
			.range([height, 0]);

		chartGroup.append('g').attr('transform', `translate(0, ${height})`).call(d3.axisBottom(x));

		chartGroup.append('g').call(d3.axisLeft(y));

		const line = d3
			.line()
			.x((d) => x(d.date))
			.y((d) => y(d.num));

		chartGroup
			.append('path')
			.datum(data)
			.attr('fill', 'none')
			.attr('stroke', 'steelblue')
			.attr('stroke-width', 5)
			.attr('d', line);
	});
</script>

<div style="height: {containerHeight}; width:{containerWidth}; 	float: left; ">
	<svg bind:this={container} {width} {height} />
</div>
