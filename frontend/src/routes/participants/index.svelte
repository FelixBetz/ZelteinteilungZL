<script lang="ts">
	import { apiGetParticipants } from './_apiParticipants';

	import type { Participant } from './_apiParticipants';

	import { Table, Button } from 'sveltestrap/src';
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
					break;
				case IColumn.zipCode:
					return numberSort(a.zipcode, b.zipcode);
					break;
				case IColumn.age:
					return numberSort(a.age, b.age);
					break;
				case IColumn.firstName:
					return textSort(a.firstname, b.firstname);
					break;
				case IColumn.lastName:
					return textSort(a.lastname, b.lastname);
					break;
				case IColumn.village:
					return textSort(a.village, b.village);
					break;
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

	//let participants:
	async function getParticipants() {
		participants = await apiGetParticipants();
	}
</script>

<Button on:click={getParticipants} color="primary">Refresh</Button>

<Table striped data-toggle="table" data-search="true" data-strict-search="true">
	<thead>
		<tr>
			{#each columns as column, i}
				<th on:click={() => clickSortTable(columns[i])}>{columns[i]}</th>
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
