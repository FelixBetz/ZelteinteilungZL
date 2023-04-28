<script lang="ts">
	export let title = '';
	export let icon = '';
	export let color = '';
</script>

<div class="card {color}">
	<div class="card-header">
		<h3>
			{#if icon != ''}
				<i class={icon} />
			{/if}

			{title}
		</h3>
	</div>
	<div class="card-body">
		<slot />
	</div>
</div>
