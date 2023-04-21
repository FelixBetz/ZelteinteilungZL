<script lang="ts">
	import { apiGetMaps, apiGetParticipants, apiPostParticipants } from '$lib/_apiParticipants';

	import type { cTentParticipant, ZipCodes } from '$lib/_apiParticipants';

	import { Table, Button, Input, Row, Col } from 'sveltestrap/src';
	import { onMount } from 'svelte';
	import NavbarParticipants from '$lib/NavbarParticipants.svelte';

	import { boolSort, textSort, numberSort } from '$lib/sort';
	import SortTable from '$lib/SortTable.svelte';

	let participants: cTentParticipant[] = [];
	let filterdParticipants: cTentParticipant[] = [];

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

<Row style="padding: 10px;">
	<Col sm="3">
		<Button color="warning" on:click={getParticipants}>Refresh</Button>
		<Button color="primary" on:click={saveParticipants}>Save</Button>

		<Button on:click={getMaps} color="primary">generate Maps</Button>
	</Col>
	<Col sm="auto"><strong>Anzahl Teilnehmer:</strong> {participants.length}</Col>
	<Col sm="auto"><strong>Durchschnittsalter: </strong> {avgAge}</Col>
</Row>

<SortTable data={participants} bind:filterdData={filterdParticipants} />
