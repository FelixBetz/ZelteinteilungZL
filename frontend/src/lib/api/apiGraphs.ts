import { BASE_URL } from './api';

export interface ZipCodes {
	zipCode: number;
	location: string;
	addressString: string;
	name: string;
}

export async function apiGetMaps(zipCodes: ZipCodes[]): Promise<string[]> {
	const formData = new FormData();
	formData.append('zipCodes', JSON.stringify(zipCodes));
	const response = await fetch(BASE_URL + '/maps', {
		method: 'POST',
		body: formData
	})
		.then((res) => {
			return res.json();
		})
		.catch((error: Error) => {
			console.error(error);
			return [];
		});

	return response;
}
export interface GraphInput {
	friends: string[];
	name: string;
	tent: number;
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
	color: GraphColor;
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

export enum GraphColor {
	BLACK = 'black',
	GREEN = 'green',
	RED = 'red'
}
