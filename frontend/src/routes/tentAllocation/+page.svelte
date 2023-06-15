<script lang="ts">
	import { apiGetTentLeader, type cTentLeader } from '$lib/api/apiTentleader';
	import {
		apiGetParticipants,
		apiPostParticipants,
		type cTentParticipant
	} from '$lib/api/apiParticipants';

	import { onMount } from 'svelte';
	import TentParticipant from '$lib/TentParticipant.svelte';
	import { type Configs, apiGetConfigs } from '$lib/api/apiConfig';
	import { getStrTwoDecimal } from '$lib/helpers';
	let isPostRequest = false;
	let configs: Configs = { numTents: 9999, zlStart: '1970-08-12', calenderUrl: '' };

	interface Item {
		id: number;
		isShow: boolean;
	}
	interface Basket {
		name: string;
		items: Item[];
		tentLeaders: string[];
		age: number;
	}

	let baskets: Basket[] = [
		{
			name: 'Backlog',
			items: [],
			tentLeaders: [],
			age: 0
		}
	];

	function clearBaskets() {
		baskets = [
			{
				name: 'Backlog',
				items: [],
				tentLeaders: [],
				age: 0
			}
		];
		for (let i = 0; i < configs.numTents; i++) {
			baskets.push({ name: 'Zelt ' + (i + 1), items: [], tentLeaders: [], age: 0 });
		}
	}

	let participants: cTentParticipant[] = [];

	$: calcAvgAge(baskets);

	function calcAvgAge(pBaskets: Basket[]) {
		pBaskets.forEach((b) => {
			let avgAge = 0;
			b.items.forEach((p) => {
				avgAge += participants[p.id].age;
			});
			b.age = avgAge / b.items.length;
		});
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

	function compareBasketByAge(a: Item, b: Item) {
		return compareByAge(participants[a.id], participants[b.id]);
	}
	let hoveringOverBasket: string;

	function distributePartiscipantsToBaskets(
		pParticipants: cTentParticipant[],
		pTentLeaders: cTentLeader[]
	) {
		clearBaskets();
		participants = pParticipants.sort(compareByAge);

		//add participants to baskets
		for (let i = 0; i < participants.length; i++) {
			let tentNumber = participants[i].tent;
			if (tentNumber <= configs.numTents) {
				baskets[tentNumber].items[baskets[tentNumber].items.length] = { id: i, isShow: true };
			} else {
				baskets[0].items[baskets[0].items.length] = { id: i, isShow: true };
			}
		}

		//add tent leaders to baskets
		for (let i = 0; i < pTentLeaders.length; i++) {
			let tentNumber = pTentLeaders[i].tent;
			if (tentNumber > 0 && tentNumber <= configs.numTents) {
				baskets[tentNumber].tentLeaders[baskets[tentNumber].tentLeaders.length] =
					pTentLeaders[i].firstname + ' ' + pTentLeaders[i].lastname;
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
		isPostRequest = true;
		for (let i = 0; i < baskets.length; i++) {
			for (let k = 0; k < baskets[i].items.length; k++) {
				let id = baskets[i].items[k].id;
				if (i == 0) {
					participants[id].tent = 9999;
				} else {
					participants[id].tent = i;
				}
			}
		}
		let unsortedParticipants = await apiPostParticipants(participants)
			.then((res) => {
				return res;
			})
			.catch((error) => {
				console.error(error);
				return [];
			});
		let tentLeaders = await apiGetTentLeader();
		distributePartiscipantsToBaskets(unsortedParticipants, tentLeaders);
		isPostRequest = false;
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

	let searchString = '';

	function onBasketChange(pBasket: Basket, pSearchString: string) {
		pBasket.items.forEach((item) => {
			let itemName = participants[item.id].getFullname().toLowerCase();
			item.isShow = itemName.includes(pSearchString.trim().toLowerCase());
		});

		pBasket.items.sort(compareBasketByAge);
		return pBasket;
	}

	let filterdBacklog: Basket;
	$: filterdBacklog = onBasketChange(baskets[0], searchString);
</script>

<svelte:head>
	<title>Zelteinteilung</title>
</svelte:head>
<div class="container-fluid">
	<div class="row">
		<div class="col-sm-12">
			<button
				class="btn btn-primary w-100"
				type="button"
				on:click={saveParticipants}
				on:keydown={saveParticipants}
			>
				Save
				{#if isPostRequest}
					<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" />
				{/if}
			</button>
		</div>
	</div>
	<div class="row gx-3 gy-0 mt-3">
		<div class="col-sm-8">
			<div class="row gx-3 gy-3">
				{#each baskets as b, basketIndex}
					{#if basketIndex > 0}
						<div class="col-sm-6">
							<div
								class="card position-relative shadow-lg"
								class:hovering={hoveringOverBasket === b.name}
								on:dragenter={() => (hoveringOverBasket = b.name)}
								on:dragleave={() => (hoveringOverBasket = '')}
								on:drop={(event) => drop(event, basketIndex)}
								on:dragover={(event) => {
									if (b.items.length <= 6) {
										event.preventDefault();
									}
								}}
								style="border: 1px solid black; "
							>
								<div class="text-right position-absolute top-0 end-0 me-2">
									<i>
										Ø - Alter: {getStrTwoDecimal(b.age)}
									</i>
								</div>
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
											<TentParticipant
												participant={participants[item.id]}
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
				class="card shadow-lg"
				class:hovering={hoveringOverBasket === baskets[0].name}
				on:dragenter={() => (hoveringOverBasket = baskets[0].name)}
				on:dragleave={() => (hoveringOverBasket = '')}
				on:drop={(event) => drop(event, 0)}
				on:dragover={(event) => event.preventDefault()}
			>
				<div class="card-header">
					<div class="d-flex justify-content-between">
						<h5 class="card-title">Backlog</h5>
						<div>
							<div class="input-group ms-auto">
								<input
									class="form-control border-end-0 border form-control"
									id="exampleFormControlInput2"
									bind:value={searchString}
									type="search"
									placeholder="Search"
								/>
								<span class="input-group-append">
									<button
										class="btn btn-light border-start-0 border rounded-0 rounded-end"
										type="button"
										on:click={() => {
											searchString = '';
										}}
									>
										<i class="bi bi-x-circle" />
									</button>
								</span>
							</div>
						</div>
					</div>
				</div>

				<div class="card-body">
					<div class="row">
						{#each filterdBacklog.items as item, itemIndex}
							{#if item.isShow}
								<TentParticipant
									participant={participants[item.id]}
									on:dragstart={(event) => dragStart(event, 0, itemIndex)}
								/>
							{/if}
						{/each}
					</div>
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
