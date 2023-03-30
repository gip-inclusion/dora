/* global tarteaucitron, tarteaucitronForceLanguage */

tarteaucitronForceLanguage = "fr";

tarteaucitron.init({
  privacyUrl: "/politique-de-confidentialite" /* Privacy policy url */,
  cookieName: "tarteaucitron" /* Cookie name */,

  orientation: "bottom" /* Banner position (top - bottom) */,

  groupServices: false /* Group services by category */,

  showAlertSmall: false /* Show the small banner on bottom right */,
  cookieslist: false /* Show the cookie list */,

  showIcon: false /* Show cookie icon to manage cookies */,

  DenyAllCta: true /* Show the deny all button */,
  AcceptAllCta: true /* Show the accept all button when highPrivacy on */,
  highPrivacy: true /* HIGHLY RECOMMANDED Disable auto consent */,

  handleBrowserDNTRequest: true /* If Do Not Track == 1, disallow all */,

  removeCredit: false /* Remove credit link */,
  moreInfoLink: true /* Show more info link */,

  useExternalCss: false /* If false, the tarteaucitron.css file will be loaded */,
  useExternalJs: false /* If false, the tarteaucitron.js file will be loaded */,

  readmoreLink: "" /* Change the default readmore link */,

  mandatory: true /* Show a message about mandatory cookies */,
});


tarteaucitron.services.crispnoconsent = {
  // Basé sur https://github.com/AmauriC/tarteaucitron.js/pull/281
  // Le support par défaut de Tarte au Citron est insatisfaisant :
  // - acceptation par défaut
  // - mauvaise gestion des cookies dynamiques 'crisp-client/*'
  // TODO: tarte au citron ne gère pas les entrées dans le localStorage
  // qui devraient être effacées elles aussi.
  //
    "key": "crispnoconsent",
    "type": "support",
    "name": "Crisp (fenêtre de tchat)",
    "uri": "https://crisp.chat/fr",
    "readmoreLink": "https://help.crisp.chat/en/article/whats-crisp-eu-gdpr-compliance-status-nhv54c/",
    "needConsent": true,
    "cookies": ['crisp-client'],
    "js": function () {
        "use strict";
        if (tarteaucitron.user.crispID === undefined) {
            return;
        }

        window.$crisp = [];
        window.CRISP_WEBSITE_ID = tarteaucitron.user.crispID;

        tarteaucitron.addScript('https://client.crisp.chat/l.js');

        const interval = setInterval(function () {
            if (typeof $crisp === 'undefined') return
            clearInterval(interval);
            // boucle sur les cookies pour récupérer tous ceux qui commencent
            // par 'crisp-client'
            const theCookies = document.cookie.split(';');
            for (var i = 1 ; i <= theCookies.length; i++) {
                const cookie = theCookies[i - 1].split('=');
                const cookieName = cookie[0].trim();

                if (cookieName.indexOf('crisp-client') === 0) {
                    tarteaucitron.services.crispnoconsent.cookies.push(cookieName);
                }
            }
        }, 100)
    }
};
