import { BASE_URL } from './api';
export interface List {
	dir_link: string;
	dir_name: string;
	files: string[];
}
export async function apiGetGenerateOverallList(): Promise<string> {
	const response = await fetch(BASE_URL + '/lists/generate/all')
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
export async function apiGetListsDownloadLinks(): Promise<List[]> {
	const response = await fetch(BASE_URL + '/lists')
		.then((res) => res.json())
		.then((res: List[]) => {
			return res;
		})
		.catch((error: Error) => {
			console.error(error);
			return [];
		});

	return response;
}
