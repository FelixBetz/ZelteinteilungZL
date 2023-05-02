<script lang="ts">
	import { boolSort, numberSort, type IColumn, stringSort } from '$lib/sort';

	let serachString = '';

	export let data: any[] = [];
	export let filterdData: any[] = [];
	export let columns: IColumn[] = [];
	export let searchColumns: string[] = [];

	$: filterdData = data.filter((p) => search(p));

	function search(p: { [x: string]: { toString: () => string } }): boolean {
		for (let idx = 0; idx < searchColumns.length; idx++) {
			if (
				p[searchColumns[idx]].toString().toLowerCase().includes(serachString.trim().toLowerCase())
			) {
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

<div class="hstack">
	<div class="">
		<div class="">
			<strong>Angezeigte Elemente: </strong>
			{filterdData.length}
		</div>
	</div>
	<div class="ms-auto">
		<div class="input-group">
			<input
				class="form-control border-end-0 border ms-auto w-auto form-control bg-dark text-white"
				id="exampleFormControlInput2"
				bind:value={serachString}
				on:keyup={onSearch}
				type="search"
				placeholder="Search"
			/>
			<span class="input-group-append">
				<button
					class="btn btn-dark border-start-0 border rounded-0 rounded-end"
					type="button"
					on:click={() => {
						serachString = '';
						onSearch();
					}}
				>
					<i class="bi bi-x-circle" />
				</button>
			</span>
		</div>
	</div>
</div>
<table class="table table-striped table-dark">
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
							<input type="checkbox" class="form-check-input" bind:checked={d[col.key]} />

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
</table>
