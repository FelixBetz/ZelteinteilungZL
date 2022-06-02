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
			<NavItem>
				<NavLink href="/">Home</NavLink>
			</NavItem>
			<NavItem>
				<NavLink href="/participants">Stübis</NavLink>
			</NavItem>
			<NavItem>
				<NavLink href="/tentAllocation">Zelteinteilung</NavLink>
			</NavItem>
			<NavItem>
				<NavLink href="/mailing">Mailing</NavLink>
			</NavItem>
		</Nav>
	</Collapse>
</Navbar>
