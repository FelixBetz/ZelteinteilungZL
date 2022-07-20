interface Participant {
	street: string;
	birthdate: string;
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
	other: string;
	tent: number;
}

export class cTentParticipant {
	public age = 0;
	constructor(
		public identifier: number,
		public firstname: string,
		public lastname: string,
		public street: string,
		public zipcode: number,
		public village: string,
		public birthdate: string,
		public phone: string,
		public mail: string,
		public emergency_contact: string,
		public emergency_phone: string,
		public is_afe: boolean,
		public is_event_mail: boolean,
		public is_photo_allowed: boolean,
		public is_reduced: boolean,
		public friends: string[],
		public other: string,
		public tent: number
	) {
		this.calculateAge();
	}

	private calculateAge() {
		const today = new Date();

		const [day, month, year] = this.birthdate.split('.');
		const birthDate = new Date(+year, +month - 1, +day); //(0 = January to 11 = December)
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
						res[i].street,
						res[i].zipcode,
						res[i].village,
						res[i].birthdate,
						res[i].phone,
						res[i].mail,
						res[i].emergency_contact,
						res[i].emergency_phone,
						res[i].is_afe,
						res[i].is_event_mail,
						res[i].is_photo_allowed,
						res[i].is_reduced,
						res[i].friends,
						res[i].other,
						res[i].tent
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
				res.street,
				res.zipcode,
				res.village,
				res.birthdate,
				res.phone,
				res.mail,
				res.emergency_contact,
				res.emergency_phone,
				res.is_afe,
				res.is_event_mail,
				res.is_photo_allowed,
				res.is_reduced,
				res.friends,
				res.other,
				res.tent
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
