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

export function getStrTwoDecimal(age: number): number {
	return Math.round(age * 100) / 100;
}

export interface DateGraphData {
	date: Date;
	num: number;
}
