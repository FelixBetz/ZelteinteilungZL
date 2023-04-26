<script lang="ts">
	import * as d3 from 'd3';
	import { drag, zoom } from 'd3';
	import { onMount } from 'svelte';

	import type { IData } from '$lib/_apiParticipants';

	/*const links = [
		{ source: 'Microsoft', target: 'Amazon', type: 'friend' },
		{ source: 'Microsoft', target: 'HTC', type: 'friend' },
		{ source: 'Samsung', target: 'Apple', type: 'friend' },
		{ source: 'Motorola', target: 'Apple', type: 'friend' },
		{ source: 'Nokia', target: 'Apple', type: 'friend' },
		{ source: 'HTC', target: 'Apple', type: 'friend' },
		{ source: 'Kodak', target: 'Apple', type: 'friend' },
		{ source: 'Microsoft', target: 'Barnes & Noble', type: 'friend' },
		{ source: 'Microsoft', target: 'Foxconn', type: 'friend' },
		{ source: 'Oracle', target: 'Google', type: 'friend' },
		{ source: 'Apple', target: 'HTC', type: 'friend' },
		{ source: 'Microsoft', target: 'Inventec', type: 'friend' },
		{ source: 'Samsung', target: 'Kodak', type: 'friend' },
		{ source: 'LG', target: 'Kodak', type: 'friend' },
		{ source: 'RIM', target: 'Kodak', type: 'friend' },
		{ source: 'Sony', target: 'LG', type: 'friend' },
		{ source: 'Kodak', target: 'LG', type: 'friend' },
		{ source: 'Apple', target: 'Nokia', type: 'friend' },
		{ source: 'Qualcomm', target: 'Nokia', type: 'friend' },
		{ source: 'Apple', target: 'Motorola', type: 'friend' },
		{ source: 'Microsoft', target: 'Motorola', type: 'friend' },
		{ source: 'Motorola', target: 'Microsoft', type: 'friend' },
		{ source: 'Huawei', target: 'ZTE', type: 'friend' },
		{ source: 'Ericsson', target: 'ZTE', type: 'friend' },
		{ source: 'Kodak', target: 'Samsung', type: 'friend' },
		{ source: 'Apple', target: 'Samsung', type: 'friend' },
		{ source: 'Kodak', target: 'RIM', type: 'friend' },
		{ source: 'Nokia', target: 'Qualcomm', type: 'friend' }
	];
	const nodes = [
		{
			id: 'Microsoft'
		},
		{
			id: 'Amazon'
		},
		{
			id: 'HTC'
		},
		{
			id: 'Samsung'
		},
		{
			id: 'Apple'
		},
		{
			id: 'Motorola'
		},
		{
			id: 'Nokia'
		},
		{
			id: 'Kodak'
		},
		{
			id: 'Barnes & Noble'
		},
		{
			id: 'Foxconn'
		},
		{
			id: 'Oracle'
		},
		{
			id: 'Google'
		},
		{
			id: 'Inventec'
		},
		{
			id: 'LG'
		},
		{
			id: 'RIM'
		},
		{
			id: 'Sony'
		},
		{
			id: 'Qualcomm'
		},
		{
			id: 'Huawei'
		},
		{
			id: 'ZTE'
		},
		{
			id: 'Ericsson'
		}
	];*/

	let width = 1800;
	let height = 800;

	let container;
	let simulation;

	let node, link;
	let types = [1];

	const colourScale = d3.scaleOrdinal(d3.schemeCategory10);

	const testData: IData = {
		nodes: [
			{
				id: 'Christian Behrendt',
				group: '1'
			},
			{
				id: 'Lennart Übelhör',
				group: '2'
			},
			{
				id: 'Mauro Romer',
				group: '4'
			},
			{
				id: 'Philipp Schmid',
				group: '6'
			},
			{
				id: 'Samuel Frick',
				group: '8'
			},
			{
				id: 'Simon Frick',
				group: '9'
			},
			{
				id: 'Kilian Armbruster',
				group: '10'
			},
			{
				id: 'Paul Bischoff',
				group: '10'
			},
			{
				id: 'Vincent Dörrler',
				group: '11'
			},
			{
				id: 'Benjamin Abt',
				group: '12'
			},
			{
				id: 'Samuel Abt',
				group: '13'
			},
			{
				id: 'Jonas Faigle',
				group: '14'
			},
			{
				id: 'Vincent Romer',
				group: '14'
			},
			{
				id: 'Luc Wahlenmayer',
				group: '15'
			},
			{
				id: 'Vincent Wahlenmayer',
				group: '16'
			},
			{
				id: 'Robin Dreyer',
				group: '16'
			},
			{
				id: 'Magnus Roland',
				group: '17'
			},
			{
				id: 'Theo Frey',
				group: '17'
			},
			{
				id: 'Benedikt Föhr',
				group: '18'
			}
		],
		links: [
			{
				source: 'Paul Bischoff',
				target: 'Kilian Armbruster',
				value: 1
			},
			{
				source: 'Jonas Faigle',
				target: 'Vincent Romer',
				value: 1
			},
			{
				source: 'Vincent Wahlenmayer',
				target: 'Robin Dreyer',
				value: 1
			},
			{
				source: 'Robin Dreyer',
				target: 'Vincent Wahlenmayer',
				value: 1
			},
			{
				source: 'Magnus Roland',
				target: 'Theo Frey',
				value: 1
			},
			{
				source: 'Theo Frey',
				target: 'Magnus Roland',
				value: 1
			}
		]
	};

	let linkArc = (d) => `M${d.source.x},${d.source.y}A0,0 0 0,1 ${d.target.x},${d.target.y}`;

	function handleZoom(e) {
		d3.selectAll('g').attr('transform', e.transform);
		d3.selectAll('marker').attr('transform', e.transform);
		link.attr('d', linkArc);
		node.attr('transform', (d) => `translate(${d.x},${d.y})`);
	}
	onMount(() => {
		const svg = d3.select(container).call(zoom().on('zoom', handleZoom));
		//.attr('viewBox', [-width / 2, -height / 2, width, height]);

		simulation = d3
			.forceSimulation(testData.nodes)
			.force(
				'link',
				d3.forceLink(testData.links).id((d) => d.id)
			)
			.force('charge', d3.forceManyBody().strength(-0))
			.force('x', d3.forceX())
			.force('y', d3.forceY())
			.force('collide', d3.forceCollide(70))
			.force('center', d3.forceCenter(width / 2, height / 2));

		// Per-type markers, as they don't inherit styles.
		svg
			.append('defs')
			.selectAll('marker')
			.data(types)
			.join('marker')
			.attr('id', (d) => `arrow-${d}`)
			.attr('viewBox', '0 -5 10 10')
			.attr('refX', 38)
			.attr('refY', 0)
			.attr('markerWidth', 6)
			.attr('markerHeight', 6)
			.attr('orient', 'auto')
			.append('path')
			.attr('fill', 'black')
			.attr('d', 'M0,-5L10,0L0,5');

		link = svg
			.append('g')
			.attr('fill', 'none')
			.attr('stroke-width', 1.5)
			.selectAll('path')
			.data(testData.links)
			.join('path')
			.attr('stroke', 'black')
			.attr('marker-end', (d) => `url(${new URL(`#arrow-${d.value}`, location)})`);

		node = svg
			.append('g')
			.attr('fill', 'currentColor')
			.attr('stroke-linecap', 'round')
			.attr('stroke-linejoin', 'round')
			.selectAll('g')
			.data(testData.nodes)
			.join('g')
			.call(drag(simulation));

		node
			.append('circle')
			.attr('stroke', 'white')
			.attr('stroke-width', 1.5)
			.attr('r', 25)
			.attr('fill', (d) => colourScale(d.group));

		node
			.append('text')
			.attr('x', 30 + 4)
			.attr('y', '0.31em')
			.text((d) => d.id)
			.clone(true)
			.lower()
			.attr('fill', 'none')
			.attr('stroke', 'white')
			.attr('stroke-width', 3);

		node.on('dblclick', (e, d) => console.log(testData.nodes[d.index]));

		simulation.on('tick', () => {
			link.attr('d', linkArc);
			node.attr('transform', (d) => `translate(${d.x},${d.y})`);
		});
		svg.node();
	});
</script>

<div>
	<svg bind:this={container} {width} {height} style="border: 1px black solid" />
</div>
