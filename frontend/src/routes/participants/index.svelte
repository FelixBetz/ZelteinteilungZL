<script lang="ts">
	import { apiGetParticipants } from './_apiParticipants';

	import type { Participant } from './_apiParticipants';

	import { Table, Button, Input } from 'sveltestrap/src';
	import { onMount } from 'svelte';

	enum IColumn {
		id = 'id',
		firstName = 'first name',
		lastName = 'last name',
		zipCode = 'zip code',
		village = 'village',
		age = 'age',
		friends = ' friends'
	}

	let columns = [
		IColumn.id,
		IColumn.firstName,
		IColumn.lastName,
		IColumn.zipCode,
		IColumn.village,
		IColumn.age,
		IColumn.friends
	];
	let participants: Participant[] = [];
	let serachString = '';
	let sortBy = { col: IColumn, ascending: true };

	function numberSort(a: number, b: number) {
		if (sortBy.ascending == true) {
			let temp = a;
			a = b;
			b = temp;
		}
		if (a >= b) {
			return 0;
		} else {
			return 1;
		}
	}

	function textSort(a: string, b: string) {
		if (sortBy.ascending == true) {
			let temp = a;
			a = b;
			b = temp;
		}
		if (a >= b) {
			return 0;
		} else {
			return 1;
		}
	}
	function clickSortTable(column: IColumn) {
		let sort = (a: Participant, b: Participant) => {
			switch (column) {
				case IColumn.id:
					return numberSort(a.id, b.id);
				case IColumn.zipCode:
					return numberSort(a.zipcode, b.zipcode);
				case IColumn.age:
					return numberSort(a.age, b.age);
				case IColumn.firstName:
					return textSort(a.firstname, b.firstname);
				case IColumn.lastName:
					return textSort(a.lastname, b.lastname);
				case IColumn.village:
					return textSort(a.village, b.village);
				default:
					return 0;
			}
		};

		participants = participants.sort(sort);
		sortBy.ascending = !sortBy.ascending;
	}

	onMount(() => {
		getParticipants();
	});

	function searchParticipant(p: Participant) {
		return (
			p.firstname.toLowerCase().includes(serachString.toLowerCase()) ||
			p.lastname.toLowerCase().includes(serachString.toLowerCase()) ||
			p.zipcode.toString().toLowerCase().includes(serachString.toLowerCase()) ||
			p.village.toLowerCase().includes(serachString.toLowerCase())
		);
	}

	async function getParticipants() {
		participants = await apiGetParticipants();
		participants = participants.filter((p: Participant) => searchParticipant(p));
	}
</script>

<Button on:click={getParticipants} color="primary">Refresh</Button>

<Input
	bind:value={serachString}
	on:input={getParticipants}
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
		{#each participants as participant}
			<tr>
				<th scope="row">{participant.id}</th>
				<td>{participant.firstname}</td>
				<td>{participant.lastname}</td>
				<td>{participant.zipcode}</td>
				<td>{participant.village}</td>
				<td>{Math.round(participant.age * 100) / 100}</td>
				<td>{participant.friends}</td>
			</tr>
		{/each}
	</tbody>
</Table>
