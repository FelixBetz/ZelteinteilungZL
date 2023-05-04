export function displayTentString(pTent: number): string {
	return pTent != 9999 ? pTent.toString() : '';
}

export const WEEKDAYS = [
	'Sonntag',
	'Montag',
	'Dienstag',
	'Mittwoch',
	'Donnerstag',
	'Freitag',
	'Samstag'
];
export function getWeekdayString(pDate: Date) {
	const date = pDate.toLocaleString('de-DE', { day: '2-digit', month: '2-digit' });

	return WEEKDAYS[pDate.getDay()] + ' ' + date;
}

export function getStrTwoDecimal(age: number): string {
	return (Math.round(age * 100) / 100).toString();
}
export function getStrOneDecimal(age: number): string {
	return (Math.round(age * 10) / 10).toString();
}

export interface DateGraphData {
	date: Date;
	num: number;
}

export function getGermanDateString(pDate: string) {
	const [y, m, d] = pDate.split('-');
	return d + '.' + m + '.' + y;
}

export interface BarplotData {
	label: string;
	value: number;
}

export function getDaysDelta(pDateA: Date, pDateB: Date): number {
	const diffTime = Math.abs(pDateA.getTime() - pDateB.getTime());
	const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

	console.log(diffDays); // Output: 9

	return diffDays;
}
