<script lang="ts">
	import { Table, Input } from 'sveltestrap/src';
	import { boolSort, textSort, numberSort } from '$lib/sort';
	import type { cTentParticipant } from './_apiParticipants';

	let serachString = '';

	export let data: cTentParticipant[] = [];
	export let filterdData: cTentParticipant[] = []; // todo

	$: filterdData = data.filter((p: cTentParticipant) => searchParticipant(p));

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
	let sortBy = { col: IColumn, ascending: true };

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

	function searchParticipant(p: cTentParticipant) {
		return (
			p.firstname.toLowerCase().includes(serachString.toLowerCase()) ||
			p.lastname.toLowerCase().includes(serachString.toLowerCase()) ||
			p.zipcode.toString().toLowerCase().includes(serachString.toLowerCase()) ||
			p.village.toLowerCase().includes(serachString.toLowerCase())
		);
	}

	function onSearchParticipant() {
		filterdData = data.filter((p: cTentParticipant) => searchParticipant(p));
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

		filterdData = filterdData.sort(sort);
		sortBy.ascending = !sortBy.ascending;
	}
</script>

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
		{#each filterdData as participant}
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
