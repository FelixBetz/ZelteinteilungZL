<script lang="ts">
	import { TabContent, TabPane, Input, Button } from 'sveltestrap/src';
	import CsvUpload from '$lib/CsvUpload.svelte';

	let result = null;

	let csvFile: File;
	async function onSubmit(e) {
		const formData = new FormData(e.target);

		formData.append('csvFile', csvFile);
		//return;
		const res = await fetch('http://127.0.0.1:8080/api/test', {
			method: 'POST',
			body: formData
		});

		const json = await res.json();
		result = JSON.stringify(json);
		console.log(result);
	}

	let csvColumns: string[] = [];
</script>

<ul>
	<li>Massenmail von CSV</li>
	<li>Personalisierte Mail aus CSV Liste => persönliche Felder konfigurierbar</li>
	<li>Personalisierte Mail aus CSV Liste mit Word Template</li>
	<ul>
		<li>BCC</li>
		<li>pdf oder docx</li>
	</ul>
</ul>
<CsvUpload bind:csvColumns bind:csvFile />
<ul>
	{#each csvColumns as column}
		<li>{column}</li>
	{/each}
</ul>

<form on:submit|preventDefault={onSubmit}>
	<div>
		<label for="subject">Subject:</label>
		<input type="text" id="subject" name="subject" value="" placeholder="enter subject" />
	</div>

	<Input name="isBcc" id="isBcc" type="checkbox" label="Send as bcc" />

	<Button type="submit" color="primary">Submit</Button>

	<TabContent>
		<TabPane tab="Massenmail" tabId="massMail" active>
			<Input type="textarea" name="mailText" id="exampleText" rows={10} />
		</TabPane>
		<TabPane tab="Personalisierte Mail" tabId="personal">
			<h2>Bravo</h2>
		</TabPane>
		<TabPane tab="Personalisierte Mail (Word Template)" tabId="Charlie">
			<h2>Charlie</h2>
		</TabPane>
	</TabContent>
</form>
