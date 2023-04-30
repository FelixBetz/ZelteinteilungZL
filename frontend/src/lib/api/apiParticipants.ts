import { BASE_URL } from './api';

interface Participant {
	street: string;
	birthdate: string;
	emergency_contact: string;
	emergency_phone: string;
	firstname: string;
	friends: string[];
	identifier: number;
	is_vegetarian: boolean;
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
	paid: boolean;
	registered: string;
}

export class cTentParticipant {
	public age = 0;
	constructor(
		public identifier: number,
		public paid: boolean,
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
		public is_vegetarian: boolean,
		public is_event_mail: boolean,
		public is_photo_allowed: boolean,
		public is_reduced: boolean,
		public friends: string[],
		public other: string,
		public tent: number,
		public registered: string
	) {
		this.calculateAge();
	}

	private calculateAge() {
		const today = new Date();

		const [year, month, day] = this.birthdate.split('-');
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

export async function apiGetParticipants(): Promise<cTentParticipant[]> {
	const response = await fetch(BASE_URL + '/participants')
		.then((res) => res.json())
		.then((res: Participant[]) => {
			const ret: cTentParticipant[] = [];
			for (let i = 0; i < res.length; i++) {
				ret.push(partipantInterfaceToParticipantObject(res[i]));
			}
			return ret;
		})
		.catch((error: Error) => {
			console.error(error);
			return [];
		});

	return response;
}

export async function apiGetParticipant(pId: number): Promise<cTentParticipant | null> {
	const response = await fetch(BASE_URL + '/participant?id=' + pId)
		.then((res) => res.json())
		.then((res: Participant) => {
			const ret: cTentParticipant = partipantInterfaceToParticipantObject(res);

			return ret;
		})
		.catch((error: Error) => {
			console.error(error);
			return null;
		});

	return response;
}

function partipantInterfaceToParticipantObject(p: Participant): cTentParticipant {
	const tentParticipant: cTentParticipant = new cTentParticipant(
		p.identifier,
		p.paid,
		p.firstname,
		p.lastname,
		p.street,
		p.zipcode,
		p.village,
		p.birthdate,
		p.phone,
		p.mail,
		p.emergency_contact,
		p.emergency_phone,
		p.is_vegetarian,
		p.is_event_mail,
		p.is_photo_allowed,
		p.is_reduced,
		p.friends,
		p.other,
		p.tent,
		p.registered
	);
	return tentParticipant;
}

function participantObjectToParticipantInterface(p: cTentParticipant): Participant {
	const participant: Participant = {
		street: p.street,
		birthdate: p.birthdate,
		emergency_contact: p.emergency_contact,
		emergency_phone: p.emergency_phone,
		firstname: p.firstname,
		friends: p.friends,
		identifier: p.identifier,
		is_vegetarian: p.is_vegetarian,
		is_event_mail: p.is_event_mail,
		is_photo_allowed: p.is_photo_allowed,
		is_reduced: p.is_reduced,
		lastname: p.lastname,
		mail: p.mail,
		phone: p.phone,
		village: p.village,
		zipcode: p.zipcode,
		other: p.other,
		tent: p.tent,
		paid: p.paid,
		registered: p.registered
	};
	return participant;
}

export async function apiPostParticipant(
	pParticipant: cTentParticipant | null
): Promise<cTentParticipant | null> {
	if (pParticipant == null) {
		return null;
	}

	const participant = participantObjectToParticipantInterface(pParticipant);
	const formData = new FormData();
	formData.append('participant', JSON.stringify(participant));
	const response = await fetch(BASE_URL + '/participant?id=' + participant.identifier, {
		method: 'POST',
		body: formData
	})
		.then((res) => res.json())
		.then((res: Participant) => {
			const ret: cTentParticipant = partipantInterfaceToParticipantObject(res);

			return ret;
		})
		.catch((error: Error) => {
			console.error(error);
			return null;
		});

	return response;
}

export async function apiPostParticipants(
	pParticipant: cTentParticipant[]
): Promise<cTentParticipant[]> {
	if (pParticipant.length == 0) {
		return [];
	}

	const participants: Participant[] = [];
	for (let i = 0; i < pParticipant.length; i++) {
		const participant = participantObjectToParticipantInterface(pParticipant[i]);
		participants.push(participant);
	}
	const formData = new FormData();
	formData.append('participants', JSON.stringify(participants));
	const response = await fetch(BASE_URL + '/participants', {
		method: 'POST',
		body: formData
	})
		.then((res) => res.json())
		.then((res: Participant[]) => {
			const ret: cTentParticipant[] = [];
			for (let i = 0; i < res.length; i++) {
				ret.push(partipantInterfaceToParticipantObject(res[i]));
			}

			return ret;
		})
		.catch((error: Error) => {
			console.error(error);
			return [];
		});

	return response;
}

export async function apiGetParticipantsLastYear(): Promise<string[]> {
	const response = await fetch(BASE_URL + '/participants/last-year')
		.then((res) => res.json())
		.then((res: string[]) => {
			return res;
		})
		.catch((error: Error) => {
			console.error(error);
			return [];
		});

	return response;
}
