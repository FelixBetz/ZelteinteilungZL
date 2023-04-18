<script lang="ts">
	import { apiGetParticipants } from '$lib/_apiParticipants';
	import type { cTentParticipant } from '$lib/_apiParticipants';

	import { Row, Col } from 'sveltestrap/src';
	import { onMount } from 'svelte';
	import { NUM_TENTS } from '$lib/constants';

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
	interface TentAvg {
		avg: number;
		num: number;
		tentNumber: number;
	}

	let tentAvgAge: TentAvg[] = [];
	function calculateTentAvgAge() {
		tentAvgAge = [];
		for (let i = 0; i < NUM_TENTS; i++) {
			tentAvgAge[tentAvgAge.length] = { avg: 0, num: 0, tentNumber: i + 1 };
		}
		for (let i = 0; i < participants.length; i++) {
			let tentNumber = participants[i].tent;
			if (tentNumber <= NUM_TENTS) {
				tentAvgAge[tentNumber - 1].avg += participants[i].age;
				tentAvgAge[tentNumber - 1].num++;
			}
		}
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
			const [year, month, day] = participants[i].birthdate.split('-');

			const zlYear = 2023;

			const beginZlDate = new Date(zlYear, 7, 11); //todo
			const endZlDate = new Date(zlYear, 7, 18); //todo
			const birthDate = new Date(zlYear, +month - 1, +day); //(0 = January to 11 = December)

			if (beginZlDate <= birthDate && endZlDate >= birthDate) {
				birthDayParticipants[birthDayParticipants.length] = participants[i];
			}
		}

		calculateTentAvgAge();
	}
</script>

<svelte:head>
	<title>Home</title>
</svelte:head>
<div style="margin-top: 80px; margin-left: 10px;">
	<Row>
		<Col
			><h1>Durchschnittsalter Zelte:</h1>
			<ul>
				{#each tentAvgAge as avg}
					<li>Zelt {avg.tentNumber} ({Math.round((100 * avg.avg) / avg.num) / 100})</li>
				{/each}
			</ul>
		</Col>
		<Col>
			<h1>Participants Statistics:</h1>
			<ul>
				<li>number of participants: {participants.length}</li>
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
