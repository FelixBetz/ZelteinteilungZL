<script lang="ts">
	import { Col, CardTitle } from 'sveltestrap/src';
	import type { cTentParticipant } from '$lib/_apiParticipants';

	export let participant: cTentParticipant;
</script>

<Col sm="6" style="padding: 5px">
	<div class="card" style="padding:5px; background-color:lightgray" draggable="true" on:dragstart>
		<CardTitle>
			{participant.getFullname()}
			({participant.getAgeOneDecimal()})
		</CardTitle>
	</div>
</Col>
