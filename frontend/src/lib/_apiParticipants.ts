interface Participant {
	address: string;
	birthdate: string[];
	emergency_contact: string;
	emergency_phone: string;
	firstname: string;
	friends: string[];
	identifier: number;
	is_afe: boolean;
	is_event_mail: boolean;
	is_photo_allowed: boolean;
	is_reduced: boolean;
	lastname: string;
	mail: string;
	phone: string;
	village: string;
	zipcode: number;
}

export class cTentParticipant {
	public age = 0;
	constructor(
		public identifier: number,
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

export const baseUrl = 'http://127.0.0.1:8080/api';

export async function apiGetParticipants(): Promise<cTentParticipant[]> {
	const response = await fetch(baseUrl + '/participants')
		.then((res) => res.json())
		.then((res: Participant[]) => {
			const ret: cTentParticipant[] = [];
			for (let i = 0; i < res.length; i++) {
				ret.push(
					new cTentParticipant(
						res[i].identifier,
						res[i].firstname,
						res[i].lastname,
						res[i].zipcode,
						res[i].village,
						res[i].birthdate[0],
						res[i].friends
					)
				);
			}

			return ret;
		})
		.catch((error: Error) => {
			console.error(error);
			return [];
		});

	return response;
}

export async function apiGetParticipant(arg_id: number): Promise<cTentParticipant | null> {
	const response = await fetch(baseUrl + '/participant?id=' + arg_id)
		.then((res) => res.json())
		.then((res: Participant) => {
			const ret: cTentParticipant = new cTentParticipant(
				res.identifier,
				res.firstname,
				res.lastname,
				res.zipcode,
				res.village,
				res.birthdate[0],
				res.friends
			);

			return ret;
		})
		.catch((error: Error) => {
			console.error(error);
			return null;
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
	const response = await fetch(baseUrl + '/maps', {
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
