import { BASE_URL } from './api';

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

export async function apiGetTentLeader(): Promise<cTentLeader[]> {
	const response = await fetch(BASE_URL + '/tentleaders')
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

interface Revision {
	fullname: string;
	id: number;
	isError: boolean;
	newValue: string;
	oldValue: string;
	property: string;
	errorMessage: string;
}

export interface Logs {
	errors: string[];
	revisions: Revision[];
}

export async function apiGetLogs(): Promise<Logs> {
	const response = await fetch(BASE_URL + '/logs')
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
	const response = await fetch(BASE_URL + '/maps', {
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
	group: string;
	x?: number;
	y?: number;
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
	const response = await fetch(BASE_URL + '/graph')
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
