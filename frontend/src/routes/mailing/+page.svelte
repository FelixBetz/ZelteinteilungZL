<script lang="ts">
	import { Input, Card, Button, Row, Col, Container } from 'sveltestrap/src';
	import CsvUpload from '$lib/CsvUpload.svelte';
	import RichTextEditor from '$lib/RichTextEditor.svelte';

	enum MailTypeId {
		massMail = 0,
		personalizedMail = 1,
		tempalteMail = 2
	}
	interface MailTypeSelect {
		id: MailTypeId;
		text: string;
	}
	let result = null;

	let editor: RichTextEditor;

	let answer = '';
	let mailType: MailTypeSelect[] = [
		{ id: 0, text: 'Massenmail' },
		{ id: 1, text: 'personalsierte Mail' },
		{ id: 2, text: 'Word Template' }
	];
	let selectedMailType: MailTypeSelect = mailType[0];

	let csvFile: File;
	async function onSubmit(e) {
		if (e.target !== null) {
			const formData = new FormData(e.target);
			formData.append('content', editor.getHtmlString());
			//todo formData.append('csvFile', csvFile);
			formData.append('mail', 'betz.felix@web.de');
			formData.append('mailType', selectedMailType.id.toString());

			/*const data: any = {};
			for (let field of formData) {
				const [key, value] = field;
				data[key] = value;
			}
			console.log(data);
			return;*/
			//todo
			const res = await fetch('http://127.0.0.1:8080/api/test', {
				method: 'POST',
				body: formData
			});

			const json = await res.json();
			result = JSON.stringify(json);
			console.log(result);
		}
	}

	let csvColumns: string[] = [];
</script>

<Container>
	<ul>
		<li>Personalisierte Mail aus CSV Liste mit Word Template</li>
		<ul>
			<li>pdf oder docx</li>
		</ul>
	</ul>
	<form on:submit|preventDefault={onSubmit}>
		<Card style="background-color: lightgray; margin: 10px padding: 10px;">
			<Row>
				<Col sm="2">
					<select
						class="custom-select custom-select-lg mb-3"
						bind:value={selectedMailType}
						on:change={() => (answer = '')}
					>
						{#each mailType as type}
							<option value={type}>
								{type.text}
							</option>
						{/each}
					</select>
				</Col>
				<Col sm="2">
					<label for="subject">Subject:</label>
					<input type="text" id="subject" name="subject" value="" placeholder="enter subject" />
				</Col>
				{#if selectedMailType.id == MailTypeId.massMail}
					<Col sm="2">
						<Input name="isBcc" id="isBcc" type="checkbox" label="Send as bcc" />
					</Col>
				{/if}
				<Col sm="6"><CsvUpload bind:csvColumns bind:csvFile /></Col>
			</Row>
		</Card>
		<Button type="submit" color="primary">Submit</Button>
	</form>

	<RichTextEditor
		bind:this={editor}
		style="margin-top: 100px;"
		showCsvColums={selectedMailType.id != MailTypeId.massMail}
		bind:csvColumns
	/>
</Container>
