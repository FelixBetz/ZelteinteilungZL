export interface IColumn {
	label: string;
	ascending: boolean;
	key: string;
	link?: string;
	displayCallback?: ((arg0: any) => void) | undefined;
}

export function numberSort(a: number, b: number, sortby: boolean) {
	if (sortby == true) {
		const temp = a;
		a = b;
		b = temp;
	}
	if (a >= b) {
		return 0;
	} else {
		return 1;
	}
}

export function stringSort(a: string, b: string, sortby: boolean) {
	if (sortby == true) {
		const temp = a;
		a = b;
		b = temp;
	}
	if (a >= b) {
		return 0;
	} else {
		return 1;
	}
}

export function boolSort(a: boolean, b: boolean, sortby: boolean) {
	if (sortby == true) {
		const temp = a;
		a = b;
		b = temp;
	}
	if (a) {
		return 0;
	} else {
		return 1;
	}
}

export function getAgeTwoDecimal(age: number): number {
	return Math.round(age * 100) / 100;
}
