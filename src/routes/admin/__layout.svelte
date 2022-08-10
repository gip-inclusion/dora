<script context="module">
  import { token, userInfo } from "$lib/auth";
  import { get } from "svelte/store";

  export async function load({ url }) {
    const myToken = get(token);
    if (!myToken) {
      return {
        status: 302,
        redirect: `/auth/connexion?next=${encodeURIComponent(url.pathname)}`,
      };
    }

    const user = get(userInfo);

    if (!user?.isStaff) {
      return {
        status: 403,
        error: "Accès réservé",
      };
    }

    return {
      props: {},
    };
  }
</script>

<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
</script>

<svelte:head>
  <meta name="robots" content="noindex" />
</svelte:head>

<CenteredGrid>
  <h1><a href="/admin">Interface d'administration</a></h1>
  <slot />
</CenteredGrid>
