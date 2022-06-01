<script lang="ts">
	import { apiGetParticipants } from './participants/_apiParticipants';

	import { Button } from 'sveltestrap/src';
	let errors: { [inputName: string]: any } = {};

	function isFormValid(data: { [inputName: string]: any }): boolean {
		return !Object.keys(errors).some((inputName) =>
			Object.keys(errors[inputName]).some((errorName) => errors[inputName][errorName])
		);
	}

	function validateForm(data: { [inputName: string]: any }): void {
		if (!isRequiredFieldValid(data.email)) {
			errors['email'] = { ...errors['email'], required: true };
		} else {
			errors['email'] = { ...errors['email'], required: false };
		}

		if (!isRequiredFieldValid(data.name)) {
			errors['name'] = { ...errors['name'], required: true };
		} else {
			errors['name'] = { ...errors['name'], required: false };
		}
	}

	function isRequiredFieldValid(value) {
		return value != null && value !== '';
	}
	let result = null;
	let foo = 'baz';
	let bar = 'qux';
	async function onSubmit(e) {
		const formData = new FormData(e.target);

		const data: any = {};
		for (let field of formData) {
			const [key, value] = field;
			data[key] = value;
		}

		validateForm(data);

		if (isFormValid(data)) {
			console.log(data);
			const res = await fetch('http://127.0.0.1:8080/api/test', {
				method: 'POST',
				body: JSON.stringify({
					foo,
					bar
				})
			});

			const json = await res.json();
			result = JSON.stringify(json);
		} else {
			console.log('Invalid Form');
		}
	}
</script>

<form on:submit|preventDefault={onSubmit}>
	<div>
		<label for="email">Email</label>
		<input type="text" id="email" name="email" value="" />
		{#if errors.email && errors.email.required}
			<p class="error-message">Email is required</p>
		{/if}
	</div>
	<div>
		<label for="name">Name</label>
		<input type="text" id="name" name="name" value="" />
		{#if errors.name && errors.name.required}
			<p class="error-message">Name is required</p>
		{/if}
	</div>
	<button type="submit">Submit</button>
</form>
