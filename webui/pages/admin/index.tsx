import { ApiClient } from '@/api/api';
import {
    PostAdminGetPasswordsResponse,
    PostAdminRotatePasswordsResponse,
} from '@/types';
import { useCallback, useEffect, useState } from 'react';

export default function Admin() {
    const [passwords, setPasswords] = useState<string[]>([]);

    useEffect(() => {
        (async () => {
            const response = await ApiClient.sendRequest(
                'POST',
                '/admin/passwords',
                {}
            );
            if (response) {
            }

            if (response.status === 200) {
                const json =
                    (await response.json()) as PostAdminGetPasswordsResponse;
                setPasswords(json.authTokens);
            }
        })();
    }, []);

    const doRotatePasswords = useCallback(async () => {
        const response = await ApiClient.sendRequest(
            'POST',
            '/admin/rotate',
            {}
        );

        if (response.status === 401) {
            const authToken = prompt(
                'Admin authentication invalid. You might consider providing a correct password: '
            );

            if (authToken === null) {
                return;
            }

            localStorage['authToken'] = authToken;
            doRotatePasswords();
        } else if (response.status === 200) {
            const json =
                (await response.json()) as PostAdminRotatePasswordsResponse;
            setPasswords(json.authTokens);
        }
    }, []);

    return (
        <div className="flex flex-col items-center h-full bg-gray-800 text-white p-6">
            <h1 className="text-4xl">Admin Panel</h1>

            <div className="mb-2">
                {passwords.length ? (
                    <ul>
                        {passwords.map((pw, i) => {
                            return (
                                <li key={pw} className="text-xl">
                                    Player {i + 1}: {pw}
                                </li>
                            );
                        })}
                    </ul>
                ) : (
                    'No passwords!'
                )}
            </div>

            <button
                className="p-6 bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4 border-b-4 border-blue-700 hover:border-blue-500 rounded"
                onClick={doRotatePasswords}
            >
                Refresh Passwords
            </button>
        </div>
    );
}
