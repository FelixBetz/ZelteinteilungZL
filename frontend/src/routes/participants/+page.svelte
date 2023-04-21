<script lang="ts">
	import { apiGetMaps, apiGetParticipants, apiPostParticipants } from '$lib/_apiParticipants';

	import type { cTentParticipant, ZipCodes } from '$lib/_apiParticipants';

	import { Table, Button, Input, Row, Col } from 'sveltestrap/src';
	import { onMount } from 'svelte';
	import NavbarParticipants from '$lib/NavbarParticipants.svelte';

	import { boolSort, textSort, numberSort } from '$lib/sort';

	enum IColumn {
		id = 'id',
		paid = 'paid',
		firstName = 'Vorname',
		lastName = 'Nachname',
		zipCode = 'PLZ',
		village = 'Ort',
		age = 'Alter',
		friends = ' Freunde'
	}

	let columns = [
		IColumn.id,
		IColumn.paid,
		IColumn.firstName,
		IColumn.lastName,
		IColumn.zipCode,
		IColumn.village,
		IColumn.age,
		IColumn.friends
	];
	let participants: cTentParticipant[] = [];
	let filterdParticipants: cTentParticipant[] = [];
	let serachString = '';
	let sortBy = { col: IColumn, ascending: true };

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

	function clickSortTable(column: IColumn) {
		let sort = (a: cTentParticipant, b: cTentParticipant) => {
			switch (column) {
				case IColumn.id:
					return numberSort(a.identifier, b.identifier, sortBy.ascending);
				case IColumn.paid:
					return boolSort(a.paid, b.paid, sortBy.ascending);
				case IColumn.zipCode:
					return numberSort(a.zipcode, b.zipcode, sortBy.ascending);
				case IColumn.age:
					return numberSort(a.age, b.age, sortBy.ascending);
				case IColumn.firstName:
					return textSort(a.firstname, b.firstname, sortBy.ascending);
				case IColumn.lastName:
					return textSort(a.lastname, b.lastname, sortBy.ascending);
				case IColumn.village:
					return textSort(a.village, b.village, sortBy.ascending);
				default:
					return 0;
			}
		};

		filterdParticipants = filterdParticipants.sort(sort);
		sortBy.ascending = !sortBy.ascending;
	}

	onMount(() => {
		getParticipants();
	});

	function searchParticipant(p: cTentParticipant) {
		return (
			p.firstname.toLowerCase().includes(serachString.toLowerCase()) ||
			p.lastname.toLowerCase().includes(serachString.toLowerCase()) ||
			p.zipcode.toString().toLowerCase().includes(serachString.toLowerCase()) ||
			p.village.toLowerCase().includes(serachString.toLowerCase())
		);
	}

	function onSearchParticipant() {
		filterdParticipants = participants.filter((p: cTentParticipant) => searchParticipant(p));
	}

	async function getParticipants() {
		participants = await apiGetParticipants();
		filterdParticipants = participants;
		filterdParticipants = participants.filter((p: cTentParticipant) => searchParticipant(p));
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

<Input
	bind:value={serachString}
	on:keyup={onSearchParticipant}
	type="search"
	placeholder="Search"
	class="ms-auto w-auto"
	style="margin-right: 20px"
/>

<Table striped data-toggle="table" data-search="true" data-strict-search="true">
	<thead>
		<tr>
			{#each columns as column}
				<th on:click={() => clickSortTable(column)}>{column}</th>
			{/each}
		</tr>
	</thead>
	<tbody>
		{#each filterdParticipants as participant}
			<tr>
				<th scope="row">
					<a target="_blank" href={'/participant/' + participant.identifier}>
						{participant.identifier}
					</a>
				</th>
				<td><Input type="checkbox" bind:checked={participant.paid} /></td>
				<td>{participant.firstname}</td>
				<td>{participant.lastname}</td>
				<td>{participant.zipcode}</td>
				<td>{participant.village}</td>
				<td>{participant.getAgeTwoDecimal()}</td>
				<td>{participant.friends}</td>
			</tr>
		{/each}
	</tbody>
</Table>
