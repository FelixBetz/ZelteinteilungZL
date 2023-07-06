<script lang="ts">
	import { apiGetGenerateOverallList } from '$lib/api/apiLists';

	async function generatateOverallList() {
		await apiGetGenerateOverallList().then((x) => console.log(x));
	}
</script>

<div class="container-fluid">
	<div class="row">
		<div class="col-sm-3">
			<div
				class="btn btn-primary"
				on:click={generatateOverallList}
				on:keydown={generatateOverallList}
			>
				Generate Overall List
			</div>
		</div>
	</div>
</div>
