import { BASE_URL } from './api';

export async function apiGetGenerateOverallList(): Promise<string> {
	const response = await fetch(BASE_URL + '/lists/overall')
		.then((res) => res.json())
		.then((res: string) => {
			return res;
		})
		.catch((error: Error) => {
			console.error(error);
			return 'error';
		});

	return response;
}
