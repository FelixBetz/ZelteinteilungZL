<script lang="ts">
	import { FormGroup, Label, Input } from 'sveltestrap/src';

	export let csvColumns: string[] = [];
	export let csvFile: File;

	const onFileSelected = (e: any) => {
		csvFile = e.target.files[0];
		let reader = new FileReader();
		reader.readAsText(csvFile);

		reader.onload = () => {
			let res = reader.result;

			let firstline = '';
			if (typeof res === 'string') {
				firstline = res.split('\r\n')[0];
			}
			csvColumns = [];

			let splittedFirstLine = firstline.split(';');
			for (let i = 0; i < splittedFirstLine.length; i++) {
				csvColumns[csvColumns.length] = splittedFirstLine[i];
			}
		};
	};
</script>

<FormGroup>
	<Label for="file"
		>CSV File (CSV File muss spalte mit dem genauem Namen &quot;mail&quot; enthalten)</Label
	>
	<Input
		type="file"
		name="file"
		id="exampleFile"
		on:change={(e) => onFileSelected(e)}
		accept=".csv"
	/>
</FormGroup>
