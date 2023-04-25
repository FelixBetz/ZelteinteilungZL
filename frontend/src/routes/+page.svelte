<script lang="ts">
	import {
		apiGetParticipants,
		apiGetTentLeader,
		apiGetLogs,
		type cTentLeader,
		type cTentParticipant,
		type Logs,
		type Configs,
		apiGetConfigs
	} from '$lib/_apiParticipants';

	import { onMount } from 'svelte';
	import { NUM_TENTS } from '$lib/constants';

	interface TentAvg {
		avg: number;
		num: number;
		tentNumber: number;
	}

	interface Team {
		name: string;
		persons: string[];
	}
	interface BirthdayKid {
		name: string;
		birthday: Date;
		weekday: string;
		tent: string;
	}

	let participants: cTentParticipant[] = [];
	let birthDayKids: BirthdayKid[] = [];
	let tentLeaders: cTentLeader[] = [];
	let logs: Logs = { errors: [], revisions: [] };
	let configs: Configs = { numTents: 9999, zlStart: '1970-08-12' };

	let teams: Team[] = [];

	let avgAge = 0;
	let youngestParticipant = '';
	let eldestParticipant = '';
	let assignedParticipants = 0;

	let tentAvgAge: TentAvg[] = [];

	const weekdays = [
		'Sonntag',
		'Montag',
		'Dienstag',
		'Mittwoch',
		'Donnerstag',
		'Freitag',
		'Samstag'
	];

	$: avgAge = calculateAvgAge(participants);
	$: youngestParticipant = calculateYoungestParticipant(participants);
	$: eldestParticipant = calculateEldestParticipant(participants);
	$: assignedParticipants = caluclateAssignedParticipants(participants);
	$: calculateBirthdayKids(participants, tentLeaders, configs.zlStart);

	$: onMount(() => {
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

	function getWeekdayString(pDate: Date) {
		let weekday = weekdays[pDate.getDay()];
		let date = pDate.toLocaleString('de-DE', { day: '2-digit', month: '2-digit' });
		let weekdayString = weekday + ' ' + date;
		return weekdayString;
	}

	function calculateBirthdayKids(
		pParticipants: cTentParticipant[],
		pTentLeader: cTentLeader[],
		pZlStart: string
	) {
		const zlStartSplitted = pZlStart.split('-');

		const zlYear = +zlStartSplitted[0];
		const beginZlDate = new Date(zlYear, +zlStartSplitted[1] - 1, +zlStartSplitted[2]); //todo
		const endZlDate = new Date(zlYear, +zlStartSplitted[1] - 1, +zlStartSplitted[2]);
		endZlDate.setDate(beginZlDate.getDate() + 7);

		birthDayKids = [];

		pParticipants.forEach((p) => {
			const [year, month, day] = p.birthdate.split('-');
			const birthDate = new Date(zlYear, +month - 1, +day); //(0 = January to 11 = December)

			if (beginZlDate <= birthDate && endZlDate >= birthDate) {
				birthDayKids[birthDayKids.length] = {
					name: p.getFullname(),
					birthday: new Date(+year, +month - 1, +day),
					weekday: getWeekdayString(birthDate),
					tent: 'Zelt ' + p.tent
				};
			}
		});

		pTentLeader.forEach((p) => {
			const [year, month, day] = p.birthdate.split('-');
			const birthDate = new Date(zlYear, +month - 1, +day); //(0 = January to 11 = December)

			if (beginZlDate <= birthDate && endZlDate >= birthDate) {
				birthDayKids[birthDayKids.length] = {
					name: p.getFullname(),
					birthday: new Date(+year, +month - 1, +day),
					weekday: getWeekdayString(birthDate),
					tent: p.team
				};
			}
		});

		birthDayKids.sort((x, y) => x.birthday.getTime() - y.birthday.getTime());
	}

	async function getParticipants() {
		configs = await apiGetConfigs();
		logs = await apiGetLogs();
		participants = await apiGetParticipants();

		let mats: Team = { name: 'Mat Warts', persons: [] };
		let sukus: Team = { name: 'Suppenkutscher', persons: [] };
		let free: Team = { name: 'Zeltführer', persons: [] };
		let notAssigend: Team = { name: 'Zeltführer (kein Zelt)', persons: [] };
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
					if (leader.tent == 9999) {
						notAssigend.persons.push(fullname);
					} else {
						free.persons.push(fullname);
					}
					break;
				default:
					others.persons.push(fullname);
			}
		});

		teams.push(others);
		teams.push(mats);
		teams.push(sukus);
		teams.push(free);
		teams.push(notAssigend);
		teams.push(reserver);
		teams = teams;

		calculateTentAvgAge();
	}
</script>

<svelte:head>
	<title>Home</title>
</svelte:head>

<div style="margin-top: 80px; margin-left: 10px;">
	<div class="row">
		<div class="col col-sm-6">
			<h3>Leitungsteam ({tentLeaders.length})</h3>
			<div class="row">
				{#each teams as team}
					<div class="col col-sm-4">
						<h5>{team.name} ({team.persons.length})</h5>
						<ul>
							{#each team.persons as person}
								<li>{person}</li>
							{/each}
						</ul>
					</div>
				{/each}
			</div>
		</div>

		<div class="col col-sm-3">
			<div class="col">
				<h3>Teilnehmer Statistik:</h3>
				<ul>
					<li>Anzahl Teilnehmer: {participants.length}</li>
					<li>Durchschnittsalter: {avgAge}</li>
					<li>jüngster Teilnehmer: {youngestParticipant}</li>
					<li>ältester Teilnehmer: {eldestParticipant}</li>
					<li>
						<div>zu einem Zelt zugeteilt: {assignedParticipants}/{participants.length}</div>
						<div class="progress">
							<div
								class="progress-bar bg-info"
								role="progressbar"
								style="width: {(100 * assignedParticipants) / participants.length}%;"
							>
								{(100 * assignedParticipants) / participants.length}%
							</div>
						</div>
					</li>
				</ul>
			</div>
			<div class="col">
				<h3>Geburtstage im Lager</h3>
				<ul>
					{#each birthDayKids as kid}
						<li>
							<strong>
								{kid.name},
								<i>{+configs.zlStart.split('-')[0] - kid.birthday.getFullYear()} Jahre</i>
							</strong>
							({kid.birthday.toLocaleDateString()}),<br />
							<i>{kid.weekday} ({kid.tent})</i>
						</li>
					{/each}
				</ul>
			</div>
			<div class="col">
				<h3>Durchschnittsalter Zelte:</h3>
				<ul>
					{#each tentAvgAge as avg}
						<li>Zelt {avg.tentNumber} ({Math.round((100 * avg.avg) / avg.num) / 100})</li>
					{/each}
				</ul>
			</div>
		</div>

		<div class="col col-sm-3">
			<h3>Logs:</h3>
			<ul>
				<a href="/logs">
					<li>Error Logs: <span class="badge bg-danger">{logs.errors.length}</span></li>
				</a>
				<a href="/logs">
					<li>Revision Logs: <span class="badge bg-info">{logs.revisions.length}</span></li>
				</a>
			</ul>
		</div>
		<div class="col col-sm-3">
			<h3>Configs:</h3>
			<ul>
				<li>Anzahl Zelte: {configs.numTents}</li>
				<li>Start des Zeltlagers: {configs.zlStart}</li>
			</ul>
		</div>
	</div>
</div>
