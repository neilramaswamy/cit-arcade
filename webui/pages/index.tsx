import Head from 'next/head';
import { ApiClient } from '@/api/api';
import { useCallback, useEffect } from 'react';

const BUTTON = {
    UP: 1,
    DOWN: 2,
    LEFT: 3,
    RIGHT: 4,
    A: 5,
    B: 6,
    SELECT: 7,
    START: 8,
};

export default function Home() {
    function onButtonClick(buttonNumber: number) {
        console.log('Button clicked: ' + buttonNumber);
        // ApiClient.sendRequest("/up");
    }

    const handleKeyPress = useCallback((event: KeyboardEvent) => {
        console.log(`Key pressed: ${event.key}`);
        switch (event.key) {
            case 'ArrowUp':
            case 'w':
                onButtonClick(BUTTON.UP);
                break;
            case 'ArrowLeft':
            case 'a':
                onButtonClick(BUTTON.LEFT);
                break;
            case 'ArrowDown':
            case 's':
                onButtonClick(BUTTON.DOWN);
                break;
            case 'ArrowRight':
            case 'd':
                onButtonClick(BUTTON.RIGHT);
                break;
            case 'Escape':
            case 'j':
                onButtonClick(BUTTON.A);
                break;
            case 'Enter':
            case 'k':
                onButtonClick(BUTTON.B);
                break;
        }
    }, []);

    useEffect(() => {
        // attach the event listener
        document.addEventListener('keydown', handleKeyPress);

        // remove the event listener
        return () => {
            document.removeEventListener('keydown', handleKeyPress);
        };
    }, [handleKeyPress]);

    return (
        <>
            <Head>
                <title>The CIT Arcade</title>
                <meta name="description" content="Made with <3 by NSZ" />
                <meta
                    name="viewport"
                    content="width=device-width, initial-scale=1"
                />
                <link rel="icon" href="/favicon.ico" />
            </Head>

            <main>
                <h2>The CIT Arcade</h2>

                <div className="flex justify-between items-end max-w-2xl p-8 bg-gray-100 mx-auto">
                    {/*D Pad*/}
                    <div>
                        <div className="flex justify-center">
                            <button
                                className="h-16 w-16 bg-neutral-400 rounded-t-lg"
                                onClick={() => onButtonClick(BUTTON.UP)}
                            />
                        </div>
                        <div className="flex justify-center">
                            <button
                                className="h-16 w-16 bg-neutral-400 rounded-l-lg"
                                onClick={() => onButtonClick(BUTTON.LEFT)}
                            />
                            <div className="h-16 w-16 bg-neutral-400" />
                            <button
                                className="h-16 w-16 bg-neutral-400 rounded-r-lg"
                                onClick={() => onButtonClick(BUTTON.RIGHT)}
                            />
                        </div>
                        <div className="flex justify-center">
                            <button
                                className="h-16 w-16 bg-neutral-400 rounded-b-lg"
                                onClick={() => onButtonClick(BUTTON.DOWN)}
                            />
                        </div>
                    </div>

                    {/*Middle Buttons*/}
                    <div>
                        <div className="flex justify-center space-x-4">
                            <button
                                className="h-6 w-16 bg-neutral-400 rounded-full"
                                onClick={() => onButtonClick(BUTTON.SELECT)}
                            />
                            <button
                                className="h-6 w-16 bg-neutral-400 rounded-full"
                                onClick={() => onButtonClick(BUTTON.START)}
                            />
                        </div>
                    </div>

                    {/*Side Buttons*/}
                    <div>
                        <div className="flex justify-center space-x-4">
                            <button
                                className="h-16 w-16 bg-red-600 rounded-full"
                                onClick={() => onButtonClick(BUTTON.A)}
                            />
                            <button
                                className="h-16 w-16 bg-red-600 rounded-full"
                                onClick={() => onButtonClick(BUTTON.B)}
                            />
                        </div>
                    </div>
                </div>
            </main>
        </>
    );
}
