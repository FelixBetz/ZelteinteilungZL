<script lang="ts">
	import {
		apiGetParticipants,
		apiGetTentLeader,
		apiGetLogs,
		type TentLeader,
		type cTentParticipant,
		type Logs
	} from '$lib/_apiParticipants';

	import { Row, Col, Badge, Progress } from 'sveltestrap/src';
	import { onMount } from 'svelte';
	import { NUM_TENTS } from '$lib/constants';

	let participants: cTentParticipant[] = [];
	let birthDayParticipants: cTentParticipant[] = [];
	let tentLeaders: TentLeader[] = [];
	let logs: Logs = { errors: [], revisions: [] };

	interface Team {
		name: string;
		persons: string[];
	}

	let teams: Team[] = [];

	let avgAge = 0;
	let youngestParticipant = '';
	let eldestParticipant = '';
	let assignedParticipants = 0;

	$: avgAge = calculateAvgAge(participants);
	$: youngestParticipant = calculateYoungestParticipant(participants);
	$: eldestParticipant = calculateEldestParticipant(participants);
	$: assignedParticipants = caluclateAssignedParticipants(participants);

	onMount(() => {
		getParticipants();
	});

	function caluclateAssignedParticipants(arg_participants: cTentParticipant[]): number {
		if (arg_participants.length == 0) {
			return 0;
		}
		let loc_assigned = 0;
		for (let i = 0; i < arg_participants.length; i++) {
			if (arg_participants[i].tent != 9999) {
				loc_assigned++;
			}
		}
		return loc_assigned;
	}
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
		logs = await apiGetLogs();

		let mats: Team = { name: 'Mat Warts', persons: [] };
		let sukus: Team = { name: 'Suppenkutscher', persons: [] };
		let free: Team = { name: 'Zeltführer', persons: [] };
		let reserver: Team = { name: 'Freie Männer', persons: [] };
		let others: Team = { name: 'Sonstige', persons: [] };
		tentLeaders = await apiGetTentLeader();

		tentLeaders.forEach((leader) => {
			let fullname = leader.firstname + ' ' + leader.lastname;
			switch (leader.job.trim().toLowerCase()) {
				case 'mat':
				case 'matina':
				case 'mat wart':
					mats.persons.push(fullname);
					break;
				case 'suku':
					sukus.persons.push(fullname);
					break;
				case 'freier mann':
				case 'freie männer':
					reserver.persons.push(fullname);
					break;
				case 'zefü':
				case 'zeltführer':
					free.persons.push(fullname);
					break;
				default:
					others.persons.push(fullname);
			}
		});

		teams.push(others);
		teams.push(mats);
		teams.push(sukus);
		teams.push(free);
		teams.push(reserver);
		teams = teams;

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
		<Col sm="6">
			<h3>Leitungsteam ({tentLeaders.length})</h3>
			<Row>
				{#each teams as team}
					<Col sm="4">
						<h5>{team.name} ({team.persons.length})</h5>
						<ul>
							{#each team.persons as person}
								<li>{person}</li>
							{/each}
						</ul>
					</Col>
				{/each}
			</Row>
		</Col>

		<Col sm="3">
			<Col>
				<h3>Teilnehmer Statistik:</h3>
				<ul>
					<li>Anzahl Teilnehmer: {participants.length}</li>
					<li>Durchschnittsalter: {avgAge}</li>
					<li>jüngster Teilnehmer: {youngestParticipant}</li>
					<li>ältester Teilnehmer: {eldestParticipant}</li>
					<li>
						<div>zu einem Zelt zugeteilt: {assignedParticipants}/{participants.length}</div>
						<Progress color="info" value={(100 * assignedParticipants) / participants.length}>
							{(100 * assignedParticipants) / participants.length}%
						</Progress>
					</li>
				</ul>
			</Col>
			<Col>
				<h3>Geburtstagskinder im Lager</h3>
				<ul>
					{#each birthDayParticipants as participant}
						<li>{participant.getFullname()} ({participant.birthdate})</li>
					{/each}
				</ul>
			</Col>
			<Col>
				<h3>Durchschnittsalter Zelte:</h3>
				<ul>
					{#each tentAvgAge as avg}
						<li>Zelt {avg.tentNumber} ({Math.round((100 * avg.avg) / avg.num) / 100})</li>
					{/each}
				</ul>
			</Col>
		</Col>

		<Col sm="3">
			<h3>Logs:</h3>
			<ul>
				<a href="/logs">
					<li>Error Logs: <Badge color="danger">{logs.errors.length}</Badge></li>
				</a>
				<a href="/logs"
					><li>Revision Logs: <Badge color="info">{logs.revisions.length}</Badge></li>
				</a>
			</ul>
		</Col>
	</Row>
</div>
