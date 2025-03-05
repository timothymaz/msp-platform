"use client";
import { useAuth0 } from "@auth0/auth0-react";

export default function Home() {
  const { loginWithRedirect, logout, user, isAuthenticated } = useAuth0();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      {!isAuthenticated ? (
        <button
          onClick={() => loginWithRedirect()}
          className="px-6 py-2 text-white bg-blue-500 rounded-lg"
        >
          Log In
        </button>
      ) : (
        <div className="text-center">
          <h1 className="text-2xl font-bold">Welcome, {user?.name}!</h1>
          <button
            onClick={() => logout({ returnTo: "http://localhost:3000" })}
            className="mt-4 px-6 py-2 text-white bg-red-500 rounded-lg"
          >
            Log Out
          </button>
        </div>
      )}
    </div>
  );
}
