<script lang="ts">
	import { onMount } from 'svelte';

	import { scaleLinear, scaleOrdinal } from 'd3-scale';
	import { zoom, zoomIdentity, ZoomTransform } from 'd3-zoom';
	import { schemeCategory10 } from 'd3-scale-chromatic';
	import { select, selectAll } from 'd3-selection';
	import { drag } from 'd3-drag';
	import { transition } from 'd3-transition';

	import {
		forceSimulation,
		forceLink,
		forceManyBody,
		forceCenter,
		forceX,
		forceY,
		type Simulation,
		type SimulationNodeDatum
	} from 'd3-force';
	import type { INode, IData, ILink } from '$lib/_apiParticipants';

	let d3 = {
		zoom,
		zoomIdentity,
		scaleLinear,
		scaleOrdinal,
		schemeCategory10,
		select,
		selectAll,
		drag,
		forceSimulation,
		forceLink,
		forceManyBody,
		forceCenter,
		forceX,
		forceY,
		transition
	};

	export let graph: IData;

	let svg: SVGSVGElement;
	export let width = 1500;
	export let height = 750;
	const nodeRadius = 10;

	const padding = { top: 20, right: 40, bottom: 40, left: 25 };

	$: links = graph.links.map((d: ILink) => {
		const ret: ILink = { target: d.target, source: d.source, value: d.value };
		return ret;
	});
	$: nodes = graph.nodes.map((d: INode) => {
		let ret: INode = { id: d.id, group: d.group };
		return ret;
	});

	const colourScale = d3.scaleOrdinal(d3.schemeCategory10);

	let transform = d3.zoomIdentity;
	let simulation;
	onMount(() => {
		simulation = d3
			.forceSimulation(nodes)
			.force(
				'link',
				d3.forceLink(links).id((d) => d.id)
			)
			.force('charge', d3.forceManyBody().strength(-10))
			.force('center', d3.forceCenter(width / 2, height / 2))

			//.force('x', d3.forceX())
			//.force('y', d3.forceY())
			.on('tick', simulationUpdate);

		let test = d3
			.select(svg)
			.call(
				d3
					.drag()
					.container(svg)
					.subject(dragsubject)
					.on('start', dragstarted)
					.on('drag', dragged)
					.on('end', dragended)
			)
			.call(
				d3
					.zoom()
					.scaleExtent([1 / 10, 8])
					.on('zoom', zoomed)
			);
	});

	function simulationUpdate() {
		simulation.tick();
		nodes = [...nodes];
		links = [...links];
	}

	function zoomed(currentEvent: { transform: ZoomTransform }) {
		transform = currentEvent.transform;
		simulationUpdate();
	}

	function dragsubject(currentEvent: { x: number; y: number }) {
		const node = simulation.find(
			transform.invertX(currentEvent.x),
			transform.invertY(currentEvent.y),
			nodeRadius
		);
		if (node) {
			node.x = transform.applyX(node.x);
			node.y = transform.applyY(node.y);
		}

		return node;
	}

	function dragstarted(currentEvent: {
		active: any;
		subject: { fx: number; x: number; fy: number; y: number };
	}) {
		if (!currentEvent.active) simulation.alphaTarget(0.3).restart();
		currentEvent.subject.fx = transform.invertX(currentEvent.subject.x);
		currentEvent.subject.fy = transform.invertY(currentEvent.subject.y);
	}

	function dragged(currentEvent: { subject: { fx: number; fy: number }; x: number; y: number }) {
		currentEvent.subject.fx = transform.invertX(currentEvent.x);
		currentEvent.subject.fy = transform.invertY(currentEvent.y);
	}

	function dragended(currentEvent: { active: any; subject: { fx: null; fy: null } }) {
		if (!currentEvent.active) simulation.alphaTarget(0);
		currentEvent.subject.fx = null;
		currentEvent.subject.fy = null;
	}

	function resize() {
		({ width, height } = svg.getBoundingClientRect());
	}

	function zoomFit(paddingPercent: number, transitionDuration: number) {
		var bounds = svg.getBBox();
		var parent = svg.parentElement;
		var fullWidth = parent.clientWidth,
			fullHeight = parent.clientHeight;
		var width = bounds.width,
			height = bounds.height;
		var midX = bounds.x + width / 2,
			midY = bounds.y + height / 2;
		if (width == 0 || height == 0) return; // nothing to fit
		var scale = (paddingPercent || 0.75) / Math.max(width / fullWidth, height / fullHeight);
		var translate = [fullWidth / 2 - scale * midX, fullHeight / 2 - scale * midY];

		//console.trace('zoomFit', translate, scale);
		console.trace(translate);

		//http://bl.ocks.org/TWiStErRob/b1c62730e01fe33baa2dea0d0aa29359
		/* todo
		let test = d3
			.select(svg)
			.transition()
			.duration(transitionDuration || 0) // milliseconds
			.call(zoom.translate(translate).scale(scale).event);*/
	}
</script>

<svelte:window on:resize={resize} />

<!--<button on:click={() => zoomFit(0.95, 500)}>fit</button>-->
<!-- SVG was here -->
<!--<svg bind:this={svg} {width} {height} style="border: 1px black solid">-->
<svg bind:this={svg} {width} {height} style="border: 1px black solid">
	{#each links as link}
		<g stroke="#999" stroke-opacity="0.6">
			<line
				x1={link.source.x}
				y1={link.source.y}
				x2={link.target.x}
				y2={link.target.y}
				transform="translate({transform.x} {transform.y}) scale({transform.k} {transform.k})"
			>
				<title>{link.source.id}</title>
			</line>
		</g>
	{/each}

	{#each nodes as point}
		<circle
			class="node"
			r="5"
			fill={colourScale(point.group)}
			cx={point.x}
			cy={point.y}
			transform="translate({transform.x} {transform.y}) scale({transform.k} {transform.k})"
		>
			<title>{point.id}</title>
		</circle>

		<!-- svelte-ignore component-name-lowercase -->
		<text
			x={point.x - 15}
			y={point.y + 2}
			font-size="7"
			transform="translate({transform.x} {transform.y}) scale({transform.k} {transform.k})"
		>
			{point.id}
		</text>
	{/each}
</svg>

<style>
	svg {
		float: left;
	}

	/*	circle {
		stroke: #fff;
		stroke-width: 1.5;
	}*/
</style>
