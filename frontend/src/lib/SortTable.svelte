<script lang="ts">
	import { Table, Input } from 'sveltestrap/src';
	import { boolSort, numberSort, type IColumn, stringSort } from '$lib/sort';

	let serachString = '';

	export let data: any[] = [];
	export let filterdData: any[] = [];
	export let columns: IColumn[] = [];
	export let searchColumns: string[] = [];

	$: filterdData = data.filter((p) => search(p));

	function search(p: { [x: string]: { toString: () => string } }): boolean {
		for (let idx = 0; idx < searchColumns.length; idx++) {
			if (p[searchColumns[idx]].toString().toLowerCase().includes(serachString.toLowerCase())) {
				return true;
			}
		}
		return false;
	}

	function onSearch() {
		filterdData = data.filter((p) => search(p));
	}

	function clickSortTable(column: IColumn) {
		let sortFunc = (a: { [x: string]: string }, b: { [x: string]: string }) => {
			switch (typeof a[column.key]) {
				case 'boolean':
					return boolSort(Boolean(a[column.key]), Boolean(b[column.key]), column.ascending);
				case 'number':
					return numberSort(Number(a[column.key]), Number(b[column.key]), column.ascending);
				case 'string':
					return stringSort(a[column.key], b[column.key], column.ascending);
				default:
					return 0;
			}
		};

		filterdData = filterdData.sort(sortFunc);
		column.ascending = !column.ascending;
	}
</script>

<Input
	bind:value={serachString}
	on:keyup={onSearch}
	type="search"
	placeholder="Search"
	class="ms-auto w-auto"
	style="margin-right: 20px"
/>

<Table striped={true} dark>
	<thead>
		<tr>
			{#each columns as column}
				<th on:click={() => clickSortTable(column)}>{column.label}</th>
			{/each}
		</tr>
	</thead>
	<tbody>
		{#each filterdData as d}
			<tr>
				{#each columns as col}
					<td>
						<!--Checkbox of boolean-->
						{#if typeof d[col.key] == 'boolean'}
							<Input type="checkbox" bind:checked={d[col.key]} />

							<!--column has link-->
						{:else if col.link != undefined}
							<a target="_blank" href={col.link + d[col.key]}>
								{d[col.key]}
							</a>
						{:else if col.displayCallback != undefined}
							{col.displayCallback(d[col.key])}
						{:else}
							{d[col.key]}
						{/if}
					</td>
				{/each}
			</tr>
		{/each}
	</tbody>
</Table>
