<script lang="ts">
	import Calender from './../lib/Dashboard/Calender.svelte';
	import DashboardCard from '$lib/Dashboard/DashboardCard.svelte';
	import { apiGetLogs, type Logs } from '$lib/api/apiLogs';
	import { apiGetTentLeader, type cTentLeader } from '$lib/api/apiTentleader';

	import {
		apiGetParticipants,
		apiGetParticipantsLastYear,
		type cTentParticipant
	} from '$lib/api/apiParticipants';

	import {
		getWeekdayString,
		type DateGraphData,
		getGermanDateString,
		type BarplotData
	} from '$lib/helpers';
	import { type Configs, apiGetConfigs } from '$lib/api/apiConfig';
	import { onMount } from 'svelte';
	import DateGraph from '$lib/chart/DateGraph.svelte';
	import ProgressBar from '$lib/Dashboard/ProgressBar.svelte';
	import Barplot from '$lib/chart/Barplot.svelte';

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
	let configs: Configs = { numTents: 9999, zlStart: '1970-08-12', calenderUrl: '' };

	let friendsNotRegistered: FriendsNotRegistered[] = [];
	let lastYearRegistered: string[] = [];

	let teams: Team[] = [];

	let avgAge = 0;
	let youngestParticipant = '';
	let eldestParticipant = '';
	let assignedParticipants = 0;

	let tentAvgAge: TentAvg[] = [];

	let notPaid: string[] = [];
	let noPhotosAllowed: string[] = [];
	let vegetarians: string[] = [];

	let loopedDates: DateGraphData[] = [];
	let registeredDistibution: BarplotData[] = [];
	let ageDestirbution: BarplotData[] = [];

	let showNotPaid = false;
	let showTeamMembers = false;

	$: avgAge = calculateAvgAge(participants);
	$: youngestParticipant = calculateYoungestParticipant(participants);
	$: eldestParticipant = calculateEldestParticipant(participants);
	$: assignedParticipants = caluclateAssignedParticipants(participants);
	$: calculateBirthdayKids(participants, tentLeaders, configs.zlStart);
	$: calculateStats(participants);
	$: calcRegisteredGraphs(participants);

	$: onMount(() => {
		getParticipants();
	});

	function calcRegisteredGraphs(pParticipants: cTentParticipant[]) {
		let parsedDates: Date[] = [];

		let byMonth: BarplotData[] = [];
		for (let i = 0; i < 12; i++) {
			byMonth.push({ value: 0, label: '' });
		}

		if (pParticipants.length == 0) {
			return;
		}
		pParticipants.forEach((p) => {
			let datetime = new Date(p.registered);
			parsedDates.push(new Date(datetime.toDateString()));
			//increase by month counter
			let idx = datetime.getMonth();
			byMonth[idx].value += 1;
			byMonth[idx].label = datetime.toLocaleString('default', { month: 'short' });
		});
		parsedDates.push(new Date(Date.now()));

		//remove month with no registrations
		registeredDistibution = byMonth.filter((x) => x.value > 0);

		//parsedDates = parsedDates.sort();
		parsedDates = parsedDates.sort((a, b) => a.getTime() - b.getTime());
		let minDate = parsedDates[0];
		let maxDate = parsedDates[parsedDates.length - 1];

		// Clone the start date to avoid modifying the original
		let currentDate = new Date(minDate.getTime());

		// Loop through each day between the start and end dates
		while (currentDate <= maxDate) {
			// Add the current date to the array
			loopedDates.push({ date: new Date(currentDate.getTime()), num: 0 });
			// Move to the next day
			currentDate.setDate(currentDate.getDate() + 1);
		}
		loopedDates.forEach((l) => {
			parsedDates.forEach((p) => {
				if (l.date.getTime() >= p.getTime()) {
					l.num += 1;
				}
			});
		});

		loopedDates = loopedDates;
	}

	function calculateStats(pParticipants: cTentParticipant[]) {
		notPaid = [];
		noPhotosAllowed = [];
		vegetarians = [];

		pParticipants.forEach((p) => {
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

	function caluclateAssignedParticipants(pParticipants: cTentParticipant[]): number {
		if (pParticipants.length == 0) {
			return 0;
		}
		let loc_assigned = 0;
		for (let i = 0; i < pParticipants.length; i++) {
			if (pParticipants[i].tent != 9999) {
				loc_assigned++;
			}
		}
		return loc_assigned;
	}

	function calculateYoungestParticipant(pParticipants: cTentParticipant[]): string {
		if (pParticipants.length == 0) {
			return '';
		}
		let loc_age = 100;
		let loc_index = 0;
		for (let i = 0; i < pParticipants.length; i++) {
			if (pParticipants[i].age < loc_age) {
				loc_age = pParticipants[i].age;
				loc_index = i;
			}
		}
		return (
			pParticipants[loc_index].getFullname() +
			' (' +
			pParticipants[loc_index].getAgeTwoDecimal() +
			')'
		);
	}

	function calculateEldestParticipant(pParticipants: cTentParticipant[]): string {
		if (pParticipants.length == 0) {
			return '';
		}
		let loc_age = 0;
		let loc_index = 0;
		for (let i = 0; i < pParticipants.length; i++) {
			if (pParticipants[i].age > loc_age) {
				loc_age = pParticipants[i].age;
				loc_index = i;
			}
		}
		return (
			pParticipants[loc_index].getFullname() +
			' (' +
			pParticipants[loc_index].getAgeTwoDecimal() +
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

	function calculateAvgAge(pParticipants: cTentParticipant[]): number {
		if (pParticipants.length == 0) {
			return 0;
		}
		let ageSum = 0;
		for (let i = 0; i < pParticipants.length; i++) {
			ageSum += pParticipants[i].age;
		}
		return Math.round((ageSum / pParticipants.length) * 100) / 100;
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

	function calcAgeDistribution(pParticipants: cTentParticipant[]) {
		ageDestirbution = [
			{ label: '<10', value: 0 },
			{ label: '10', value: 0 },
			{ label: '11', value: 0 },
			{ label: '12', value: 0 },
			{ label: '13', value: 0 },
			{ label: '14', value: 0 },
			{ label: '15', value: 0 },
			{ label: '≥16', value: 0 }
		];

		pParticipants.forEach((participant) => {
			if (participant.age < 10) {
				ageDestirbution[0].value += 1; // < 10
			} else if (participant.age < 11) {
				ageDestirbution[1].value += 1; //10
			} else if (participant.age < 12) {
				ageDestirbution[2].value += 1; //11
			} else if (participant.age < 13) {
				ageDestirbution[3].value += 1; //12
			} else if (participant.age < 14) {
				ageDestirbution[4].value += 1; //13
			} else if (participant.age < 15) {
				ageDestirbution[5].value += 1; //14
			} else if (participant.age < 16) {
				ageDestirbution[6].value += 1; //15
			} else {
				ageDestirbution[7].value += 1; //>=16
			}
		});

		ageDestirbution = ageDestirbution;
	}

	async function getParticipants() {
		configs = await apiGetConfigs();
		logs = await apiGetLogs();
		participants = await apiGetParticipants();
		lastYearRegistered = await apiGetParticipantsLastYear();
		calcAgeDistribution(participants);

		lastYearRegistered = lastYearRegistered.sort((a, b) => {
			let lastNameA = a.split(' ')[1];
			let lastNameB = b.split(' ')[1];
			if (lastNameA > lastNameB) {
				return 1;
			}
			if (lastNameA < lastNameB) {
				return -1;
			}

			return 0;
		});

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

<div class="container-fluid mb-5">
	<div class="row gx-3 gy-3">
		<!--1. column-->
		<div class="col-sm-4">
			<div class="row gx-3 gy-3">
				<div class="col-sm-12">
					<DashboardCard
						title={'Leitungsteam (' + tentLeaders.length + ')'}
						icon="bi-people"
						bgColor={'bg-secondary'}
					>
						<div class="row gx-0 gy-0">
							{#each teams as team}
								<div class="col-sm-6">
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
				</div>

				<div class="col-sm-12">
					<DashboardCard
						title={'Anmeldeverlauf (' + participants.length + ' Anmeldungen)'}
						icon="bi-activity"
						bgColor={'bg-success'}
					>
						{#if loopedDates.length > 0}
							<DateGraph data={loopedDates} color={'#198754'} />
						{/if}
					</DashboardCard>
				</div>

				<div class="col-sm-6">
					<DashboardCard
						title={'Termine'}
						icon="bi-calendar4"
						bgColor={'bg-secondary'}
						isSmallTitle={true}
					>
						<Calender calenderUrl={configs.calenderUrl} />
					</DashboardCard>
				</div>

				<div class="col-sm-6">
					<DashboardCard
						title={'Durchschnittsalter Zelte'}
						icon="bi-bar-chart"
						bgColor={'bg-secondary'}
						isSmallTitle={true}
					>
						<ul>
							<li>zu einem Zelt zugeteilt: {assignedParticipants}/{participants.length}</li>

							<ProgressBar
								bgColor={'bg-secondary'}
								percentage={(100 * assignedParticipants) / participants.length}
								height={30}
								classes="mb-3"
							/>

							<div class="row">
								{#each tentAvgAge as avg}
									<div class="col-sm-12">
										<li>Zelt {avg.tentNumber} ({Math.round((100 * avg.avg) / avg.num) / 100})</li>
									</div>
								{/each}
							</div>
						</ul>
					</DashboardCard>
				</div>
			</div>
		</div>

		<!--2. column-->
		<div class="col-sm-4">
			<div class="row gx-3 gy-3">
				<div class="col-sm-12">
					<DashboardCard title={'Teilnehmer Statistik'} icon="bi-graph-up" bgColor="bg-primary">
						<ul>
							<li>Anzahl Teilnehmer: {participants.length}</li>
							<li>Durchschnittsalter: {avgAge}</li>
							<li>jüngster Teilnehmer: {youngestParticipant}</li>
							<li>ältester Teilnehmer: {eldestParticipant}</li>
						</ul>
					</DashboardCard>
				</div>

				<div class="col-sm-12">
					<DashboardCard title={'Geburtstage im Lager'} icon="bi-gift" bgColor={'bg-success'}>
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

				<div class="col-sm-6">
					<DashboardCard
						title={'keine Fotos: ' + noPhotosAllowed.length}
						icon="bi-camera-video-off"
						bgColor={'bg-warning'}
						isSmallTitle={true}
					>
						{#if noPhotosAllowed.length == 0}
							<i>niemand</i>
						{:else}
							<ul>
								{#each noPhotosAllowed as p}
									<li>{p}</li>
								{/each}
							</ul>
						{/if}
					</DashboardCard>
				</div>

				<div class="col-sm-6">
					<DashboardCard
						title={'Vegetarisch: ' + vegetarians.length}
						icon="bi-piggy-bank"
						bgColor={'bg-warning'}
						isSmallTitle={true}
					>
						{#if vegetarians.length == 0}
							<i>niemand</i>
						{:else}
							<ul>
								{#each vegetarians as p}
									<li>{p}</li>
								{/each}
							</ul>
						{/if}
					</DashboardCard>
				</div>

				<div class="col-sm-6">
					<DashboardCard
						title={'Bezahlt: ' + (participants.length - notPaid.length) + '/' + participants.length}
						icon="bi-currency-euro"
						bgColor={'bg-danger'}
						isSmallTitle={true}
					>
						<ProgressBar
							bgColor={'bg-danger'}
							percentage={(100 * (participants.length - notPaid.length)) / participants.length}
							height={30}
							classes="mb-2"
						/>

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
				<div class="col-sm-6">
					<DashboardCard
						title={'Anmeldungen pro Monat'}
						icon="bi-bar-chart"
						bgColor={'bg-success'}
						isSmallTitle={true}
					>
						{#if registeredDistibution.length > 0}
							<Barplot data={registeredDistibution} color={'#198754'} />
						{/if}
					</DashboardCard>
				</div>
				<div class="col-sm-12">
					<DashboardCard
						title={'Altersverteilung'}
						icon="bi-bar-chart"
						bgColor={'bg-primary'}
						isSmallTitle={true}
					>
						{#if ageDestirbution.length > 0}
							<Barplot data={ageDestirbution} color={'#0d6efd'} xLabel={'Alter'} />
						{/if}
					</DashboardCard>
				</div>
			</div>
		</div>

		<!--3. column-->
		<div class="col-sm-4">
			<div class="row gx-3 gy-3">
				<div class="col-sm-12">
					<DashboardCard
						title={'Nicht angemeldete Freunde: ' + friendsNotRegistered.length}
						icon="bi-person-x"
						bgColor={'bg-danger'}
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
						title={'Letztes Jahr angemeldet: ' + lastYearRegistered.length}
						icon="bi-person-x"
						bgColor={'bg-danger'}
					>
						<ul>
							<div class="row">
								{#each lastYearRegistered as name}
									<div class="col-sm-4">
										<li><strong>{name}</strong></li>
									</div>
								{/each}
							</div>
						</ul>
					</DashboardCard>
				</div>
				<div class="col-sm-6">
					<DashboardCard
						title={'Logs'}
						icon="bi-card-text"
						bgColor={'bg-secondary'}
						isSmallTitle={true}
					>
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
					<DashboardCard
						title={'Configs'}
						icon="bi-gear"
						bgColor={'bg-secondary'}
						isSmallTitle={true}
					>
						<ul>
							<li>Anzahl Zelte: {configs.numTents}</li>
							<li>Start des Zeltlagers: {getGermanDateString(configs.zlStart)}</li>
							<li><a href={configs.calenderUrl} target="_blank"> Kalender URL</a></li>
						</ul>
					</DashboardCard>
				</div>
			</div>
		</div>
	</div>
	<div class="row gx-3 gy-3" />
</div>
