import { join } from "path";

const getAPIClient = () => {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "";
  console.log(`API URL is ${apiUrl}`);

  const sendRequest = async (path: string) => {
    const response = await fetch(join(apiUrl, path));
    return response;
  };

  return {
    sendRequest,
  };
};

export const ApiClient = getAPIClient();
