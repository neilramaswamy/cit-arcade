import Head from "next/head";
import Image from "next/image";
import { Inter } from "@next/font/google";
import styles from "@/styles/Home.module.css";
import { ApiClient } from "@/api/api";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  return (
    <>
      <Head>
        <title>The CIT Arcade</title>
        <meta name="description" content="Made with <3 by NSZ" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h2>The CIT Arcade</h2>

        <div>
          <button
            onClick={() => {
              ApiClient.sendRequest("/up");
            }}
          >
            Go up
          </button>
        </div>

        <div>
          <button
            onClick={() => {
              ApiClient.sendRequest("/down");
            }}
          >
            Go down
          </button>
        </div>
      </main>
    </>
  );
}
