<script>
  import { eyeFillIcon, eyeOffIcon } from "$lib/icons";

  export let value = "";

  export let name;
  export let autocomplete;
  export let passwordrules;

  export let readonly = false;
  export let disabled = false;
  export let placeholder = "";

  let passwdVisible = false;
  let passwdType = "password";

  function handlePasswordRevealClick() {
    passwdVisible = !passwdVisible;
    passwdType = passwdVisible ? "text" : "password";
  }

  // Pour rendre le mdp visible, on veut pouvoir changer le type de l'input
  // de `password` a `text`
  // Mais Svelte ne permet pas d'avoir un type dynamique et du binding bidirectionnel
  // en même temps, il faut donc mettre à jour la variable manuellement
  // https://stackoverflow.com/a/57393751
  const handlePasswordFieldInput = (e) => {
    value = e.target.value;
  };
</script>

<div class="flex items-center">
  <input
    class="w-full"
    {name}
    id={name}
    on:blur
    on:input={handlePasswordFieldInput}
    {value}
    type={passwdType}
    {placeholder}
    {disabled}
    {readonly}
    {autocomplete}
    {passwordrules}
  />
  <div
    class="absolute right-s16 h-s24 w-s24 fill-current text-gray-text-alt2"
    on:click={handlePasswordRevealClick}
  >
    {@html passwdVisible ? eyeOffIcon : eyeFillIcon}
  </div>
</div>

<style lang="postcss">
  input[type="text"],
  input[type="password"] {
    @apply rounded border border-gray-03 px-s12 py-s6 text-f14 placeholder-gray-text-alt outline-none focus:shadow-focus;
  }
</style>
