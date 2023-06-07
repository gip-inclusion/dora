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
