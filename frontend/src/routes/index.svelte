<script lang="ts">
	import { apiGetParticipants } from '$lib/_apiParticipants';
	import type { cTentParticipant } from '$lib/_apiParticipants';

	import { Button, Container, Row, Col } from 'sveltestrap/src';
	import { onMount } from 'svelte';

	let participants: cTentParticipant[] = [];
	let birthDayParticipants: cTentParticipant[] = [];

	let avgAge = 0;
	let youngestParticipant = '';
	let eldestParticipant = '';

	$: avgAge = calculateAvgAge(participants);
	$: youngestParticipant = calculateYoungestParticipant(participants);
	$: eldestParticipant = calculateEldestParticipant(participants);

	onMount(() => {
		getParticipants();
	});

	function calculateYoungestParticipant(arg_participants: cTentParticipant[]): string {
		if (arg_participants.length == 0) {
			return '';
		}
		let loc_age = 100;
		let loc_index = 0;
		for (let i = 0; i < arg_participants.length; i++) {
			if (arg_participants[i].age < loc_age) {
				loc_age = arg_participants[i].age;
				loc_index = i;
			}
		}
		return (
			arg_participants[loc_index].getFullname() +
			' (' +
			arg_participants[loc_index].getAgeTwoDecimal() +
			')'
		);
	}
	function calculateEldestParticipant(arg_participants: cTentParticipant[]): string {
		if (arg_participants.length == 0) {
			return '';
		}
		let loc_age = 0;
		let loc_index = 0;
		for (let i = 0; i < arg_participants.length; i++) {
			if (arg_participants[i].age > loc_age) {
				loc_age = arg_participants[i].age;
				loc_index = i;
			}
		}
		return (
			arg_participants[loc_index].getFullname() +
			' (' +
			arg_participants[loc_index].getAgeTwoDecimal() +
			')'
		);
	}

	function calculateAvgAge(arg_participants: cTentParticipant[]): number {
		if (arg_participants.length == 0) {
			return 0;
		}
		let ageSum = 0;
		for (let i = 0; i < arg_participants.length; i++) {
			ageSum += arg_participants[i].age;
		}
		return Math.round((ageSum / arg_participants.length) * 100) / 100;
	}

	async function getParticipants() {
		participants = await apiGetParticipants();

		//parse bithday
		for (let i = 0; i < participants.length; i++) {
			const [day, month, year] = participants[i].birthdate.split('.');
			const beginZlDate = new Date(2022, 7, 5);
			const endZlDate = new Date(2022, 7, 12);
			const birthDate = new Date(2022, +month - 1, +day); //(0 = January to 11 = December)

			if (beginZlDate <= birthDate && endZlDate >= birthDate) {
				birthDayParticipants[birthDayParticipants.length] = participants[i];
			}
		}
	}
</script>

<svelte:head>
	<title>Home</title>
</svelte:head>
<div style="margin-top: 80px; margin-left: 10px;">
	<Row>
		<Col><h1>Hi Lale</h1></Col>
		<Col>
			<h1>Participants Statistics:</h1>
			<ul>
				<li>average age: {avgAge}</li>
				<li>youngest participant age: {youngestParticipant}</li>
				<li>eldest participant: {eldestParticipant}</li>
			</ul>
		</Col>
		<Col
			><h1>Birthday kids</h1>
			<ul>
				{#each birthDayParticipants as participant}
					<li>{participant.getFullname()} ({participant.birthdate})</li>
				{/each}
			</ul>
		</Col>
	</Row>
</div>
