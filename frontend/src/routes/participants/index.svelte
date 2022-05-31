<script lang="ts">
	import { apiGetParticipants } from './_apiParticipants';

	import type { Participant } from './_apiParticipants';

	let participants: Participant[] = [];
	//let participants:
	async function getParticipants() {
		participants = await apiGetParticipants();
	}
</script>

<button on:click={getParticipants}>get</button>

{#each participants as participant}
	<div>
		{participant.firstname}&NonBreakingSpace;{participant.lastname}
	</div>
{/each}
