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
		console.log(typeof event);
		console.log(event);
		console.log('tsd');

		isOpen = event.detail.isOpen;
	}
</script>

{isOpen}
<Navbar color="dark" dark expand="md">
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
		</Nav>
	</Collapse>
</Navbar>
