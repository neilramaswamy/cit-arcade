import Head from 'next/head';
import { ApiClient } from '@/api/api';
import { useCallback, useEffect } from 'react';
import { Button } from 'types';
import { throttle } from 'lodash';

export default function Home() {
    function onButtonClick(buttonNumber: number) {
        console.log('Button clicked: ' + buttonNumber);
        ApiClient.sendRequest('/nes', buttonNumber);
    }

    // TODO(neil): fix this warning: rebuild
    const handleKeyPress = useCallback(
        throttle(
            (event: KeyboardEvent) => {
                console.log(`Key pressed: ${event.key}`);
                switch (event.key) {
                    case 'ArrowUp':
                    case 'w':
                        onButtonClick(Button.Up);
                        break;
                    case 'ArrowLeft':
                    case 'a':
                        onButtonClick(Button.Left);
                        break;
                    case 'ArrowDown':
                    case 's':
                        onButtonClick(Button.Down);
                        break;
                    case 'ArrowRight':
                    case 'd':
                        onButtonClick(Button.Right);
                        break;
                    case 'Escape':
                    case 'j':
                        onButtonClick(Button.A);
                        break;
                    case 'Enter':
                    case 'k':
                        onButtonClick(Button.B);
                        break;
                }
            },
            100,
            { leading: true }
        ),
        []
    );

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
                                onClick={() => onButtonClick(Button.Up)}
                            />
                        </div>
                        <div className="flex justify-center">
                            <button
                                className="h-16 w-16 bg-neutral-400 rounded-l-lg"
                                onClick={() => onButtonClick(Button.Left)}
                            />
                            <div className="h-16 w-16 bg-neutral-400" />
                            <button
                                className="h-16 w-16 bg-neutral-400 rounded-r-lg"
                                onClick={() => onButtonClick(Button.Right)}
                            />
                        </div>
                        <div className="flex justify-center">
                            <button
                                className="h-16 w-16 bg-neutral-400 rounded-b-lg"
                                onClick={() => onButtonClick(Button.Down)}
                            />
                        </div>
                    </div>

                    {/*Middle Buttons*/}
                    <div>
                        <div className="flex justify-center space-x-4">
                            <button
                                className="h-6 w-16 bg-neutral-400 rounded-full"
                                onClick={() => onButtonClick(Button.Select)}
                            />
                            <button
                                className="h-6 w-16 bg-neutral-400 rounded-full"
                                onClick={() => onButtonClick(Button.Start)}
                            />
                        </div>
                    </div>

                    {/*Side Buttons*/}
                    <div>
                        <div className="flex justify-center space-x-4">
                            <button
                                className="h-16 w-16 bg-red-600 rounded-full"
                                onClick={() => onButtonClick(Button.A)}
                            />
                            <button
                                className="h-16 w-16 bg-red-600 rounded-full"
                                onClick={() => onButtonClick(Button.B)}
                            />
                        </div>
                    </div>
                </div>
            </main>
        </>
    );
}
