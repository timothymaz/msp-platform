"use client";
import { Geist, Geist_Mono } from "next/font/google";
import { Auth0Provider } from "@auth0/auth0-react";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <Auth0Provider
      domain={process.env.NEXT_PUBLIC_AUTH0_DOMAIN as string}
      clientId={process.env.NEXT_PUBLIC_AUTH0_CLIENT_ID as string}
      authorizationParams={{
        redirect_uri: "http://localhost:3000/dashboard",
        audience: process.env.NEXT_PUBLIC_AUTH0_AUDIENCE as string,
        scope: "openid profile email",
      }}
    >
      <html lang="en">
        <body
          className={`${geistSans.variable} ${geistMono.variable} antialiased`}
        >
          {children}
        </body>
      </html>
    </Auth0Provider>
  );
}
