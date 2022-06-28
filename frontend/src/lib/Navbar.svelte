<script lang="ts">
	import {
		Collapse,
		Navbar,
		NavbarToggler,
		NavbarBrand,
		Nav,
		NavItem,
		NavLink
	} from 'sveltestrap/src';

	interface NavEntry {
		label: string;
		route: string;
	}

	let navEntries: NavEntry[] = [
		{ label: 'Home', route: '/' },
		{ label: 'Stübis', route: '/participants' },
		{ label: 'Zelteinteilung', route: '/tentAllocation' }
	];

	let isOpen = false;

	function handleUpdate(event: CustomEvent) {
		isOpen = event.detail.isOpen;
	}
</script>

<Navbar color="dark" dark expand="md" fixed="top" height="50px">
	<NavbarBrand href="/">LaleControl</NavbarBrand>
	<NavbarToggler on:click={() => (isOpen = !isOpen)} />
	<Collapse {isOpen} navbar expand="md" on:update={handleUpdate}>
		<Nav class="ms-auto" navbar>
			{#each navEntries as entry}
				<NavItem>
					<NavLink href={entry.route}>{entry.label}</NavLink>
				</NavItem>
			{/each}
		</Nav>
	</Collapse>
</Navbar>
