<script lang="ts">
	import type { cTentParticipant } from '$lib/api/apiParticipants';
	export let participant: cTentParticipant;
</script>

<div class="col-sm-6" style="padding: 5px">
	<div class="card" style="padding:5px; background-color:lightgray" draggable="true" on:dragstart>
		<h5 class="card-title">
			{participant.getFullname()}
			({participant.getAgeTwoDecimal()})
		</h5>
	</div>
</div>
