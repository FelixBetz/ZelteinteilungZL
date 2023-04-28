<script lang="ts">
	import { apiGetMaps, apiGetParticipants, apiPostParticipants } from '$lib/_apiParticipants';

	import type { cTentParticipant, ZipCodes } from '$lib/_apiParticipants';

	import { onMount } from 'svelte';
	import NavbarParticipants from '$lib/NavbarParticipants.svelte';

	import SortTable from '$lib/SortTable.svelte';

	import type { IColumn } from '$lib/sort';
	import { displayTentString, getStrTwoDecimal } from '$lib/helpers';

	let participants: cTentParticipant[] = [];
	let filterdParticipants: cTentParticipant[] = [];

	function getFriendsString(friends: string[]) {
		return friends.filter((friend) => friend != '').join(', ');
	}

	const columns: IColumn[] = [
		{ label: 'id', key: 'identifier', ascending: true, link: '/participant/' },
		{ label: 'paid', key: 'paid', ascending: true },
		{ label: 'Zelt', key: 'tent', ascending: true, displayCallback: displayTentString },
		{ label: 'firstName', key: 'firstname', ascending: true },
		{ label: 'lastName', key: 'lastname', ascending: true },
		{ label: 'zipCode', key: 'zipcode', ascending: true },
		{ label: 'village', key: 'village', ascending: true },
		{ label: 'age', key: 'age', ascending: true, displayCallback: getStrTwoDecimal },
		{ label: 'friends', key: 'friends', ascending: true, displayCallback: getFriendsString }
	];
	const searchColumns: string[] = ['firstname', 'lastname', 'zipcode', 'village'];

	let avgAge = 0;
	$: avgAge = calculateAvgAge(participants);

	function calculateAvgAge(arg_participants: cTentParticipant[]): number {
		if (arg_participants.length == 0) {
			return 0;
		}
		let ageSum = 0;
		for (let i = 0; i < arg_participants.length; i++) {
			ageSum += arg_participants[i].age;
		}
		return Math.round((ageSum / arg_participants.length) * 100) / 100;
	}

	onMount(() => {
		getParticipants();
	});

	async function getParticipants() {
		participants = await apiGetParticipants();
		filterdParticipants = participants;
	}

	async function saveParticipants() {
		participants = await apiPostParticipants(participants);
	}

	async function getMaps() {
		let zipCodes: ZipCodes[] = [];

		for (let i = 0; i < filterdParticipants.length; i++) {
			zipCodes.push({
				zipCode: filterdParticipants[i].zipcode,
				location: filterdParticipants[i].village
			});
		}

		await apiGetMaps(zipCodes);
	}
</script>

<svelte:head>
	<title>Stübis</title>
</svelte:head>

<NavbarParticipants />
<div class="container-fluid">
	<div class="row">
		<div class="col-sm-3">
			<div class="btn btn-warning" on:click={getParticipants} on:keydown={getParticipants}>
				Refresh
			</div>

			<div class="btn btn-primary" on:click={saveParticipants} on:keydown={saveParticipants}>
				Save
			</div>

			<div class="btn btn-primary" on:click={getMaps} on:keydown={getMaps}>generate Maps</div>
		</div>
		<div class="col-sm-auto"><strong>Anzahl Teilnehmer:</strong> {participants.length}</div>
		<div class="col-sm-auto"><strong>Durchschnittsalter: </strong> {avgAge}</div>
	</div>

	<SortTable data={participants} bind:filterdData={filterdParticipants} {columns} {searchColumns} />
</div>
