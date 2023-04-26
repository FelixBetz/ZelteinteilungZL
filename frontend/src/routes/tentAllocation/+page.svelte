<script lang="ts">
	import {
		apiGetConfigs,
		apiGetParticipants,
		apiGetTentLeader,
		apiPostParticipants,
		type Configs,
		type cTentLeader
	} from '$lib/_apiParticipants';
	import type { cTentParticipant } from '$lib/_apiParticipants';
	import { onMount } from 'svelte';
	import Tent from '$lib/TentParticipant.svelte';
	import TentParticipant from '$lib/TentParticipant.svelte';
	let configs: Configs = { numTents: 9999, zlStart: '1970-08-12' };
	interface Basket {
		name: string;
		items: number[];
		tentLeaders: string[];
	}

	let baskets: Basket[] = [
		{
			name: 'Backlog',
			items: [],
			tentLeaders: []
		}
	];

	function clearBaskets() {
		baskets = [
			{
				name: 'Backlog',
				items: [],
				tentLeaders: []
			}
		];
		for (let i = 0; i < configs.numTents; i++) {
			baskets.push({ name: 'Zelt ' + (i + 1), items: [], tentLeaders: [] });
		}
	}

	let participants: cTentParticipant[] = [];

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

	function distributePartiscipantsToBaskets(
		arg_participants: cTentParticipant[],
		arg_tentLeaders: cTentLeader[]
	) {
		clearBaskets();
		participants = arg_participants.sort(compareByAge);

		//add participants to baskets
		for (let i = 0; i < participants.length; i++) {
			let tentNumber = participants[i].tent;
			if (tentNumber <= configs.numTents) {
				baskets[tentNumber].items[baskets[tentNumber].items.length] = i;
			} else {
				baskets[0].items[baskets[0].items.length] = i;
			}
		}

		//add tent leaders to baskets
		for (let i = 0; i < arg_tentLeaders.length; i++) {
			let tentNumber = arg_tentLeaders[i].tent;
			if (tentNumber > 0 && tentNumber <= configs.numTents) {
				baskets[tentNumber].tentLeaders[baskets[tentNumber].tentLeaders.length] =
					arg_tentLeaders[i].firstname + ' ' + arg_tentLeaders[i].lastname;
			}
		}
	}

	async function getParticipants() {
		configs = await apiGetConfigs();
		let tentLeaders = await apiGetTentLeader();
		let unsortedParticipants = await apiGetParticipants();
		distributePartiscipantsToBaskets(unsortedParticipants, tentLeaders);
	}

	async function saveParticipants() {
		for (let i = 0; i < baskets.length; i++) {
			for (let k = 0; k < baskets[i].items.length; k++) {
				let id = baskets[i].items[k];
				if (i == 0) {
					participants[id].tent = 9999;
				} else {
					participants[id].tent = i;
				}
			}
		}
		let unsortedParticipants = await apiPostParticipants(participants);
		let tentLeaders = await apiGetTentLeader();
		distributePartiscipantsToBaskets(unsortedParticipants, tentLeaders);
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
<div class="row" style="padding: 20px">
	<div
		class="btn btn-primary w-100"
		color="primary"
		on:click={saveParticipants}
		on:keydown={saveParticipants}
	>
		Save
	</div>
</div>
<div class="row">
	<div class="col-sm-8">
		<div class="row">
			{#each baskets as b, basketIndex}
				{#if basketIndex > 0}
					<div class="col-sm-6">
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
							style="margin: 10px; border: 1px solid black; "
						>
							<div class="card-header">
								<h5 class="card-title">
									Zelt {basketIndex} (
									{#each b.tentLeaders as leader}
										{leader}
									{/each})
								</h5>
							</div>
							<div
								class="card-body"
								class:tent_alert={b.items.length >= 7}
								class:tent_warning={b.items.length <= 5}
							>
								<div class="row">
									{#each b.items as item, itemIndex}
										<Tent
											participant={participants[item]}
											on:dragstart={(event) => dragStart(event, basketIndex, itemIndex)}
										/>
									{/each}
								</div>
							</div>
						</div>
					</div>
				{/if}
			{/each}
		</div>
	</div>

	<div class="col-sm-4" style="overflow-y: scroll;">
		<div
			class="card"
			class:hovering={hoveringOverBasket === baskets[0].name}
			on:dragenter={() => (hoveringOverBasket = baskets[0].name)}
			on:dragleave={() => (hoveringOverBasket = '')}
			on:drop={(event) => drop(event, 0)}
			on:dragover={(event) => event.preventDefault()}
			style="margin: 10px"
		>
			<div class="card-header">
				<h5 class="card-title">Backlog</h5>
			</div>

			<div class="card-body">
				<div class="row">
					{#each baskets[0].items as item, itemIndex}
						<TentParticipant
							participant={participants[item]}
							on:dragstart={(event) => dragStart(event, 0, itemIndex)}
						/>
					{/each}
				</div>
			</div>
		</div>
	</div>
</div>

<style>
	.tent_alert {
		background-color: indianred;
	}
	.tent_warning {
		background-color: orange;
	}
</style>
