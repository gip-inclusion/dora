/* global tarteaucitron, tarteaucitronForceLanguage */

tarteaucitronForceLanguage = "fr";
tarteaucitron.init({
  lang: "fr",
  privacyUrl: "/privacy" /* Privacy policy url */,

  hashtag: "#tarteaucitron" /* Open the panel with this hashtag */,
  cookieName: "tarteaucitron" /* Cookie name */,

  orientation: "bottom" /* Banner position (top - bottom) */,

  groupServices: false /* Group services by category */,

  showAlertSmall: false /* Show the small banner on bottom right */,
  cookieslist: false /* Show the cookie list */,

  closePopup: true /* Show a close X on the banner */,

  showIcon: true /* Show cookie icon to manage cookies */,
  // "iconSrc": "", /* Optionnal: URL or base64 encoded image */
  iconPosition:
    "BottomRight" /* BottomRight, BottomLeft, TopRight and TopLeft */,

  adblocker: false /* Show a Warning if an adblocker is detected */,

  DenyAllCta: true /* Show the deny all button */,
  AcceptAllCta: true /* Show the accept all button when highPrivacy on */,
  highPrivacy: true /* HIGHLY RECOMMANDED Disable auto consent */,

  handleBrowserDNTRequest: true /* If Do Not Track == 1, disallow all */,

  removeCredit: false /* Remove credit link */,
  moreInfoLink: true /* Show more info link */,

  useExternalCss: false /* If false, the tarteaucitron.css file will be loaded */,
  useExternalJs: false /* If false, the tarteaucitron.js file will be loaded */,

  readmoreLink: "" /* Change the default readmore link */,

  mandatory: false /* Show a message about mandatory cookies */,
});
