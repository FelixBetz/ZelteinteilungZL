<script lang="ts">
	import Navbar from '$lib/Navbar.svelte';
	import { Styles } from 'sveltestrap';

	import '../app.css';
</script>

<Styles />
<Navbar />

<main>
	<slot />
</main>

<style>
	main {
		margin-top: 50px;
	}
</style>
