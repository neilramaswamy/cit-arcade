import { join } from "path";

const getAPIClient = () => {
  console.log(process.env);
  const apiUrl = process.env.API_URL || "";

  const sendRequest = async (path: string) => {
    const response = await fetch(join(apiUrl, path));
    return response;
  };

  return {
    sendRequest,
  };
};

export const ApiClient = getAPIClient();
