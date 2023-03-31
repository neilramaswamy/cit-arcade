import join from 'url-join';
import { Button } from 'types';

const getAPIClient = () => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
    console.log(`API URL is: ${apiUrl}`);

    const sendRequest = async (path: string, buttonNumber: Button) => {
        const destination = join(apiUrl, path);

        console.log(`Joined path is ${destination}`);

        const requestOptions = {
            method: 'POST',
            body: JSON.stringify({ button: buttonNumber }),
        };

        try {
            const response = await fetch(destination, requestOptions);
            return response;
        } catch (e) {
            console.error(`Error making fetch to ${destination}: ${e}`);
        }
    };

    return {
        sendRequest,
    };
};

export const ApiClient = getAPIClient();
