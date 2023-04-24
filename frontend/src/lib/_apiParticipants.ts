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
		public tent: number
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

interface TentLeader {
	identifier: number;
	firstname: string;
	lastname: string;
	birthdate: string;
	street: string;
	zipcode: number;
	village: string;
	mail: string;
	phone: string;
	handy: string;
	job: string;
	team: string;
	tent: number;
	comment: string;
}

export class cTentLeader {
	public age = 0;
	constructor(
		public identifier: number,
		public firstname: string,
		public lastname: string,
		public birthdate: string,
		public street: string,
		public zipcode: number,
		public village: string,
		public mail: string,
		public phone: string,
		public handy: string,
		public job: string,
		public team: string,
		public tent: number,
		public comment: string
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

export const baseUrl = 'http://127.0.0.1:8080/api';

export async function apiGetParticipants(): Promise<cTentParticipant[]> {
	const response = await fetch(baseUrl + '/participants')
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

export async function apiGetParticipant(arg_id: number): Promise<cTentParticipant | null> {
	const response = await fetch(baseUrl + '/participant?id=' + arg_id)
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
		p.tent
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
		paid: p.paid
	};
	return participant;
}

function tentleaderInterfaceToParticipantObject(p: TentLeader): cTentLeader {
	const tentParticipant: cTentLeader = new cTentLeader(
		p.identifier,
		p.firstname,
		p.lastname,
		p.birthdate,
		p.street,
		p.zipcode,
		p.village,
		p.mail,
		p.phone,
		p.handy,
		p.job,
		p.team,
		p.tent,
		p.comment
	);
	return tentParticipant;
}

export async function apiPostParticipant(
	arg_participant: cTentParticipant | null
): Promise<cTentParticipant | null> {
	if (arg_participant == null) {
		return null;
	}

	const participant = participantObjectToParticipantInterface(arg_participant);
	const formData = new FormData();
	formData.append('participant', JSON.stringify(participant));
	const response = await fetch(baseUrl + '/participant?id=' + participant.identifier, {
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
	arg_participant: cTentParticipant[]
): Promise<cTentParticipant[]> {
	if (arg_participant.length == 0) {
		return [];
	}

	const participants: Participant[] = [];
	for (let i = 0; i < arg_participant.length; i++) {
		const participant = participantObjectToParticipantInterface(arg_participant[i]);
		participants.push(participant);
	}
	const formData = new FormData();
	formData.append('participants', JSON.stringify(participants));
	const response = await fetch(baseUrl + '/participants', {
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

export async function apiGetTentLeader(): Promise<cTentLeader[]> {
	const response = await fetch(baseUrl + '/tentleaders')
		.then((res) => res.json())
		.then((res: TentLeader[]) => {
			const ret: cTentLeader[] = [];
			for (let i = 0; i < res.length; i++) {
				ret.push(tentleaderInterfaceToParticipantObject(res[i]));
			}
			return ret;
		})
		.catch((error: Error) => {
			console.error(error);
			return [];
		});

	return response;
}

export interface Logs {
	errors: string[];
	revisions: string[];
}

export async function apiGetLogs(): Promise<Logs> {
	const response = await fetch(baseUrl + '/logs')
		.then((res) => res.json())
		.then((res: Logs) => {
			return res;
		})
		.catch((error: Error) => {
			console.error(error);
			const ret: Logs = { errors: [], revisions: [] };
			return ret;
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
export interface GraphInput {
	friends: string[];
	name: string;
}

export interface INode {
	id: string;
	group: number;
}
export interface ILink {
	source: string;
	target: string;
	value: number;
}

export interface IData {
	nodes: INode[];
	links: ILink[];
}
export async function apiGetGraph(): Promise<GraphInput[]> {
	const response = await fetch(baseUrl + '/graph')
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
