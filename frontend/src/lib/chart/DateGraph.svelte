<script lang="ts">
	import type { DateGraphData } from '$lib/helpers';
	import * as d3 from 'd3';
	import { onMount } from 'svelte';

	export let color = 'steelblue';

	let container: SVGSVGElement;

	const margin = { top: 5, right: 15, bottom: 20, left: 20 };
	let width = 500;
	let height = 300 - margin.top - margin.bottom;
	export let data: DateGraphData[] = [];

	onMount(() => {
		const svg = d3
			.select(container)
			.attr('viewBox', [
				0,
				0,
				width + margin.left + margin.right,
				height + margin.top + margin.bottom
			]);

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
			.attr('stroke', color)
			.attr('stroke-width', 5)
			.attr('d', line);

		// Define an area generator
		const area = d3
			.area()
			.x((d) => x(d.date))
			.y0(y(0))
			.y1((d) => y(d.num));

		// Add the area path to the chart
		chartGroup.append('path').datum(data).attr('fill', color).attr('opacity', 0.5).attr('d', area);

		// Add horizontal dotted lines
		chartGroup
			.append('g')
			.attr('class', 'grid')
			.call(d3.axisLeft(y).tickSize(-0).tickFormat('').ticks(5))
			.selectAll('line')
			.attr('x2', width) // extend the lines to the edge of the chart
			.attr('stroke-dasharray', '1 1') // make all lines dotted*/
			.attr('opacity', 0.5);
	});
</script>

<svg bind:this={container} width="100%" height="100%" />
