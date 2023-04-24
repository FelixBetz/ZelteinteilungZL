<script lang="ts">
	import { apiGetTentLeader, type cTentLeader } from '$lib/_apiParticipants';
	import { onMount } from 'svelte';
	import SortTable from '$lib/SortTable.svelte';
	import { getAgeTwoDecimal, type IColumn } from '$lib/sort';

	let tentLeaders: cTentLeader[] = [];
	let filterdTentLeaders: cTentLeader[] = [];

	const columns: IColumn[] = [
		{ label: 'id', key: 'identifier', ascending: true },
		{ label: 'firstName', key: 'firstname', ascending: true },
		{ label: 'lastName', key: 'lastname', ascending: true },
		{ label: 'job', key: 'job', ascending: true },
		{ label: 'team', key: 'team', ascending: true },
		{ label: 'tent', key: 'tent', ascending: true },
		/*{ label: 'street', key: 'street', ascending: true },
		{ label: 'zipCode', key: 'zipcode', ascending: true },
		{ label: 'village', key: 'village', ascending: true },*/
		{ label: 'mail', key: 'mail', ascending: true },
		{ label: 'handy', key: 'handy', ascending: true },
		{ label: 'age', key: 'age', ascending: true, displayCallback: getAgeTwoDecimal },
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
	}
	let teams: Team[] = [];

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
			teams.push({ name: name, indices: [] });
		});

		//add tent leaders to team
		tentLeaders.forEach((leader, index) => {
			addLeaderToTeam(leader.team, index);
		});
		teams = teams;
	}

	onMount(() => {
		getParticipants();
	});

	async function getParticipants() {
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
			</ul>
		</div>

		{#each teams as team}
			<div class="col">
				<h3>{team.name} ({team.indices.length})</h3>
				<ul>
					{#each team.indices as idx}
						<li>{tentLeaders[idx].firstname} {tentLeaders[idx].lastname}</li>
					{/each}
				</ul>
			</div>
		{/each}
	</div>

	<SortTable data={tentLeaders} bind:filterdData={filterdTentLeaders} {columns} {searchColumns} />
</div>
