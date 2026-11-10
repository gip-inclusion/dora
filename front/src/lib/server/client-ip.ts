import { FRONT_PROXY_SECRET } from "$app/env/private";
import { API_URL } from "#lib/env.ts";

// En-têtes relatifs à l'IP du client reçus du navigateur : ils ne doivent pas
// être relayés au back, qui ne ferait pas la différence avec ceux du front.
const CLIENT_IP_HEADERS = [
  "x-forwarded-for",
  "x-real-ip",
  "forwarded",
  "x-dora-client-ip",
  "x-dora-proxy-secret",
];

// Transmet au back l'IP du client, authentifiée par le secret partagé
// FRONT_PROXY_SECRET, pour qu'il l'utilise comme identité de rate limiting et
// dans ses logs. X-Forwarded-For est réécrit avec cette IP, pour ne pas relayer
// les adresses fournies par le navigateur.
export function setClientIpHeaders(headers: Headers, clientAddress: string) {
  CLIENT_IP_HEADERS.forEach((header) => headers.delete(header));
  headers.set("X-Forwarded-For", clientAddress);
  if (FRONT_PROXY_SECRET) {
    headers.set("X-Dora-Client-Ip", clientAddress);
    headers.set("X-Dora-Proxy-Secret", FRONT_PROXY_SECRET);
  }
}

export function isApiRequest(url: string) {
  return new URL(url).origin === new URL(API_URL).origin;
}
