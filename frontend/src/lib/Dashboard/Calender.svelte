<script lang="ts">
	import { getDaysDelta, getStrOneDecimal } from '$lib/helpers';
	//@ts-ignore
	import ICAL from 'ical.js';
	import { onMount } from 'svelte';

	interface Event {
		name: string;
		start: Date;
		end: Date;
		description: string;
	}

	export let calenderUrl = 'https://invalid-calender.de';

	let substituteMsg = 'keine Termine';

	let events: Event[] = [];
	let nextEventIdx = -1;

	export let color = 'danger';

	$: nextEventIdx = getClosestDateIdx(events);

	$: getCalender(calenderUrl);

	let isFetchAllowed = false;

	function toBeautyDeltaStr(): string {
		let days = getDaysDelta(new Date(Date.now()), events[nextEventIdx].start);
		if (days <= 6) {
			return 'noch ' + days + ' Tage';
		}

		return 'noch ' + getStrOneDecimal(days / 7) + ' Wochen';
	}

	onMount(() => {
		isFetchAllowed = true;
	});

	function toLocleDateStr(pDate: Date): string {
		return pDate.toLocaleDateString('de-DE', {
			day: '2-digit',
			month: '2-digit',
			year: '2-digit'
		});
	}

	function getClosestDateIdx(pEvents: Event[]) {
		let targetData = new Date(Date.now());
		for (let i = 0; i < pEvents.length; i++) {
			if (pEvents[i].start.getTime() - targetData.getTime() > 0) {
				return i;
			}
		}

		return -1;
	}
	function getCalender(pUrl: string) {
		if (!isFetchAllowed) {
			return;
		}
		substituteMsg = 'keine Termine';
		// Fetch the iCalendar file
		fetch(pUrl)
			.then((response) => response.text())
			.then((data) => {
				// Parse the iCalendar data using iCalendar.js
				const jcalData = ICAL.parse(data);
				const calendar = new ICAL.Component(jcalData);

				// Get all VEVENT components in the calendar
				const icsEvents = calendar.getAllSubcomponents('vevent');

				// Loop through each event and log its properties
				//@ts-ignore
				icsEvents.forEach((event) => {
					const summary = event.getFirstPropertyValue('summary');
					const startDate = event.getFirstPropertyValue('dtstart').toJSDate();
					const endDate = event.getFirstPropertyValue('dtend').toJSDate();

					events[events.length] = {
						name: summary,
						start: startDate,
						end: endDate,
						description: ''
					};
				});
				events = events.sort((a, b) => {
					return a.start.getTime() - b.start.getTime();
				});
			})
			.catch(() => {
				events = [];

				substituteMsg =
					'<strong class="text-danger">Kalender nicht erreichbar</strong> ' +
					'<br/>(<a target="_blank" href ="' +
					pUrl +
					'">Kalender Link</a>)';
			});
	}
</script>

{#if events.length == 0}
	<i>{@html substituteMsg}</i>
{:else}
	<ul>
		{#each events as event, idx}
			{#if idx == nextEventIdx}
				<span class="highlight-container" style="--color: var(--bs-{color}-rgb)">
					<span class="highlight">
						<li class="mt-2 mb-2">
							<strong> {toLocleDateStr(event.start)}: </strong><br />
							<i> {event.name} </i><br />
							<strong><i>({toBeautyDeltaStr()})</i></strong>
						</li>
					</span>
				</span>
			{:else}
				<li class="mt-1">
					<strong>{toLocleDateStr(event.start)}: </strong><br />
					<i> {event.name} </i>
				</li>
			{/if}
		{/each}
	</ul>
{/if}

<style>
	.highlight-container,
	.highlight {
		position: relative;
	}

	.highlight-container {
		display: inline-block;
	}
	.highlight-container:before {
		content: ' ';
		display: block;
		height: 100%;
		width: 120%;
		margin-left: -20px;

		position: absolute;
		background-color: rgba(var(--color), 0.3) !important;

		transform: rotate(2deg);
		top: -1px;
		left: -1px;
		border-radius: 20% 25% 20% 24%;
		padding: 10px 3px 3px 10px;
	}
</style>
