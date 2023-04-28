<script lang="ts">
	import DashboardCard from '$lib/Dashboard/DashboardCard.svelte';
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
	import { getWeekdayString, getStrTwoDecimal } from '$lib/helpers';

	import { onMount } from 'svelte';

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

	interface FriendsNotRegistered {
		name: string;
		namendBy: string[];
	}

	let participants: cTentParticipant[] = [];
	let birthDayKids: BirthdayKid[] = [];
	let tentLeaders: cTentLeader[] = [];
	let logs: Logs = { errors: [], revisions: [] };
	let configs: Configs = { numTents: 9999, zlStart: '1970-08-12' };

	let friendsNotRegistered: FriendsNotRegistered[] = [];

	let teams: Team[] = [];

	let avgAge = 0;
	let youngestParticipant = '';
	let eldestParticipant = '';
	let assignedParticipants = 0;

	let tentAvgAge: TentAvg[] = [];

	let notPaid: string[] = [];
	let noPhotosAllowed: string[] = [];
	let vegetarians: string[] = [];

	let showNotPaid = false;
	let showTeamMembers = false;

	$: avgAge = calculateAvgAge(participants);
	$: youngestParticipant = calculateYoungestParticipant(participants);
	$: eldestParticipant = calculateEldestParticipant(participants);
	$: assignedParticipants = caluclateAssignedParticipants(participants);
	$: calculateBirthdayKids(participants, tentLeaders, configs.zlStart);
	$: calculateStats(participants);

	$: onMount(() => {
		getParticipants();
	});

	function calculateStats(arg_participants: cTentParticipant[]) {
		notPaid = [];
		noPhotosAllowed = [];
		vegetarians = [];

		arg_participants.forEach((p) => {
			if (!p.paid) {
				notPaid[notPaid.length] = p.getFullname();
			}
			if (p.is_vegetarian) {
				vegetarians[vegetarians.length] = p.getFullname();
			}
			if (!p.is_photo_allowed) {
				noPhotosAllowed[noPhotosAllowed.length] = p.getFullname();
			}
		});
	}

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
		for (let i = 0; i < configs.numTents; i++) {
			tentAvgAge[tentAvgAge.length] = { avg: 0, num: 0, tentNumber: i + 1 };
		}
		for (let i = 0; i < participants.length; i++) {
			let tentNumber = participants[i].tent;
			if (tentNumber <= configs.numTents) {
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

	function calculateBirthdayKids(
		pParticipants: cTentParticipant[],
		pTentLeader: cTentLeader[],
		pZlStart: string
	) {
		const zlStartSplitted = pZlStart.split('-');

		const zlYear = +zlStartSplitted[0];
		const beginZlDate = new Date(zlYear, +zlStartSplitted[1] - 1, +zlStartSplitted[2]);
		const endZlDate = new Date(zlYear, +zlStartSplitted[1] - 1, +zlStartSplitted[2]);
		endZlDate.setDate(beginZlDate.getDate() + 7); //+ 7 days

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

	function parseNotRegisteredFriends(pParitcipants: cTentParticipant[]) {
		friendsNotRegistered = [];

		let compareFriends: string[] = [];
		pParitcipants.forEach((participant) => {
			compareFriends.push(participant.getFullname());
		});
		pParitcipants.forEach((participant) => {
			participant.friends.forEach((friend) => {
				if (friend != '' && !compareFriends.includes(friend)) {
					let isAdded = false;
					friendsNotRegistered.forEach((el) => {
						if (el.name == friend) {
							el.namendBy.push(participant.getFullname());
							isAdded = true;
						}
					});
					if (!isAdded) {
						friendsNotRegistered.push({
							name: friend,
							namendBy: new Array(participant.getFullname())
						});
					}
				}
			});
		});

		friendsNotRegistered = friendsNotRegistered.sort((a, b) => {
			let lastNameA = a.name.split(' ')[1];
			let lastNameB = b.name.split(' ')[1];
			if (lastNameA > lastNameB) {
				return 1;
			}
			if (lastNameA < lastNameB) {
				return -1;
			}

			return 0;
		});
	}

	async function getParticipants() {
		configs = await apiGetConfigs();
		logs = await apiGetLogs();
		participants = await apiGetParticipants();

		parseNotRegisteredFriends(participants);

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
						free.persons.push(fullname + (' (Zelt: ' + leader.tent + ')'));
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
		<div class="col col-sm-4">
			<DashboardCard title={'Leitungsteam (' + tentLeaders.length + ')'} icon="bi-people">
				<div class="row">
					{#each teams as team}
						<div class="col col-sm-6">
							<h5>
								{team.name} ({team.persons.length})
								<i
									on:click={() => (showTeamMembers = !showTeamMembers)}
									on:keydown={() => (showTeamMembers = !showTeamMembers)}
									class={showTeamMembers ? 'bi-dash-lg' : 'bi-plus-lg'}
								/>
							</h5>
							<ul class={showTeamMembers ? '' : 'collapse'}>
								{#each team.persons as person}
									<li>{person}</li>
								{/each}
							</ul>
						</div>
					{/each}
				</div>
			</DashboardCard>

			<div class="col-sm-12">
				<DashboardCard title={'Durchschnittsalter Zelte'} icon="bi-bar-chart">
					<ul>
						{#each tentAvgAge as avg}
							<li>Zelt {avg.tentNumber} ({Math.round((100 * avg.avg) / avg.num) / 100})</li>
						{/each}
					</ul>
				</DashboardCard>
			</div>

			<div class="row">
				<div class="col-sm-6">
					<DashboardCard title={'Logs'} icon="bi-card-text">
						<ul>
							<a href="/logs">
								<li>Error Logs: <span class="badge bg-danger">{logs.errors.length}</span></li>
							</a>
							<a href="/logs">
								<li>Revision Logs: <span class="badge bg-info">{logs.revisions.length}</span></li>
							</a>
						</ul>
					</DashboardCard>
				</div>
				<div class="col-sm-6">
					<DashboardCard title={'Configs'} icon="bi-gear">
						<ul>
							<li>Anzahl Zelte: {configs.numTents}</li>
							<li>Start des Zeltlagers: {configs.zlStart}</li>
						</ul>
					</DashboardCard>
				</div>
			</div>
		</div>

		<div class="col col-sm-4">
			<div class="row">
				<div class="col-sm-12">
					<DashboardCard title={'Teilnehmer Statistik'} icon="bi-graph-up">
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
										{getStrTwoDecimal((100 * assignedParticipants) / participants.length)}%
									</div>
								</div>
							</li>
						</ul>
					</DashboardCard>
				</div>

				<div class="col-sm-12">
					<DashboardCard title={'Geburtstage im Lager'} icon="bi-gift">
						<ul>
							{#each birthDayKids as kid}
								<li>
									<strong>
										{kid.name},
										<i>{+configs.zlStart.split('-')[0] - kid.birthday.getFullYear()} Jahre</i>
									</strong>
									({kid.birthday.toLocaleDateString('de-DE', {
										day: '2-digit',
										month: '2-digit',
										year: 'numeric'
									})}),<br />
									<i>{kid.weekday} ({kid.tent})</i>
								</li>
							{/each}
						</ul>
					</DashboardCard>
				</div>

				<div class="col-sm-12">
					<DashboardCard
						title={'Nicht fotografieren:' + noPhotosAllowed.length}
						icon="bi-camera-video-off"
					>
						<ul>
							{#each noPhotosAllowed as p}
								<li>{p}</li>
							{/each}
						</ul>
					</DashboardCard>
				</div>

				<div class="col-sm-12">
					<DashboardCard title={'Vegetarisch: ' + vegetarians.length} icon="bi-piggy-bank">
						<ul>
							{#each vegetarians as p}
								<li>{p}</li>
							{/each}
						</ul>
					</DashboardCard>
				</div>
			</div>
		</div>
		<div class="col col-sm-4">
			<div class="row">
				<div class="col-sm-12">
					<DashboardCard
						title={'Nicht angemeldete Freunde: ' + friendsNotRegistered.length}
						icon="bi-person-x"
					>
						<ul>
							{#each friendsNotRegistered as p}
								<li><strong>{p.name}</strong> (angegeben von: {p.namendBy.join(', ')})</li>
							{/each}
						</ul>
					</DashboardCard>
				</div>

				<div class="col-sm-12">
					<DashboardCard
						title={'Bezahlt: ' + (participants.length - notPaid.length) + '/' + participants.length}
						icon="bi-currency-euro"
					>
						<div class="progress">
							<div
								class="progress-bar bg-info"
								role="progressbar"
								style="width: {(100 * (participants.length - notPaid.length)) /
									participants.length}%;"
							>
								{getStrTwoDecimal(
									(100 * (participants.length - notPaid.length)) / participants.length
								)}%
							</div>
						</div>
						<h5>
							Nicht Bezahlt: {notPaid.length}
							<i
								on:click={() => (showNotPaid = !showNotPaid)}
								on:keydown={() => (showNotPaid = !showNotPaid)}
								class={showNotPaid ? 'bi-dash-lg' : 'bi-plus-lg'}
							/>
						</h5>

						<ul class={showNotPaid ? '' : 'collapse'}>
							{#each notPaid as p}
								<li>{p}</li>
							{/each}
						</ul>
					</DashboardCard>
				</div>
			</div>
		</div>
	</div>
</div>
