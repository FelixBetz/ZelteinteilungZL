<script lang="ts">
	import { apiGetParticipants } from '$lib/_apiParticipants';
	import type { cTentParticipant } from '$lib/_apiParticipants';
	import { onMount } from 'svelte';
	import { Col, Row, CardBody, CardHeader, CardTitle } from 'sveltestrap/src';
	import Tent from '$lib/TentParticipant.svelte';
	import TentParticipant from '$lib/TentParticipant.svelte';
	import { select, timeDay } from 'd3';

	interface Basket {
		name: string;
		items: number[];
	}

	let baskets: Basket[] = [
		{
			name: 'Backlog',
			items: []
		}
	];
	const numTents = 13;
	let participants: cTentParticipant[] = [];
	for (let i = 0; i < numTents; i++) {
		baskets.push({ name: 'Zelt ' + (i + 1), items: [] });
	}

	function compareByAge(a: cTentParticipant, b: cTentParticipant) {
		if (a.age < b.age) {
			return 1;
		}
		if (a.age > b.age) {
			return -1;
		}
		return 0;
	}

	let hoveringOverBasket: string;
	async function getParticipants() {
		let unsortedParticipants = await apiGetParticipants();
		participants = unsortedParticipants.sort(compareByAge);

		for (let i = 0; i < participants.length; i++) {
			let tentNumber = participants[i].tent;
			if (tentNumber < numTents) {
				baskets[tentNumber].items[baskets[tentNumber].items.length] = i;
			} else {
				baskets[0].items[baskets[0].items.length] = i;
			}
		}
	}

	onMount(() => {
		getParticipants();
	});

	function dragStart(event: DragEvent, basketIndex: number, itemIndex: number) {
		// The data we want to make available when the element is dropped
		// is the index of the item being dragged and
		// the index of the basket from which it is leaving.
		const data = { basketIndex, itemIndex };
		event.dataTransfer?.setData('text/plain', JSON.stringify(data));
	}

	function drop(
		event: DragEvent & { currentTarget: EventTarget & HTMLDivElement },
		basketIndex: number
	) {
		event.preventDefault();
		const json = event.dataTransfer?.getData('text/plain');

		if (json !== undefined) {
			const data = JSON.parse(json);

			// Remove the item from one basket.
			// Splice returns an array of the deleted elements, just one in this case.
			const [item] = baskets[data.basketIndex].items.splice(data.itemIndex, 1);

			// Add the item to the drop target basket.
			baskets[basketIndex].items.push(item);
			baskets = baskets;
		}

		hoveringOverBasket = '';
	}
</script>

<svelte:head>
	<title>Zelteinteilung</title>
</svelte:head>

<Row>
	<Col sm="8">
		<Row>
			{#each baskets as b, basketIndex}
				{#if basketIndex > 0}
					<Col sm="6">
						<div
							class="card"
							class:hovering={hoveringOverBasket === b.name}
							on:dragenter={() => (hoveringOverBasket = b.name)}
							on:dragleave={() => (hoveringOverBasket = '')}
							on:drop={(event) => drop(event, basketIndex)}
							on:dragover={(event) => {
								if (b.items.length <= 6) {
									event.preventDefault();
								}
							}}
							style="margin: 10px; "
						>
							<CardHeader>
								<CardTitle>Zelt {basketIndex}</CardTitle>
							</CardHeader>
							<div class="card-body" class:tent_alert={b.items.length >= 7}>
								<Row>
									{#each b.items as item, itemIndex}
										<Tent
											participant={participants[item]}
											on:dragstart={(event) => dragStart(event, basketIndex, itemIndex)}
										/>
									{/each}
								</Row>
							</div>
						</div>
					</Col>
				{/if}
			{/each}
		</Row>
	</Col>

	<Col sm="4" style="overflow-y: scroll;">
		<div
			class="card"
			class:hovering={hoveringOverBasket === baskets[0].name}
			on:dragenter={() => (hoveringOverBasket = baskets[0].name)}
			on:dragleave={() => (hoveringOverBasket = '')}
			on:drop={(event) => drop(event, 0)}
			on:dragover={(event) => event.preventDefault()}
			style="margin: 10px"
		>
			<CardHeader>
				<CardTitle>Backlog</CardTitle>
			</CardHeader>
			<CardBody>
				<Row>
					{#each baskets[0].items as item, itemIndex}
						<TentParticipant
							participant={participants[item]}
							on:dragstart={(event) => dragStart(event, 0, itemIndex)}
						/>
					{/each}
				</Row>
			</CardBody>
		</div>
	</Col>
</Row>

<style>
	.tent_alert {
		background-color: indianred;
	}
</style>
