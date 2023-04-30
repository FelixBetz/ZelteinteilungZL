<script lang="ts">
	interface NavEntry {
		label: string;
		route: string;
	}
	let activeIdx = 0;

	let navEntries: NavEntry[] = [
		{ label: 'Home', route: '/' },
		{ label: 'Stübis', route: '/participants' },
		{ label: 'Team', route: '/team' },
		{ label: 'Zelteinteilung', route: '/tentAllocation' },
		{ label: 'Graph', route: '/graph' },
		{ label: 'Logs', route: '/logs' },
		{ label: 'Configs', route: '/configs' }
	];

	let isOpen = false;
</script>

<nav class="navbar navbar-dark navbar-expand-md bg-dark bg-gradient fixed-top" style="height: 50px">
	<div class="container-fluid">
		<a class="navbar-brand" href="/">
			<img src="favicon.png" class="img-fluid" style="height: 50px" alt="..." />
			LaleControl
		</a>

		<button
			class="navbar-toggler"
			type="button"
			data-bs-toggle="offcanvas"
			data-bs-target="#offcanvasDarkNavbar"
			aria-controls="offcanvasDarkNavbar"
			on:click={() => (isOpen = !isOpen)}
		>
			<span class="navbar-toggler-icon" />
		</button>

		<div class="{isOpen ? ' ' : 'collapse '} navbar-collapse navbar-expand-md">
			<ul class="navbar-nav ms-auto">
				{#each navEntries as entry, i}
					<li class="nav-item">
						<a
							class="nav-link {i == activeIdx ? ' active' : ''}"
							href={entry.route}
							on:click={() => (activeIdx = i)}
						>
							{entry.label}
						</a>
					</li>
				{/each}
			</ul>
		</div>
	</div>
</nav>
