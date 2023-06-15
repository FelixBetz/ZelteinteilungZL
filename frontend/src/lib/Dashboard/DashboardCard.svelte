<script lang="ts">
	export let title = '';
	export let icon = '';
	export let bgColor = '';
	export let color = '';
	export let isSmallTitle = false;
	export let classes = '';
</script>

<div class="card {color} shadow-lg">
	<div class="card-header {bgColor} m-0 p-0 ps-2 pt-2 {classes}" style="--bs-bg-opacity: 0.7;">
		{#if isSmallTitle}
			<h5>
				{#if icon != ''}
					<i class={icon} />
				{/if}

				{title}
			</h5>
		{:else}
			<h3>
				{#if icon != ''}
					<i class={icon} />
				{/if}

				{title}
			</h3>
		{/if}
	</div>
	<div class="card-body rounded-bottom" style="--bs-bg-opacity: 0.4;">
		<slot />
	</div>
</div>
