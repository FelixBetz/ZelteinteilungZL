export interface IColumn {
	label: string;
	ascending: boolean;
	key: string;
	link?: string;
	displayCallback?:
		| ((pVal: boolean) => string)
		| ((pVal: string) => string)
		| ((pVal: number) => string)
		| ((pVal: string[]) => string);
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
