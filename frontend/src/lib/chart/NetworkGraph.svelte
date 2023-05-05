<script lang="ts">
	import * as d3 from 'd3';
	import { drag } from 'd3';
	import { onMount } from 'svelte';
	import type { ILink, INode } from '$lib/api/apiGraphs';

	let width = 1800;
	let height = 800;

	export let containerHeight = '100vh';
	export let containerWidth = '100%';

	let container: SVGSVGElement;
	let simulation;
	//@ts-ignore
	let node;
	//@ts-ignore
	let link;
	let types = [0, 1, 2, 3];

	export let nodes: INode[] = [];
	export let links: ILink[] = [];

	const colourScale = d3.scaleOrdinal(d3.schemeCategory10);
	//@ts-ignore
	let linkArc = (d) => `M${d.source.x},${d.source.y}A0,0 0 0,1 ${d.target.x},${d.target.y}`;
	let zoomFunc = d3.zoom().on('zoom', handleZoom);
	//@ts-ignore
	function handleZoom(e) {
		d3.select(container).selectAll('g').attr('transform', e.transform);
		d3.select(container).selectAll('marker').attr('transform', e.transform);
		//@ts-ignore
		link.attr('d', linkArc);
		//@ts-ignore
		node.attr('transform', (d) => `translate(${d.x},${d.y})`);
	}

	function getLinksColor(pVal: number) {
		switch (pVal) {
			case 1:
				return 'black';
			case 2:
				console.log('green');
				return 'green';
			case 3:
				return 'red';
			default:
				console.log(pVal);
				return 'black';
		}
	}

	onMount(() => {
		//@ts-ignore
		const svg = d3.select(container).call(zoomFunc);
		//.attr('viewBox', [-width / 2, -height / 2, width, height]);

		simulation = d3
			.forceSimulation(nodes)
			.force(
				'link',
				//@ts-ignore
				d3.forceLink(links).id((d) => d.id)
			)
			.force('collide', d3.forceCollide(80))
			.force('charge', d3.forceManyBody().strength(-800))

			.force('x', d3.forceX())
			.force('y', d3.forceY())

			.force('center', d3.forceCenter(width / 2, height / 2));

		// Per-type markers, as they don't inherit styles.
		svg
			.append('defs')
			.selectAll('marker')
			.data(types)
			.join('marker')
			.attr('id', (d) => `arrow-${d}`)
			.attr('viewBox', '0 -5 10 10')
			.attr('refX', 21)
			.attr('refY', 0)
			.attr('markerWidth', 6)
			.attr('markerHeight', 6)
			.attr('orient', 'auto')
			.append('path')
			.attr('fill', (d) => getLinksColor(d))
			.attr('d', 'M0,-5L10,0L0,5');

		link = svg
			.append('g')
			.attr('fill', 'none')
			.attr('stroke-width', 1.5)
			.selectAll('path')
			.data(links)
			.join('path')
			.attr('stroke', (d) => getLinksColor(d.value))
			//@ts-ignore
			.attr('marker-end', (d) => `url(${new URL(`#arrow-${d.value}`, location)})`);

		node = svg
			.append('g')
			.attr('fill', 'currentColor')
			.attr('stroke-linecap', 'round')
			.attr('stroke-linejoin', 'round')
			.selectAll('g')
			.data(nodes)
			.join('g')
			.call(drag);

		node
			.append('circle')
			.attr('stroke', 'white')
			.attr('stroke-width', 1.5)
			.attr('r', 10)
			.attr('fill', (d) => colourScale(d.group));

		node
			.append('text')
			.attr('x', 12)
			.attr('y', '0.31em')
			.text((d) => d.id)
			.clone(true)
			.lower()
			.attr('fill', 'none')
			.attr('stroke', 'white')
			.attr('stroke-width', 3);

		node.on('click', (e, d) => console.log(d));

		simulation.on('tick', () => {
			//@ts-ignore
			link.attr('d', linkArc);
			//@ts-ignore
			node.attr('transform', (d) => `translate(${d.x},${d.y})`);
		});
		svg.node();
	});
	/*function resetZoom(e: KeyboardEvent) {
		if (e.key == 'Escape') {
			d3.select(container).transition().call(zoomFunc.scaleTo, 1);
		}
	}*/
</script>

<div
	bind:clientWidth={width}
	bind:clientHeight={height}
	style="height: {containerHeight}; width:{containerWidth}; 	float: left; "
>
	<svg bind:this={container} {width} {height} style="border: 1px black solid" />
</div>
