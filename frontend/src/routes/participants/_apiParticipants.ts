
export interface Participant {
	birthdate: string[];
	firstname: string;
	friends: string[];
	lastname: string;
	village: string;
	zipcode: number;
}


const base = 'http://127.0.0.1:8080/api';

export async function apiGetParticipants(): Promise<Participant[]> {
	// locals.userid comes from src/hooks.js
	const response = await fetch(base + "/participants")
		.then(res => res.json())
		.then((res: Participant[]) => {
			let b: Participant[] = res;
			return b;
		})
		.catch((error: Error) => {
			console.log(error);
			return [];
		});

	return response;
}