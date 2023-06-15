<script lang="ts">
	import Navbar from '$lib/Navbar.svelte';

	import 'bootstrap/dist/css/bootstrap.min.css';
	import 'bootstrap-icons/font/bootstrap-icons.min.css';
	import '../app.css';
</script>

<Navbar />

<main>
	<slot />
</main>

<style>
	main {
		margin-top: 50px;
		padding-top: 10px;
	}
</style>
