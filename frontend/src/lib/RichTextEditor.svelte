<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { Editor } from '@tiptap/core';
	import StarterKit from '@tiptap/starter-kit';
	import type { Level } from '@tiptap/extension-heading/src/heading';
	import { Card, CardHeader, CardTitle, CardBody } from 'sveltestrap/src';

	const headingsLevel: Level[] = [1, 2, 3, 4, 5, 6];

	export let style = '';
	export let showCsvColums = false;
	export let csvColumns: string[] = [];

	let element: HTMLDivElement;
	let editor: Editor;
	let selected = '';

	onMount(() => {
		editor = new Editor({
			element: element,
			extensions: [StarterKit],
			content: '',
			onTransaction: () => {
				// force re-render so `editor.isActive` works as expected
				editor = editor;
			}
		});
	});

	onDestroy(() => {
		if (editor) {
			editor.destroy();
		}
	});
	export function getHtmlString() {
		let htmlString = editor.getHTML();
		console.log(htmlString);
		return htmlString;
	}
</script>

<Card {style}>
	<CardHeader>
		<CardTitle>Mail Editor</CardTitle>

		{#if editor}
			{#each headingsLevel as hLevel}
				<button
					type="button"
					class="btn btn-secondary"
					on:click={() => editor.chain().focus().toggleHeading({ level: hLevel }).run()}
					class:active={editor.isActive('heading', { level: hLevel })}
				>
					H{hLevel}
				</button>
			{/each}

			<button
				type="button"
				class="btn btn-secondary"
				on:click={() => editor.chain().focus().setParagraph().run()}
				class:active={editor.isActive('paragraph')}
			>
				P
			</button>
			{#if showCsvColums}
				<button
					type="button"
					class="btn btn-secondary"
					on:click={() => {
						if (selected != '') {
							const insertString = '[$$$' + selected + '$$$]';
							editor.chain().insertContent(insertString).run();
						}
					}}
				>
					Insert CSV Col: {selected}
				</button>
				<select class="custom-select custom-select-lg mb-3" bind:value={selected}>
					{#each csvColumns as column}
						<option value={column}>
							{column}
						</option>
					{/each}
				</select>
				<ul>
					{#each csvColumns as column}
						<li>{column}</li>
					{/each}
				</ul>
			{/if}
		{/if}
	</CardHeader>
	<CardBody>
		<div bind:this={element} />
	</CardBody>
</Card>
