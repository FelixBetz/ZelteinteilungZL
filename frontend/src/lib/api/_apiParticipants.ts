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

export interface ZipCodes {
	zipCode: number;
	location: string;
}

export async function apiGetMaps(zipCodes: ZipCodes[]): Promise<string> {
	const formData = new FormData();
	formData.append('zipCodes', JSON.stringify(zipCodes));
	const response = await fetch(BASE_URL + '/maps', {
		method: 'POST',
		body: formData
	})
		.then((res) => {
			res;
			return 'ok';
		})
		.catch((error: Error) => {
			console.error(error);
			return 'error';
		});

	return response;
}
export interface GraphInput {
	friends: string[];
	name: string;
}

export interface INode {
	id: string;
	group: string;
	x?: number;
	y?: number;
}
export interface ILink {
	source: string;
	target: string;
	value: number;
}

export interface IData {
	nodes: INode[];
	links: ILink[];
}
export async function apiGetGraph(): Promise<GraphInput[]> {
	const response = await fetch(BASE_URL + '/graph')
		.then((res) => res.json())
		.then((res: GraphInput[]) => {
			return res;
		})
		.catch((error: Error) => {
			console.error(error);
			return [];
		});

	return response;
}
