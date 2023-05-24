import { ApiClient } from '@/api/api';
import { PostUserPasswordResponse } from '@/types';
import { useRouter } from 'next/router';
import { useState } from 'react';

export default function Home() {
    const router = useRouter();
    const [password, setPassword] = useState('');

    const onPasswordSubmit = async (): Promise<void> => {
        // Store a copy of the password since after the request, password could have
        // been modified (accidental keystrokes)
        const passwordToSend = password;

        const response = await ApiClient.sendRequest(
            'POST',
            '/user/password',
            {},
            passwordToSend
        );

        if (response.status === 401) {
            alert('Invalid password! Try again.');
        } else if (response.status === 200) {
            localStorage['authToken'] = passwordToSend;

            const json = (await response.json()) as PostUserPasswordResponse;
            router.push(`/control?playerIndex=${json.playerIndex}`);
        }
    };

    return (
        // Center the div vertically; full-width on mobile, 500px maximum thereafter
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-800 sm:px-6 lg:px-8">
            <div className="w-full sm:w-96 flex items-start flex-col p-5 justify-center">
                <h2 className="text-4xl mb-3 font-extrabold tracking-tight text-white sm:text-5xl">
                    The CIT Arcade
                </h2>

                <input
                    type="number"
                    placeholder="Enter your token..."
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="p-2 mb-3 rounded-md"
                />

                <input
                    type="submit"
                    onClick={onPasswordSubmit}
                    className="bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4 border-b-4 border-blue-700 hover:border-blue-500 rounded"
                />
            </div>
        </div>
    );
}
