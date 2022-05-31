export interface Participant {
	birthdate: string[];
	firstname: string;
	friends: string[];
	id: number;
	lastname: string;
	village: string;
	zipcode: number;
	age: number;
}

const base = 'http://127.0.0.1:8080/api';

function getAge(birthString: string) {
	const today = new Date();
	const birthDate = new Date(birthString);

	const diffMilliseconds = today.getTime() - birthDate.getTime();
	const age = diffMilliseconds / 1000 / 3600 / 24 / 365;
	return age;
}

export async function apiGetParticipants(): Promise<Participant[]> {
	// locals.userid comes from src/hooks.js
	const response = await fetch(base + '/participants')
		.then((res) => res.json())
		.then((res: Participant[]) => {
			const b: Participant[] = res;
			for (let i = 0; i < b.length; i++) {
				b[i].age = getAge(b[i].birthdate[0]);
			}
			return b;
		})
		.catch((error: Error) => {
			console.log(error);
			return [];
		});

	return response;
}
