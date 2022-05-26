/* global tarteaucitron, ga, Shareaholic, stLight, clicky, top, google, Typekit, FB, ferankReady, IN, stButtons, twttr, PCWidget*/
/* jslint regexp: true, nomen: true*/

// generic iframe
tarteaucitron.services.iframe = {
    "key": "iframe",
    "type": "other",
    "name": "Web content",
    "uri": "",
    "needConsent": true,
    "cookies": [],
    "js" () {

        tarteaucitron.fallback(['tac_iframe'], (x) => {
            const frame_title = tarteaucitron.fixSelfXSS(x.getAttribute("title")),
                width = x.getAttribute("width"),
                height = x.getAttribute("height"),
                allowfullscreen = x.getAttribute("allowfullscreen"),
                url = x.getAttribute("data-url");

            return `<iframe title="${  frame_title  }" src="${  url  }" width="${  width  }" height="${  height  }" scrolling="no" allowtransparency${  allowfullscreen == '0' ? '' : ' webkitallowfullscreen mozallowfullscreen allowfullscreen'  }></iframe>`;
        });
    },
    "fallback" () {

        const id = 'iframe';
        tarteaucitron.fallback(['tac_iframe'], (elem) => {
            elem.style.width = `${elem.getAttribute('width')  }px`;
            elem.style.height = `${elem.getAttribute('height')  }px`;
            return tarteaucitron.engage(id);
        });
    }
};


// crisp
tarteaucitron.services.crisp = {
    "key": "crisp",
    "type": "other",
    "name": "Crisp Chat",
    "uri": "https://help.crisp.chat/en/article/crisp-chatbox-cookie-ip-policy-1147xor/",
    "needConsent": true,
    "cookies": ['crisp-client', '__cfduid'],
    "js": function () {
        "use strict";

        if (tarteaucitron.user.crispID === undefined) {
            return;
        }

        window.$crisp = [];
        window.CRISP_WEBSITE_ID = tarteaucitron.user.crispID;

        tarteaucitron.addScript('https://client.crisp.chat/l.js');
    }
};
