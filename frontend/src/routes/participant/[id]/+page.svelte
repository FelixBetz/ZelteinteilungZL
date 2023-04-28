<script lang="ts">
	import { apiGetParticipant, apiPostParticipant } from '$lib/_apiParticipants';

	import type { cTentParticipant } from '$lib/_apiParticipants';

	import { onMount } from 'svelte';
	import { page } from '$app/stores';

	let participant: cTentParticipant | null = null;
	let inputRegisteredValue: string;

	function parseDatimeTimeStr(argParticipant: cTentParticipant | null): string {
		if (argParticipant == null) {
			return '';
		}
		return argParticipant.registered.replace(' ', 'T');
	}

	$: inputRegisteredValue = parseDatimeTimeStr(participant);

	async function getParticipant(id: number) {
		participant = await apiGetParticipant(id);
	}

	async function postParticipant() {
		participant = await apiPostParticipant(participant);
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
	<div class="container">
		<form>
			<div class="row">
				<div class="col">
					<h1>{participant.getFullname() + ' (Zelt ' + participant.tent + ')'}</h1>
				</div>
			</div>
			<div class="row">
				<h3>Persönliche Infos:</h3>
				<div class="col">
					<div class="form-floating">
						<input
							type="text"
							class="form-control"
							id="participanId"
							placeholder="id"
							disabled
							bind:value={participant.identifier}
						/>
						<label for="participanId">Id</label>
					</div>
				</div>
				<div class="col">
					<div class="form-floating">
						<input
							type="text"
							class="form-control"
							id="firstname"
							placeholder="Enter firstname"
							bind:value={participant.firstname}
						/>
						<label for="firstname">Vorname</label>
					</div>
				</div>
				<div class="col">
					<div class="form-floating">
						<input
							type="text"
							class="form-control"
							id="lastname"
							placeholder="Enter lastname"
							bind:value={participant.lastname}
						/>
						<label for="lastname">Nachname</label>
					</div>
				</div>
				<div class="col">
					<div class="form-floating">
						<input
							class="form-control"
							type="date"
							placeholder="Enter birthdate"
							id="birthdate"
							bind:value={participant.birthdate}
						/>
						<label for="birthdate">Geburtstag</label>
					</div>
				</div>
			</div>
			<div class="row">
				<h3>Adresse:</h3>
				<div class="col">
					<div class="form-floating">
						<input
							class="form-control"
							type="text"
							id="street"
							placeholder="Enter street"
							bind:value={participant.street}
						/>

						<label for="street">Straße</label>
					</div>
				</div>
				<div class="col">
					<div class="form-floating">
						<input
							class="form-control"
							type="text"
							placeholder="Enter zipcode"
							id="zipcode"
							bind:value={participant.zipcode}
						/>
						<label for="zipcode">PLZ</label>
					</div>
				</div>
				<div class="col">
					<div class="form-floating">
						<input
							class="form-control"
							type="text"
							id="village"
							placeholder="Enter village"
							bind:value={participant.village}
						/>
						<label for="village">Ort</label>
					</div>
				</div>
			</div>
			<div class="row">
				<div class="col">
					<!--contact data-->
					<div class="row">
						<h3>Kontaktdaten:</h3>
						<div class="col">
							<div class="form-floating">
								<input class="form-control" type="email" id="mail" bind:value={participant.mail} />
								<label for="mail">Mail</label>
							</div>
						</div>
						<div class="col">
							<div class="form-floating">
								<input
									class="form-control"
									type="text"
									id="phone"
									placeholder="Enter phone number"
									bind:value={participant.phone}
								/>
								<label for="phone">Telefon</label>
							</div>
						</div>
					</div>
				</div>

				<div class="col">
					<!--emercency contact-->
					<div class="row">
						<h3>Notfallkontakt:</h3>
						<div class="col">
							<div class="form-floating">
								<input
									class="form-control"
									type="text"
									id="emergency_contact"
									bind:value={participant.emergency_contact}
								/>
								<label for="emergency_contact">Name</label>
							</div>
						</div>
						<div class="col">
							<div class="form-floating">
								<input
									class="form-control"
									type="text"
									id="emergency_phone"
									placeholder="Enter phone number"
									bind:value={participant.emergency_phone}
								/>
								<label for="emergency_phone">Telefon</label>
							</div>
						</div>
					</div>
				</div>
			</div>

			<div class="row">
				<div class="col">
					<!--friends-->
					<div class="row">
						<h3>Mit wem möchte ich ins Zelt:</h3>
						<div class="row">
							<div class="col">
								<div class="form-floating">
									<input
										class="form-control"
										type="text"
										placeholder="Enter name"
										id="friend1"
										bind:value={participant.friends[0]}
									/>
									<label for="friend1">Freund 1</label>
								</div>
							</div>
						</div>
						<div class="row">
							<div class="col pt-2">
								<div class="form-floating">
									<input
										class="form-control"
										type="text"
										placeholder="Enter name"
										id="friend2"
										bind:value={participant.friends[1]}
									/>
									<label for="friend2">Freund 2</label>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div class="col">
					<div class="row">
						<h3>&nbsp;</h3>
						<div class="col-sm-auto">
							<input
								type="checkbox"
								class="form-check-input"
								id="is_reduced"
								bind:checked={participant.is_reduced}
							/>
							<label for="is_reduced">ermäßigt</label>
						</div>
						<div class="col-sm-auto">
							<input
								type="checkbox"
								class="form-check-input"
								id="is_photo_allowed"
								bind:checked={participant.is_photo_allowed}
							/>
							<label for="is_photo_allowed">fotografieren</label>
						</div>
						<div class="col-sm-auto">
							<input
								type="checkbox"
								class="form-check-input"
								id="is_vegetarian"
								bind:checked={participant.is_vegetarian}
							/>
							<label for="is_vegetarian">Vegetarisch</label>
						</div>
						<div class="col-sm-auto">
							<input
								type="checkbox"
								class="form-check-input"
								id="is_event_mail"
								bind:checked={participant.is_event_mail}
							/>
							<label for="is_event_mail">Verteiler</label>
						</div>
						<div class="col-sm-auto">
							<input
								type="checkbox"
								class="form-check-input"
								id="paid"
								bind:checked={participant.paid}
							/>
							<label for="paid">bezahlt</label>
						</div>
					</div>

					<div class="col mt-3">
						<div class="form-floating">
							<input
								class="form-control"
								type="datetime-local"
								placeholder="Enter registered"
								id="registered"
								bind:value={inputRegisteredValue}
								on:change={() => {
									if (participant != undefined) {
										participant.registered = inputRegisteredValue.replace('T', ' ');
									}
								}}
							/>
							<label for="registered">Registriert</label>
						</div>
					</div>
				</div>
			</div>

			<div class="row">
				<h3>Sonstiges:</h3>
				<div class="col">
					<div class="form-floating">
						<textarea
							class="form-control"
							placeholder="Leave a comment here"
							bind:this={inner}
							bind:value={participant.other}
							on:input={resize}
						/>
						<label for="floatingTextarea">Sonstiges</label>
					</div>
				</div>
			</div>
		</form>
		<div class="row" style="margin-top: 20px">
			<div class="col-sm-12">
				<div class="btn btn-primary w-100" on:click={postParticipant} on:keydown={postParticipant}>
					Save
				</div>
			</div>
		</div>
	</div>
{/if}
