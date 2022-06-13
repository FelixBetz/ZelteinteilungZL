<script lang="ts">
	import { apiGetMaps, apiGetParticipants, baseUrl } from '$lib/_apiParticipants';

	import type { cTentParticipant, ZipCodes } from '$lib/_apiParticipants';

	import { Table, Button, Input, TabContent, TabPane } from 'sveltestrap/src';
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
	let participants: cTentParticipant[] = [];
	let filterdParticipants: cTentParticipant[] = [];
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
		let sort = (a: cTentParticipant, b: cTentParticipant) => {
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

<TabContent pills style="margin:10px;">
	<TabPane tabId="table" tab="table" active>
		<div style="margin-top: 10px;" />
		<Button on:click={getParticipants} color="secondary">Refresh</Button>
		<Button on:click={getMaps} color="secondary">generate Maps</Button>

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
						<th scope="row">{participant.id}</th>
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
	</TabPane>
	<TabPane tabId="heatmap" tab="Heatmap">
		<embed
			on:click={() => console.log('asdfasf')}
			id="id_heatmap"
			title="heatmap"
			src={baseUrl + '/maps/heatmap.html'}
			style="width:100%; height: calc(100vh - 125px) !important; "
		/>
	</TabPane>
	<TabPane tabId="markermap" tab="markermap" on:clic>
		<embed
			title="markermap"
			src={baseUrl + '/maps/markermap.html'}
			style="width:100%; height: calc(100vh - 125px) !important; "
		/>
	</TabPane>
</TabContent>
