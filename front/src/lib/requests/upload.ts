import { getApiURL } from "$lib/utils/api";
import { getToken } from "$lib/utils/auth";

export async function deleteFile(fileName: string) {
  const encodedFileName = encodeURIComponent(fileName);
  const url = `${getApiURL()}/delete-upload/${encodedFileName}/`;

  const method = "DELETE";
  const res = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      Authorization: `Token ${getToken()}`,
    },
  });

  return res.ok;
}
