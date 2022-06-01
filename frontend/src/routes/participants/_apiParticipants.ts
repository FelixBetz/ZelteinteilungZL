interface Participant {
	birthdate: string[];
	firstname: string;
	friends: string[];
	id: number;
	lastname: string;
	village: string;
	zipcode: number;
	age: number;
}

export class TentParticipant {
	public age = 0;
	constructor(
		public id: number,
		public firstname: string,
		public lastname: string,
		public zipcode: number,
		public village: string,
		public birthdateStr: string,
		public friends: string[]
	) {
		this.calculateAge();
	}

	private calculateAge() {
		const today = new Date();
		const birthDate = new Date(this.birthdateStr);

		const diffMilliseconds = today.getTime() - birthDate.getTime();
		this.age = diffMilliseconds / 1000 / 3600 / 24 / 365;
	}

	public getAgeOneDecimal() {
		return Math.round(this.age * 10) / 10;
	}
	public getAgeTwoDecimal() {
		return Math.round(this.age * 100) / 100;
	}

	public getFullname() {
		return this.firstname + ' ' + this.lastname;
	}
}

const base = 'http://127.0.0.1:8080/api';

export async function apiGetParticipants(): Promise<TentParticipant[]> {
	const response = await fetch(base + '/participants')
		.then((res) => res.json())
		.then((res: Participant[]) => {
			const ret: TentParticipant[] = [];
			for (let i = 0; i < res.length; i++) {
				const p = new TentParticipant(
					res[i].id,
					res[i].firstname,
					res[i].lastname,
					res[i].zipcode,
					res[i].village,
					res[i].birthdate[0],
					res[i].friends
				);
				ret.push(p);
			}

			return ret;
		})
		.catch((error: Error) => {
			console.error(error);
			return [];
		});

	return response;
}
