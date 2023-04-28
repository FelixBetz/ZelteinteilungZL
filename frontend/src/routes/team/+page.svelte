<script lang="ts">
	import {
		apiGetConfigs,
		apiGetTentLeader,
		type Configs,
		type cTentLeader
	} from '$lib/_apiParticipants';
	import { onMount } from 'svelte';
	import SortTable from '$lib/SortTable.svelte';
	import type { IColumn } from '$lib/sort';
	import { displayTentString, getStrTwoDecimal } from '$lib/helpers';

	let tentLeaders: cTentLeader[] = [];
	let filterdTentLeaders: cTentLeader[] = [];

	let isIncludePriest = false;

	let avgAge = 0;

	function calcAverageAge(pTeam: cTentLeader[], pIsIncludePriest: boolean) {
		let ageSum = 0;
		let num = 0;
		pTeam.forEach((leader) => {
			if (pIsIncludePriest || leader.job.toLowerCase() != 'lagerpfarrer') {
				ageSum += leader.age;
				num += 1;
			}
		});

		return ageSum / num;
	}

	$: avgAge = calcAverageAge(filterdTentLeaders, isIncludePriest);
	$: calcTeamAvg(isIncludePriest);

	function calcTeamAvg(pIsIncludePriest: boolean) {
		teams.forEach((team) => {
			let ageSum = 0;
			let num = 0;
			team.indices.forEach((idx) => {
				if (pIsIncludePriest || tentLeaders[idx].job.toLowerCase() != 'lagerpfarrer') {
					ageSum += tentLeaders[idx].age;
					num += 1;
				}
			});

			team.avg = ageSum / num;
		});

		teams = teams;
	}

	const columns: IColumn[] = [
		{ label: 'id', key: 'identifier', ascending: true },
		{ label: 'firstName', key: 'firstname', ascending: true },
		{ label: 'lastName', key: 'lastname', ascending: true },
		{ label: 'job', key: 'job', ascending: true },
		{ label: 'team', key: 'team', ascending: true },
		{ label: 'Zelt', key: 'tent', ascending: true, displayCallback: displayTentString },
		/*{ label: 'street', key: 'street', ascending: true },
		{ label: 'zipCode', key: 'zipcode', ascending: true },
		{ label: 'village', key: 'village', ascending: true },*/
		{ label: 'mail', key: 'mail', ascending: true },
		{ label: 'handy', key: 'handy', ascending: true },
		{ label: 'age', key: 'age', ascending: true, displayCallback: getStrTwoDecimal },
		{ label: 'comment', key: 'comment', ascending: true }
	];

	const searchColumns: string[] = [
		'firstname',
		'lastname',
		'job',
		'team',
		'tent',
		'mail',
		'comment'
	];

	interface Job {
		name: string;
		indices: number[];
	}

	let jobs: Job[] = [];

	interface Team {
		indices: number[];
		name: string;
		avg: number;
	}
	let teams: Team[] = [];
	let configs: Configs = { numTents: 9999, zlStart: '1970-08-12' };
	function parseJobs() {
		let mats: Job = { name: 'Mat Warts', indices: [] };
		let sukus: Job = { name: 'Suppenkutscher', indices: [] };
		let free: Job = { name: 'Zeltführer', indices: [] };
		let reserver: Job = { name: 'Freie Männer', indices: [] };
		let others: Job = { name: 'Sonstige', indices: [] };
		tentLeaders.forEach((leader, index) => {
			switch (leader.job.trim().toLowerCase()) {
				case 'mat':
				case 'matina':
				case 'mat wart':
					mats.indices.push(index);
					break;
				case 'suku':
					sukus.indices.push(index);
					break;
				case 'freier mann':
				case 'freie männer':
					reserver.indices.push(index);
					break;
				case 'zefü':
				case 'zeltführer':
					free.indices.push(index);
					break;
				default:
					others.indices.push(index);
			}
		});

		jobs.push(others);
		jobs.push(mats);
		jobs.push(sukus);
		jobs.push(free);
		jobs.push(reserver);
		jobs = jobs;
	}

	function addLeaderToTeam(pTeamName: string, pIdx: number) {
		for (let i = 0; i < teams.length; i++) {
			if (teams[i].name == pTeamName) {
				teams[i].indices.push(pIdx);
			}
		}
	}

	function parseTeams() {
		let teamNames = new Set<string>();
		//parse all Teams
		tentLeaders.forEach((leader) => {
			teamNames.add(leader.team);
		});
		//create  all teams
		teamNames.forEach((name) => {
			teams.push({ name: name, indices: [], avg: 0 });
		});

		//add tent leaders to team
		tentLeaders.forEach((leader, index) => {
			addLeaderToTeam(leader.team, index);
		});
		calcTeamAvg(isIncludePriest);
		teams = teams;
	}

	onMount(() => {
		getParticipants();
	});

	async function getParticipants() {
		configs = await apiGetConfigs();
		tentLeaders = await apiGetTentLeader();
		parseJobs();
		parseTeams();
	}
</script>

<svelte:head>
	<title>Team</title>
</svelte:head>

<div style="margin-top: 80px; margin-left: 10px;">
	<div class="row">
		<div class="col">
			<h3>Leitungsteam</h3>
			<ul>
				<li><strong>Gesamt: {tentLeaders.length}</strong></li>
				{#each jobs as job}
					<li>{job.name}: {job.indices.length}</li>
				{/each}
				<br />
				<li>
					<i>
						Durchschnittsalter: {getStrTwoDecimal(avgAge)} <br />
						(
						<input
							type="checkbox"
							class="form-check-input"
							id="avg"
							bind:checked={isIncludePriest}
						/>
						<label for="avg">Lagerpfarrer mitrechnen</label>)
					</i>
				</li>
			</ul>
		</div>

		{#each teams as team}
			<div class="col">
				<h3>{team.name} ({team.indices.length})</h3>
				<ul>
					{#each team.indices as idx}
						{#if tentLeaders[idx].job.toLowerCase() == 'zefü'}
							{#if tentLeaders[idx].tent == 9999}
								<li>
									<i>
										<strong>
											{tentLeaders[idx].firstname}
											{tentLeaders[idx].lastname}
											<span style="color:red">(Zelt XXX)</span>
										</strong>
									</i>
								</li>
							{:else if tentLeaders[idx].tent > configs.numTents}
								<li>
									<i>
										<strong>
											{tentLeaders[idx].firstname}
											{tentLeaders[idx].lastname}
											<span style="color:red">(Zelt {tentLeaders[idx].tent})</span>
										</strong>
									</i>
								</li>
							{:else}
								<li>
									{tentLeaders[idx].firstname}
									{tentLeaders[idx].lastname} (Zelt {tentLeaders[idx].tent})
								</li>
							{/if}
						{:else}
							<li>{tentLeaders[idx].firstname} {tentLeaders[idx].lastname}</li>
						{/if}
					{/each}
					<br />
					<li><i>Durchschnittsalter: {getStrTwoDecimal(team.avg)}</i></li>
				</ul>
			</div>
		{/each}
	</div>

	<SortTable data={tentLeaders} bind:filterdData={filterdTentLeaders} {columns} {searchColumns} />
</div>
