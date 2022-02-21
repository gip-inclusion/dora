<script>
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import PasswordForm from "./_password-form.svelte";
  import UserinfoForm from "./_userinfo-form.svelte";
</script>

<svelte:head>
  <title>Mon profil | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <CenteredGrid --col-bg="var(--col-gray-00)" topPadded>
    <div class="col-span-full col-start-1 mb-s80">
      <div class="mb-s32">
        <h2>Mon profil</h2>
      </div>
      <div class="border-t border-gray-03" />
      <div class="flex flex-col gap-s24 xl:flex-row">
        <div class="flex-1">
          <UserinfoForm />
        </div>
        <div class="flex-1">
          <PasswordForm />
        </div>
      </div>
    </div>
  </CenteredGrid>
</EnsureLoggedIn>
