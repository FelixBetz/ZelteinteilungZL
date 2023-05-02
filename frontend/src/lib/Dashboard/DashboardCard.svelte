<script lang="ts">
	export let title = '';
	export let icon = '';
	export let bgColor = '';
	export let color = '';
</script>

<div class="card {color} ">
	<div class="card-header {bgColor}" style="--bs-bg-opacity: 0.7;">
		<h3>
			{#if icon != ''}
				<i class={icon} />
			{/if}

			{title}
		</h3>
	</div>
	<div class="card-body rounded-bottom" style="--bs-bg-opacity: 0.4;">
		<slot />
	</div>
</div>

<style>
</style>
