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
