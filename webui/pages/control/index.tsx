import Head from 'next/head';
import { ApiClient } from '@/api/api';
import { createRef, useCallback, useEffect, useRef } from 'react';
import { ControlButton } from 'types';
import { throttle } from 'lodash';
import { useRouter } from 'next/router';
import { useSwipeable } from 'react-swipeable';

export default function Control() {
    const router = useRouter();

    const handlers = useSwipeable({
        onSwipedLeft: () => {
            onButtonClick(ControlButton.Left);
        },
        onSwipedRight: () => {
            onButtonClick(ControlButton.Right);
        },
        onSwipedDown: () => {
            onButtonClick(ControlButton.Down);
        },
        onSwipedUp: () => {
            onButtonClick(ControlButton.Up);
        },
    });

    const ref = useRef<HTMLDivElement>();

    const refPassthrough = (el: HTMLDivElement) => {
        // call useSwipeable ref prop with el
        handlers.ref(el);

        // set myRef el so you can access it yourself
        ref.current = el;
    };

    async function onButtonClick(button: number) {
        console.log('Button clicked: ' + button);
        const response = await ApiClient.sendRequest('POST', '/user/control', {
            button,
        });

        if (response?.status === 401) {
            alert('Your turn is up! Wait for another code to play again.');
            router.push('/');
        }
    }

    const playerIndex = router.query['playerIndex'] ?? null;

    // TODO(neil): fix this warning: rebuild
    const handleKeyPress = useCallback(
        throttle(
            (event: KeyboardEvent) => {
                console.log(`Key pressed: ${event.key}`);
                switch (event.key) {
                    case 'ArrowUp':
                    case 'w':
                        onButtonClick(ControlButton.Up);
                        break;
                    case 'ArrowLeft':
                    case 'a':
                        onButtonClick(ControlButton.Left);
                        break;
                    case 'ArrowDown':
                    case 's':
                        onButtonClick(ControlButton.Down);
                        break;
                    case 'ArrowRight':
                    case 'd':
                        onButtonClick(ControlButton.Right);
                        break;
                    case ' ':
                    case 'Enter':
                        onButtonClick(ControlButton.Select);
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

            <div
                ref={refPassthrough}
                className="h-full flex flex-col bg-gray-800 items-center justify-center"
            >
                <div className="flex justify-between items-end max-w-2xl p-8 bg-gray-100 mx-auto rounded-lg mb-3">
                    {/*D Pad*/}
                    <div>
                        <div className="flex justify-center">
                            <button
                                className="h-16 w-16 bg-neutral-400 rounded-t-lg"
                                onClick={() => onButtonClick(ControlButton.Up)}
                            />
                        </div>
                        <div className="flex justify-center">
                            <button
                                className="h-16 w-16 bg-neutral-400 rounded-l-lg"
                                onClick={() =>
                                    onButtonClick(ControlButton.Left)
                                }
                            />
                            <div className="h-16 w-16 bg-neutral-400" />
                            <button
                                className="h-16 w-16 bg-neutral-400 rounded-r-lg"
                                onClick={() =>
                                    onButtonClick(ControlButton.Right)
                                }
                            />
                        </div>
                        <div className="flex justify-center">
                            <button
                                className="h-16 w-16 bg-neutral-400 rounded-b-lg"
                                onClick={() =>
                                    onButtonClick(ControlButton.Down)
                                }
                            />
                        </div>
                    </div>

                    {/*Middle Buttons*/}
                    <div className="ml-10 mr-10">
                        <div className="flex justify-center space-x-4">
                            <button
                                className="h-6 w-16 bg-neutral-400 rounded-full"
                                onClick={() =>
                                    onButtonClick(ControlButton.Pause)
                                }
                            >
                                Pause
                            </button>
                        </div>
                    </div>

                    {/*Side Buttons*/}
                    <div>
                        <div className="flex justify-center space-x-4">
                            <button
                                className="h-16 w-16 bg-red-600 rounded-full"
                                onClick={() =>
                                    onButtonClick(ControlButton.Select)
                                }
                            >
                                A
                            </button>
                        </div>
                    </div>
                </div>

                {/* Player status */}
                {playerIndex !== null && (
                    <h3 className="text-3xl text-white">
                        Player {playerIndex}{' '}
                    </h3>
                )}
            </div>
        </>
    );
}
