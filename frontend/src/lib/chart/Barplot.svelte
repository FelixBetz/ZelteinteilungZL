<script lang="ts">
	import { onMount } from 'svelte';
	import * as d3 from 'd3';
	import type { BarplotData } from '$lib/helpers';

	let maxValue = 0;
	export let color = 'steelblue';

	let textSize = 30;

	$: maxValue = calcMaxValue(data);

	function calcMaxValue(pData: BarplotData[]): number {
		if (pData.length <= 0) {
			return 0;
		}
		return pData.reduce(function (prev, current) {
			return prev.value > current.value ? prev : current;
		}).value;
	}

	export let data: BarplotData[] = [];
	let container: SVGSVGElement;

	onMount(() => {
		const margin = { top: 30, right: 0, bottom: 45, left: 45 };
		let width = 500;
		let height = 300 - margin.top - margin.bottom;

		let svg = d3
			.select(container)
			.attr('viewBox', [
				0,
				0,
				width + margin.left + margin.right,
				height + margin.top + margin.bottom
			])
			.append('g')
			.attr('transform', `translate(${margin.left},${margin.top})`);

		const x = d3.scaleBand().range([0, width]).padding(0.1);
		const y = d3.scaleLinear().range([height, 0]);

		x.domain(data.map((d) => d.label));
		y.domain([0, maxValue]).nice();

		svg
			.selectAll('.bar')
			.data(data)
			.enter()
			.append('rect')
			.attr('class', 'bar')
			.attr('x', (d) => x(d.label))
			.attr('width', x.bandwidth())
			.attr('y', (d) => y(d.value))
			.attr('height', (d) => height - y(d.value))
			.attr('fill', color);

		svg
			.append('g')
			.attr('transform', `translate(0,${height})`)
			.call(d3.axisBottom(x))
			.attr('font-size', textSize + 'px');

		svg
			.append('g')
			.call(d3.axisLeft(y).ticks(5).tickFormat(d3.format('.0f')))
			.attr('font-size', textSize + 'px');

		svg
			.selectAll('.text')
			.data(data)
			.enter()
			.append('text')
			.attr('class', 'text')
			.attr('text-anchor', 'middle')
			.attr('font-size', textSize + 'px')
			.attr('x', (d) => x(d.label) + x.bandwidth() / 2)
			.attr('y', (d) => y(d.value) - 5)
			.text((d) => d.value);
	});
</script>

<svg bind:this={container} width="100%" height="100%" />
