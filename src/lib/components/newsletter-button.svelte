<script>
  import { newspaperIcon } from "$lib/icons";
  import LinkButton from "./link-button.svelte";
  export let extraClass = "";
  export let wFull = false;
</script>

<LinkButton
  label="S’abonner à l’infolettre"
  icon={newspaperIcon}
  iconOnRight
  secondary
  {extraClass}
  {wFull}
  to="https://d4c653e7.sibforms.com/serve/MUIEAEkY4naptXBIq5NdRg5UPxP1wmwbGCinne5c1gynY-wfrZ0Dz0QP_NqkXtfyYqhdaq3AO8VFZJ9giRi9ZT0eah7Ut2U0LeKSTVIHQb_5nhvTLUMWXo9ZMeIYCHVlzmjkXGQ66S5ewcYpSADUgV--2RVZ_mrnsRJQoCNwZ8y-sWzfQsEzfKuTA7SLbZ_dWeqaigudym3EaiHT"
  otherTab
  nofollow
/>
