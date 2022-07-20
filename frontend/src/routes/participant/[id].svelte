<script lang="ts">
	import { apiGetParticipant } from '$lib/_apiParticipants';

	import type { cTentParticipant } from '$lib/_apiParticipants';

	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { Container, Input, Row, Col, Form, FormGroup } from 'sveltestrap/src';

	let participant: cTentParticipant | null = null;

	async function getParticipant(id: number) {
		participant = await apiGetParticipant(id);
		console.log(participant);
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
				<Col><h1>{participant.getFullname() + ' (Zelt X)'}</h1></Col>
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
							bind:value={participant.birthdateStr}
						/>
						<div slot="label">birthdate</div>
					</FormGroup>
				</Col>
			</Row>
			<Row>
				<h3>Adresse:</h3>
				<Col>
					<FormGroup floating>
						<Input placeholder="Enter street" />
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
					<Row>
						<h3>Kontaktdaten:</h3>
						<Col>
							<FormGroup floating>
								<Input type="email" />
								<div slot="label">mail</div>
							</FormGroup>
						</Col>
						<Col>
							<FormGroup floating>
								<Input placeholder="Enter phone number" />
								<div slot="label">phone</div>
							</FormGroup>
						</Col>
					</Row>
				</Col>

				<Col>
					<Row>
						<h3>Notfallkontakt:</h3>
						<Col>
							<FormGroup floating>
								<Input />
								<div slot="label">name</div>
							</FormGroup>
						</Col>
						<Col>
							<FormGroup floating>
								<Input placeholder="Enter phone number" />
								<div slot="label">phone</div>
							</FormGroup>
						</Col>
					</Row>
				</Col>
			</Row>

			<Row>
				<Col>
					<Row>
						<h3>Mit wem möchte ich ins Zelt:</h3>
						<Row>
							<Col>
								<FormGroup floating>
									<Input placeholder="Enter name" />
									<div slot="label">friend1</div>
								</FormGroup>
							</Col>
						</Row>
						<Row>
							<Col>
								<FormGroup floating>
									<Input placeholder="Enter name" />
									<div slot="label">friend2</div>
								</FormGroup>
							</Col>
						</Row>
					</Row>
				</Col>
				<Col>
					<Row>
						<h3>todo:</h3>
						<Col>
							<FormGroup floating>
								<Input type="checkbox" label="ermäßigt" />
							</FormGroup>
						</Col>
						<Col>
							<FormGroup floating>
								<Input type="checkbox" label="fotografieren" />
							</FormGroup>
						</Col>
						<Col>
							<FormGroup floating>
								<Input type="checkbox" label="Tochter Afe" />
							</FormGroup>
						</Col>
						<Col>
							<FormGroup floating>
								<Input type="checkbox" label="verteiler" />
							</FormGroup>
						</Col>
					</Row>
				</Col>
			</Row>

			<Row>
				<h3>Sonstiges:</h3>
				<Col><Input rows={1} type="textarea" bind:inner on:input={resize} /></Col>
			</Row>
		</Form>
	</Container>
{/if}
