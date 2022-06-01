<script lang="ts">
	import { Col, CardTitle } from 'sveltestrap/src';

	export let participantName = '';
</script>

<Col sm="6" style="padding: 5px">
	<div class="card" style="padding:5px" draggable="true" on:dragstart>
		<CardTitle>
			{participantName}
		</CardTitle>
	</div>
</Col>
