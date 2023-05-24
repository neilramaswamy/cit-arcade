import '@/styles/globals.css';
import { AppProps } from 'next/app';
import { VT323 } from 'next/font/google';

const vt323 = VT323({
    weight: '400',
    subsets: ['latin'],
});

export default function App({ Component, pageProps }: AppProps) {
    return (
        <main className={`${vt323.className} h-full`}>
            <Component {...pageProps} />
        </main>
    );
}
