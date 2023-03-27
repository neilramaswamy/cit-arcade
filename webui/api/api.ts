import { join } from "path";

const getAPIClient = () => {
  console.log(process.env);
  const remoteURL = process.env.remoteURL || "";

  const sendRequest = async (path: string) => {
    const response = await fetch(join(remoteURL, path));
    return response;
  };

  return {
    sendRequest,
  };
};

export const ApiClient = getAPIClient();
