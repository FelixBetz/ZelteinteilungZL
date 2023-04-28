import { BASE_URL } from './api';

interface Revision {
	fullname: string;
	id: number;
	isError: boolean;
	newValue: string;
	oldValue: string;
	property: string;
	errorMessage: string;
}

export interface Logs {
	errors: string[];
	revisions: Revision[];
}

export async function apiGetLogs(): Promise<Logs> {
	const response = await fetch(BASE_URL + '/logs')
		.then((res) => res.json())
		.then((res: Logs) => {
			return res;
		})
		.catch((error: Error) => {
			console.error(error);
			const ret: Logs = { errors: [], revisions: [] };
			return ret;
		});

	return response;
}
