const content = `
Contact: mailto:service.securite@gip-inclusion.org
Policy: https://inclusion.beta.gouv.fr/.well-known/security-policy.txt
Preferred-Languages: fr, en
Expires: 2027-01-01T00:00:00.000Z
Encryption: https://inclusion.beta.gouv.fr/.well-known/pdi-pgp.asc
`.trim();

export function GET() {
  return new Response(content, {
    headers: { "content-type": "text/plain" },
  });
}
