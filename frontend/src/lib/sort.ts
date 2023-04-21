export function numberSort(a: number, b: number, sortby: Boolean) {
	if (sortby == true) {
		let temp = a;
		a = b;
		b = temp;
	}
	if (a >= b) {
		return 0;
	} else {
		return 1;
	}
}

export function textSort(a: string, b: string, sortby: Boolean) {
	if (sortby == true) {
		let temp = a;
		a = b;
		b = temp;
	}
	if (a >= b) {
		return 0;
	} else {
		return 1;
	}
}

export function boolSort(a: boolean, b: boolean, sortby: Boolean) {
	if (sortby == true) {
		let temp = a;
		a = b;
		b = temp;
	}
	if (a) {
		return 0;
	} else {
		return 1;
	}
}
