<script lang="ts">
	import { apiGetParticipants } from './participants/_apiParticipants';
	import type { Participant } from './participants/_apiParticipants';
	import { onMount } from 'svelte';
	import { flip } from 'svelte/animate';

	let participants: Participant[] = [];

	async function getParticipants() {
		participants = await apiGetParticipants();
	}

	onMount(() => {
		getParticipants();
	});

	let baskets = [
		{
			name: 'Basket 1',
			items: ['Orange', 'Pineapple']
		},
		{
			name: 'Basket 2',
			items: ['Banana', 'Apple']
		},
		{
			name: 'Basket 3',
			items: ['GrapeFruit']
		}
	];

	let hoveringOverBasket: string;
	function dragStart(event, basketIndex: number, itemIndex: number) {
		// The data we want to make available when the element is dropped
		// is the index of the item being dragged and
		// the index of the basket from which it is leaving.
		const data = { basketIndex, itemIndex };
		event.dataTransfer.setData('text/plain', JSON.stringify(data));
	}

	function drop(event, basketIndex: number) {
		event.preventDefault();
		const json = event.dataTransfer.getData('text/plain');
		const data = JSON.parse(json);

		// Remove the item from one basket.
		// Splice returns an array of the deleted elements, just one in this case.
		const [item] = baskets[data.basketIndex].items.splice(data.itemIndex, 1);

		// Add the item to the drop target basket.
		baskets[basketIndex].items.push(item);
		baskets = baskets;

		hoveringOverBasket = '';
	}
</script>

<p>Zelteinteilung</p>

<ul>
	{#each participants as participant}
		<li draggable={true}>{participant.firstname} {participant.lastname}</li>
	{/each}
</ul>

{#each baskets as basket, basketIndex (basket)}
	<div animate:flip>
		<b>{basket.name}</b>
		<ul
			class:hovering={hoveringOverBasket === basket.name}
			on:dragenter={() => (hoveringOverBasket = basket.name)}
			on:dragleave={() => (hoveringOverBasket = '')}
			on:drop={(event) => drop(event, basketIndex)}
			ondragover="return false"
		>
			{#each basket.items as item, itemIndex (item)}
				<div class="item" animate:flip>
					<li draggable={true} on:dragstart={(event) => dragStart(event, basketIndex, itemIndex)}>
						{item}
					</li>
				</div>
			{/each}
		</ul>
	</div>
{/each}

<style>
	.hovering {
		border-color: orange;
	}
	.item {
		display: inline; /* required for flip to work */
	}
	li {
		background-color: lightgray;
		cursor: pointer;
		display: inline-block;
		margin-right: 10px;
		padding: 10px;
	}
	li:hover {
		background: orange;
		color: white;
	}
	ul {
		border: solid lightgray 1px;
		display: flex; /* required for drag & drop to work when .item display is inline */
		height: 40px; /* needed when empty */
		padding: 10px;
	}
</style>
