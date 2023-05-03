import { BASE_URL } from './api';

export interface Configs {
	numTents: number;
	zlStart: string;
	calenderUrl: string;
}

export async function apiGetConfigs(): Promise<Configs> {
	const response = await fetch(BASE_URL + '/configs')
		.then((res) => res.json())
		.then((res: Configs) => {
			return res;
		})
		.catch((error: Error) => {
			console.error(error);
			const ret: Configs = { numTents: 9999, zlStart: '1970-08-12', calenderUrl: '' };
			return ret;
		});

	return response;
}

export async function apiPostConfigs(pConfigs: Configs): Promise<Configs> {
	const options = {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(pConfigs)
	};

	const response = await fetch(BASE_URL + '/configs', options)
		.then((res) => res.json())
		.then((res: Configs) => {
			return res;
		})
		.catch((error: Error) => {
			console.error(error);
			const ret: Configs = { numTents: 9999, zlStart: '1970-08-12', calenderUrl: '' };
			return ret;
		});

	return response;
}
