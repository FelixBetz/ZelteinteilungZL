<script lang="ts">
	import { getStrTwoDecimal } from '$lib/helpers';

	export let bgColor = '';
	export let percentage = 0;
	export let height = 30;
	export let classes = '';
</script>

<div class="progress {classes}" style="height:{height}px">
	<div
		class="progress-bar {bgColor}"
		role="progressbar"
		style="width: {percentage}%; font-size: 200%"
	>
		{getStrTwoDecimal(percentage)}%
	</div>
</div>
