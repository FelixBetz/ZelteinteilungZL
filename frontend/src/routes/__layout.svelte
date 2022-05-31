<script lang="ts">
	import Navbar from '$lib/Navbar.svelte';

	import '../app.css';
</script>

<Navbar />

<main>
	<slot />
</main>

<!-- todo
<footer>
	<p>visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to learn SvelteKit</p>
</footer>-->
