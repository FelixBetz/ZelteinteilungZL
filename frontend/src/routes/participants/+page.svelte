<script lang="ts">
	import { apiGetMaps, type ZipCodes } from '$lib/api/apiGraphs';

	import { onMount } from 'svelte';
	import NavbarParticipants from '$lib/NavbarParticipants.svelte';

	import SortTable from '$lib/SortTable.svelte';

	import type { IColumn } from '$lib/sort';
	import { displayTentString, getStrTwoDecimal } from '$lib/helpers';
	import {
		apiGetParticipants,
		apiPostParticipants,
		cTentParticipant
	} from '$lib/api/apiParticipants';

	let participants: cTentParticipant[] = [];
	let filterdParticipants: cTentParticipant[] = [];

	interface Warning {
		message: string;
		isOpen: boolean;
	}

	let warnings: Warning[] = [];

	let isMapRequest = false;
	let isPostRequest = false;

	function getFriendsString(friends: string[]) {
		return friends.filter((friend) => friend != '').join(', ');
	}

	const columns: IColumn[] = [
		{ label: 'id', key: 'identifier', ascending: true, link: '/participant/' },
		{ label: 'paid', key: 'paid', ascending: true },
		{ label: 'Zelt', key: 'tent', ascending: true, displayCallback: displayTentString },
		{ label: 'Vorname', key: 'firstname', ascending: true },
		{ label: 'Nachname', key: 'lastname', ascending: true },
		{ label: 'PLZ', key: 'zipcode', ascending: true },
		{ label: 'Ort', key: 'village', ascending: true },
		{ label: 'Alter', key: 'age', ascending: true, displayCallback: getStrTwoDecimal },
		{ label: 'Freunde', key: 'friends', ascending: true, displayCallback: getFriendsString },
		{ label: 'Sonstiges', key: 'other', ascending: true }
	];
	const searchColumns: string[] = ['firstname', 'lastname', 'zipcode', 'village'];

	let avgAge = 0;
	$: avgAge = calculateAvgAge(participants);

	function calculateAvgAge(pParticipants: cTentParticipant[]): number {
		if (pParticipants.length == 0) {
			return 0;
		}
		let ageSum = 0;
		for (let i = 0; i < pParticipants.length; i++) {
			ageSum += pParticipants[i].age;
		}
		return Math.round((ageSum / pParticipants.length) * 100) / 100;
	}

	onMount(() => {
		getParticipants();
	});

	async function getParticipants() {
		participants = [];
		participants = await apiGetParticipants();
		filterdParticipants = participants;
	}

	async function saveParticipants() {
		isPostRequest = true;
		participants = await apiPostParticipants(participants)
			.then((res) => {
				isPostRequest = false;
				return res;
			})
			.catch((error) => {
				console.error(error);
				return [];
			});
	}

	async function getMaps() {
		isMapRequest = true;
		let zipCodes: ZipCodes[] = [];

		for (let i = 0; i < filterdParticipants.length; i++) {
			let p = filterdParticipants[i];
			zipCodes.push({
				zipCode: p.zipcode,
				location: p.village,
				addressString: p.street + ', ' + p.zipcode + ' ' + p.village + ', DE',
				name: p.getFullname()
			});
		}

		await apiGetMaps(zipCodes).then((res) => {
			res.forEach((warning) => {
				warnings[warnings.length] = { isOpen: true, message: warning };
			});
			isMapRequest = false;
		});
	}
</script>

<svelte:head>
	<title>Stübis</title>
</svelte:head>

<!--Toasts-->
{#if warnings.length > 0 && warnings.reduce((acc, val) => acc || val.isOpen, false)}
	<div class="row m-2">
		{#each warnings as warning}
			{#if warning.isOpen}
				<div class=" p-1 col-sm-auto">
					<div class="position-relativ alert alert-warning" role="alert">
						<div class="m-0 p-0">
							<i class="bi bi-exclamation-triangle" />
							{warning.message}
							<i
								class="bi bi-x-lg position-absolute top-0 end-0 me-1"
								on:keydown={() => (warning.isOpen = false)}
								on:click={() => (warning.isOpen = false)}
							/>
						</div>
					</div>
				</div>
			{/if}
		{/each}
	</div>
{/if}
<!--NavbarParticipants-->
<NavbarParticipants />
<!--Table-->
<div class="container-fluid">
	<div class="row">
		<div class="col-sm-3">
			<div class="btn btn-warning" on:click={getParticipants} on:keydown={getParticipants}>
				Refresh
			</div>

			<button
				class="btn btn-primary"
				type="button"
				on:click={saveParticipants}
				on:keydown={saveParticipants}
			>
				Save
				{#if isPostRequest}
					<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" />
				{/if}
			</button>

			<button class="btn btn-primary" type="button" on:click={getMaps} on:keydown={getMaps}>
				generate Maps
				{#if isMapRequest}
					<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" />
				{/if}
			</button>
		</div>
		<div class="col-sm-auto"><strong>Anzahl Teilnehmer:</strong> {participants.length}</div>
		<div class="col-sm-auto"><strong>Durchschnittsalter: </strong> {avgAge}</div>
	</div>

	<SortTable data={participants} bind:filterdData={filterdParticipants} {columns} {searchColumns} />
</div>
