<script lang="ts">
	import { Col, CardTitle } from 'sveltestrap/src';
	import type { Participant } from '../participants/_apiParticipants';

	export let participant: Participant;
</script>

<Col sm="6" style="padding: 5px">
	<div class="card" style="padding:5px; background-color:lightgray" draggable="true" on:dragstart>
		<CardTitle>
			{participant.firstname}
			{participant.lastname} ({Math.round(10 * participant.age) / 10})
		</CardTitle>
	</div>
</Col>
