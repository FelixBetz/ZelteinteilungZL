<script lang="ts">
	import Navbar from '$lib/Navbar.svelte';
	import { Styles } from 'sveltestrap';

	import '../app.css';
</script>

<Styles />
<Navbar />

<main style="margin-top: 50px">
	<slot />
</main>

<!-- todo
<footer>
	<p>visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to learn SvelteKit</p>
</footer>-->
