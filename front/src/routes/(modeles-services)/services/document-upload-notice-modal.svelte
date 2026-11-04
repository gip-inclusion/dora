<script lang="ts">
  import Modal from "#lib/components/hoc/modal.svelte";
  import CloseLineSystem from "svelte-remix/CloseLineSystem.svelte";
  import Button from "#lib/components/display/button.svelte";

  interface Props {
    isOpen: boolean;
    onConfirm: () => void;
  }

  let { isOpen = $bindable(false), onConfirm }: Props = $props();
</script>

<Modal {isOpen} hideCloseButton hideTitle hideOverflow width="medium">
  <div class="flex flex-col overflow-hidden">
    <Button
      extraClass="self-end"
      label="Fermer"
      onclick={() => (isOpen = false)}
      icon={CloseLineSystem}
      iconOnRight
      noBackground
      noPadding
    />
    <h2>Notice d’informations&#8239;: Pièces justificatives</h2>
    <h6 class="text-gray-text">
      Toute demande de pièces justificatives est réglementée. Veuillez prendre
      connaissance de la notice suivante&#8239;:
    </h6>
    <div class="mt-s16 border-gray-02 border-1">
      <div class=" p-s16 gap-s16 flex max-h-[24rem] flex-col overflow-y-scroll">
        <div class="flex flex-col items-center justify-center">
          <h4 class="text-france-blue mb-s0">Notice d’information</h4>
          <h4 class="text-france-blue mb-s0">Pièces justificatives</h4>
        </div>
        <div>
          <h4 class="text-france-blue">
            Suis-je responsable des données&#8239;?
          </h4>
          <div class="flex justify-center">
            <div
              class="bg-service-violet p-s16 mr-s16 flex flex-col items-center justify-center rounded-md"
            >
              <h4 class="text-france-blue">📥 Je reçois une orientation</h4>
              <p class="text-f14 text-gray-text">
                Vous êtes considéré comme le <strong
                  >responsable de traitement</strong
                >. C’est vous qui déterminez quelles pièces et données sont
                nécessaires pour valider l’orientation.
              </p>
            </div>
            <div
              class="bg-service-violet p-s16 flex flex-col items-center justify-center rounded-md"
            >
              <h4 class="text-france-blue">📤 J’aide à une orientation</h4>
              <p class="text-f14 text-gray-text">
                Vous n’êtes pas le responsable principal. Vous intégrez les
                données, mais c’est l’organisme récepteur qui les traite et en
                est responsable.
              </p>
            </div>
          </div>
        </div>
        <div>
          <h4>Qu’en est-il du GIP Plateforme de l’inclusion&#8239;?</h4>
          <p class="text-f14 text-gray-text">
            Il est co-responsable de traitement, car il décide notamment
            d’éléments importants comme les durées de conservation et certaines
            modalités.
          </p>
        </div>
        <div>
          <h4>Quelles pièces justificatives puis-je demander&#8239;?</h4>
          <p class="text-f14 text-gray-text">
            Pour respecter le principe de minimisation du RGPD. Les données
            doivent être nécessaires pour savoir si l’orientation vers vous est
            valable. Elles ne doivent pas conduire à une pré-inscription qui
            devra se faire directement auprès de vous.
          </p>
        </div>
        <div
          class="bg-service-violet p-s16 gap-s8 flex flex-col items-center justify-center rounded-md"
        >
          <h5 class="text-france-blue">À faire</h5>
          <div class="mx-s64">
            <div class="flex justify-between">
              <span class="mr-s16">✅</span>
              <p class="text-f14 text-gray-text">
                <b>Identifier le bénéficiaire&#8239;:</b> Demander des pièces qui
                prouvent que le bénéficiaire fait partie du public que vous accompagnez.
              </p>
            </div>
            <div class="flex justify-between">
              <span class="mr-s16">✅</span>
              <p class="text-f14 text-gray-text">
                <b>Se concentrer sur le bénéficiaire&#8239;: </b>
                Ne collecter des données sur des tiers que si c’est indispensable
                pour l’orientation et si vous pouvez les informer.
              </p>
            </div>
          </div>
        </div>
        <div
          class="bg-service-violet p-s16 gap-s8 flex flex-col items-center justify-center rounded-md"
        >
          <h5 class="text-france-blue">À éviter</h5>
          <div class="mx-s64 flex justify-between">
            <span class="mr-s16">❌</span>
            <p class="text-f14 text-gray-text">
              <b>La pré-inscription&#8239;: </b>
              Ne pas utiliser Dora pour des pré-inscriptions. Ces démarches doivent
              se faire directement auprès de votre organisme.
            </p>
          </div>
        </div>
        <h4 class="m-s0">
          Et le rôle du GIP Plateforme de l’Inclusion&#8239;?
        </h4>
        <div
          class="bg-service-violet p-s16 gap-s8 flex flex-col items-center justify-center rounded-md"
        >
          <h5 class="text-france-blue">Le rôle de Vigie du GIP</h5>
          <div class="mx-s64 flex justify-between">
            <span class="mr-s16">🛡️</span>
            <p class="text-f14 text-gray-text">
              Le GIP assure une veille. De manière aléatoire ou en cas de doute,
              il peut vous contacter pour comprendre la justification de la
              demande d’une pièce justificative.
            </p>
          </div>
        </div>
        <div>
          <h4 class="text-france-blue">
            Certaines données sont-elles interdites dans Dora&#8239;?
          </h4>
          <p class="text-f14 text-gray-text">
            Pour des raisons de sécurité notamment, les RIB, les cartes vitales
            et le NIR ne peuvent être traités sur Dora, et toute donnée sensible
            qui n’est pas indispensable.
          </p>
        </div>
        <div>
          <h4 class="text-france-blue">
            Qui peut avoir accès aux fiches d’orientation&#8239;?
          </h4>
          <p class="text-f14 text-gray-text">
            Il revient à chaque organisme de déterminer qui a accès aux fiches
            et aux pièces justificatives. Si l’organisme a plusieurs comptes,
            par défaut, n’ouvrez pas l’accès à toute personne de votre
            organisation sans raison. Cela respectera le principe de
            minimisation et renforcera la sécurité des données.
          </p>
          <p class="text-f14 text-gray-text">
            Chacune doit répondre dans un délai raisonnable.
          </p>
        </div>
        <div class="border-gray-02 pb-s8 border-b-1">
          <h4 class="text-france-blue">
            Quels sont les droits des personnes&#8239;?
          </h4>
          <p class="text-f14 text-gray-text">
            Les bénéficiaires peuvent s’opposer au traitement de leurs données,
            y compris dans le cadre d’orientation. S’ils en font la demande, les
            données ne sont plus utilisées et il peut être procédé à la
            suppression des données.
          </p>
        </div>
        <div class="bg-service-violet p-s16 rounded-md">
          <h4 class="m-s0">Pour en savoir plus&#8239;…</h4>
          <ul class="p-s16 list-disc">
            <li class="m-s0 text-f14 text-gray-text">
              La <a
                class="text-magenta-cta"
                href="/politique-de-confidentialite"
                target="_blank"
                rel="noopener nofollow">politique de confidentialité de Dora</a
              >
            </li>
            <li class="m-s0 text-f14 text-gray-text">
              L'<a
                class="text-magenta-cta"
                href="/cgu#accord_co_responsabilite"
                target="_blank"
                rel="noopener nofollow">accord de co-responsabilité</a
              > entre le GIP et vous
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
  <div class="mt-s16 pt-s16 border-gray-02 pb-s8 flex justify-end border-t-1">
    <Button
      id="document-upload-notice-accept-button"
      label="J’ai compris"
      onclick={onConfirm}
    />
  </div>
</Modal>
