<script>
  import { arrowRightSIcon } from "$lib/icons.js";
  export let label = "";
  export let details = "";
  export let type = "button";
  export let name = null;

  export let disabled = false;
</script>

<button
  {type}
  {name}
  class="px-3 py-3/2 text-sm leading-normal border text-gray-01 border-gray-01 flex flex-row items-center justify-between text-left rounded focus:shadow-focus outline-none"
  on:click
  {disabled}>
  <div>
    <h4 class="pb-1">{label}</h4>
    <p class="text-gray-text-alt2 text-sm">{details}</p>
  </div>
  <div class="w-3 h-3 ml-1 fill-current">
    {@html arrowRightSIcon}
  </div>
</button>
