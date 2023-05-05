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
			<br />
			{#if showCsvColums}
				{#each csvColumns as column}
					<button
						type="button"
						class="btn btn-secondary"
						on:click={() => {
							const insertString = '[$$$' + column + '$$$]';
							editor.chain().insertContent(insertString).run();
						}}
					>
						{column}
					</button>
				{/each}
			{/if}
			<br />
			<button
				type="button"
				class="btn btn-secondary"
				on:click={() => {
					console.log('clear');
					editor.chain().clearContent().run();
				}}
				>Clear All
			</button>
		{/if}
	</CardHeader>
	<CardBody>
		<div bind:this={element} />
	</CardBody>
</Card>
