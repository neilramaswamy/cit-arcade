import join from 'url-join';
import { ControlButton } from 'types';

const getAPIClient = () => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
    console.log(`API URL is ${apiUrl}`);

    const sendRequest = async (
        method: string,
        path: string,
        payload: Object,
        authToken: string = localStorage.getItem('authToken') ?? ''
    ) => {
        const destination = join(apiUrl, path);

        const requestOptions = {
            method,
            body: JSON.stringify({
                ...payload,
                authToken,
            }),
        };

        const response = await fetch(destination, requestOptions);
        return response;
    };

    return {
        sendRequest,
    };
};

export const ApiClient = getAPIClient();
