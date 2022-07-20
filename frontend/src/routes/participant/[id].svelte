<script lang="ts">
	import { apiGetParticipant } from '$lib/_apiParticipants';

	import type { cTentParticipant } from '$lib/_apiParticipants';

	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { Container, Input, Row, Col, Form, FormGroup } from 'sveltestrap/src';

	let participant: cTentParticipant | null = null;
	let inputBirthdateValue: string;

	function parseTimeStr(argParticipant: cTentParticipant | null): string {
		if (argParticipant == null) {
			return '';
		}
		let splittedBitdateStr = argParticipant.birthdate.split('.');
		let y = splittedBitdateStr[2];
		let m = splittedBitdateStr[1];
		let d = splittedBitdateStr[0];
		inputBirthdateValue = y + '-' + m + '-' + d;
		return inputBirthdateValue;
	}

	$: inputBirthdateValue = parseTimeStr(participant);

	async function getParticipant(id: number) {
		participant = await apiGetParticipant(id);
	}

	onMount(() => {
		let id = parseInt($page.params['id']);
		getParticipant(id);
	});

	let inner: HTMLTextAreaElement;
	const resize = () => {
		inner.style.height = 'auto';
		inner.style.height = 4 + inner.scrollHeight + 'px';
	};
</script>

{#if participant != null}
	<Container>
		<Form>
			<Row>
				<Col><h1>{participant.getFullname() + ' (Zelt ' + participant.tent + ')'}</h1></Col>
			</Row>
			<Row>
				<h3>Persönliche Infos:</h3>
				<Col>
					<FormGroup floating label="Id">
						<Input disabled bind:value={participant.identifier} />
					</FormGroup>
				</Col>
				<Col>
					<FormGroup floating>
						<Input placeholder="Enter firstname" bind:value={participant.firstname} />
						<div slot="label">firstname</div>
					</FormGroup>
				</Col>
				<Col>
					<FormGroup floating>
						<Input placeholder="Enter lastname" bind:value={participant.lastname} />
						<div slot="label">lastname</div>
					</FormGroup>
				</Col>
				<Col>
					<FormGroup floating>
						<Input
							type="date"
							placeholder="Enter birthdate"
							bind:value={inputBirthdateValue}
							on:change={() => {
								let splittedBitdateStr = inputBirthdateValue.split('-');
								let y = splittedBitdateStr[0];
								let m = splittedBitdateStr[1];
								let d = splittedBitdateStr[2];
								if (participant != undefined) {
									participant.birthdate = d + '.' + m + '.' + y;
								}
							}}
						/>
						<div slot="label">birthdate</div>
					</FormGroup>
				</Col>
			</Row>
			<Row>
				<h3>Adresse:</h3>
				<Col>
					<FormGroup floating>
						<Input placeholder="Enter street" bind:value={participant.street} />
						<div slot="label">street</div>
					</FormGroup>
				</Col>
				<Col>
					<FormGroup floating>
						<Input placeholder="Enter zipcode" bind:value={participant.zipcode} />
						<div slot="label">zipcode</div>
					</FormGroup>
				</Col>
				<Col>
					<FormGroup floating>
						<Input placeholder="Enter village" bind:value={participant.village} />
						<div slot="label">village</div>
					</FormGroup>
				</Col>
			</Row>
			<Row>
				<Col>
					<!--contact data-->
					<Row>
						<h3>Kontaktdaten:</h3>
						<Col>
							<FormGroup floating>
								<Input type="email" bind:value={participant.mail} />
								<div slot="label">mail</div>
							</FormGroup>
						</Col>
						<Col>
							<FormGroup floating>
								<Input placeholder="Enter phone number" bind:value={participant.phone} />
								<div slot="label">phone</div>
							</FormGroup>
						</Col>
					</Row>
				</Col>

				<Col>
					<!--emercency contact-->
					<Row>
						<h3>Notfallkontakt:</h3>
						<Col>
							<FormGroup floating>
								<Input bind:value={participant.emergency_contact} />
								<div slot="label">name</div>
							</FormGroup>
						</Col>
						<Col>
							<FormGroup floating>
								<Input placeholder="Enter phone number" bind:value={participant.emergency_phone} />
								<div slot="label">phone</div>
							</FormGroup>
						</Col>
					</Row>
				</Col>
			</Row>

			<Row>
				<Col>
					<!--friends-->
					<Row>
						<h3>Mit wem möchte ich ins Zelt:</h3>
						<Row>
							<Col>
								<FormGroup floating>
									<Input placeholder="Enter name" bind:value={participant.friends[0]} />
									<div slot="label">friend1</div>
								</FormGroup>
							</Col>
						</Row>
						<Row>
							<Col>
								<FormGroup floating>
									<Input placeholder="Enter name" bind:value={participant.friends[1]} />
									<div slot="label">friend2</div>
								</FormGroup>
							</Col>
						</Row>
					</Row>
				</Col>
				<Col>
					<Row>
						<h3>&nbsp;</h3>
						<Col>
							<FormGroup floating>
								<Input type="checkbox" label="ermäßigt" bind:checked={participant.is_reduced} />
							</FormGroup>
						</Col>
						<Col>
							<FormGroup floating>
								<Input
									type="checkbox"
									label="fotografieren"
									bind:checked={participant.is_photo_allowed}
								/>
							</FormGroup>
						</Col>
						<Col>
							<FormGroup floating>
								<Input type="checkbox" label="Tochter Afe" bind:checked={participant.is_afe} />
							</FormGroup>
						</Col>
						<Col>
							<FormGroup floating>
								<Input type="checkbox" label="verteiler" bind:checked={participant.is_event_mail} />
							</FormGroup>
						</Col>
					</Row>
				</Col>
			</Row>

			<Row>
				<h3>Sonstiges:</h3>
				<Col
					><Input
						rows={1}
						type="textarea"
						bind:inner
						bind:value={participant.other}
						on:input={resize}
					/></Col
				>
			</Row>
		</Form>
	</Container>
{/if}
