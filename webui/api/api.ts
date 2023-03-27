import join from "url-join";

const getAPIClient = () => {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "";
  console.log(`API URL is: ${apiUrl}`);

  const sendRequest = async (path: string) => {
    const destination = join(apiUrl, path);

    console.log(`Joined path is ${destination}`);
    const response = await fetch(destination);
    return response;
  };

  return {
    sendRequest,
  };
};

export const ApiClient = getAPIClient();
