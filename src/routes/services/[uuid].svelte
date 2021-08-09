<script context="module">
  import { getApiURL } from "$lib/utils";

  export async function load({ page, fetch, _session, _context }) {
    const url = `${getApiURL()}/services/${page.params.uuid}/`;
    const res = await fetch(url, {
      headers: {
        Accept: "application/json; version=1.0",
      },
    });

    if (res.ok) {
      const service = await res.json();
      return {
        props: {
          service,
        },
      };
    }
    return {
      status: res.status,
      error: new Error(`Could not load ${url}`),
    };
  }
</script>

<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  export let service;
</script>

<svelte:head>
  <title>Dora: {service.name}</title>
</svelte:head>

<CenteredGrid>
  <div class="col-start-1 col-span-full">
    <h1>{service.name}</h1>

    <strong>id : </strong>{service.id} <br />
    <strong>name : </strong>{service.name} <br />
    <strong>shortDesc : </strong>{service.shortDesc} <br />
    <strong>fullDesc : </strong>{service.fullDesc} <br />
    <strong>kinds : </strong>{service.kinds} <br />
    <strong>categories : </strong>{service.categories} <br />
    <strong>subcategories : </strong>{service.subcategories} <br />
    <strong>isCommonLaw : </strong>{service.isCommonLaw} <br />
    <strong>isCumulative : </strong>{service.isCumulative} <br />
    <strong>hasFee : </strong>{service.hasFee} <br />
    <strong>feeDetails : </strong>{service.feeDetails} <br />
    <strong
      >beneficiariesAccessModes :
    </strong>{service.beneficiariesAccessModes}
    <br />
    <strong
      >beneficiariesAccessModesOther :
    </strong>{service.beneficiariesAccessModesOther} <br />
    <strong>coachOrientationModes : </strong>{service.coachOrientationModes}
    <br />
    <strong
      >coachOrientationModesOther :
    </strong>{service.coachOrientationModesOther}
    <br />
    <strong>forms : </strong>{service.forms} <br />
    <strong>onlineForms : </strong>{service.onlineForms} <br />
    <strong>contactName : </strong>{service.contactName} <br />
    <strong>contactPhone : </strong>{service.contactPhone} <br />
    <strong>contactEmail : </strong>{service.contactEmail} <br />
    <strong>contactUrl : </strong>{service.contactUrl} <br />
    <strong>isContactInfoPublic : </strong>{service.isContactInfoPublic} <br />
    <strong>locationKind : </strong>{service.locationKind} <br />
    <strong>remoteUrl : </strong>{service.remoteUrl} <br />
    <strong>address1 : </strong>{service.address1} <br />
    <strong>address2 : </strong>{service.address2} <br />
    <strong>postalCode : </strong>{service.postalCode} <br />
    <strong>cityCode : </strong>{service.cityCode} <br />
    <strong>city : </strong>{service.city} <br />
    <strong>longitude : </strong>{service.longitude} <br />
    <strong>latitude : </strong>{service.latitude} <br />
    <strong>isTimeLimited : </strong>{service.isTimeLimited} <br />
    <strong>startDate : </strong>{service.startDate} <br />
    <strong>endDate : </strong>{service.endDate} <br />
    <strong>recurrence : </strong>{service.recurrence} <br />
    <strong>recurrenceOther : </strong>{service.recurrenceOther} <br />
    <strong>suspensionCount : </strong>{service.suspensionCount} <br />
    <strong>suspensionDate : </strong>{service.suspensionDate} <br />
    <strong>creationDate : </strong>{service.creationDate} <br />
    <strong>modificationDate : </strong>{service.modificationDate} <br />
    <strong>structure : </strong>{service.structure} <br />
    <strong>creator : </strong>{service.creator} <br />
    <strong>lastEditor : </strong>{service.lastEditor} <br />
    <strong>accessConditions : </strong>{service.accessConditions} <br />
    <strong>concernedPublic : </strong>{service.concernedPublic} <br />
    <strong>requirements : </strong>{service.requirements} <br />
    <strong>credentials : </strong>{service.credentials} <br />
  </div>
</CenteredGrid>
