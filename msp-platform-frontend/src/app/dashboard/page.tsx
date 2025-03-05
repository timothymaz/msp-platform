"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function DashboardPage() {
  const [user, setUser] = useState(null);
  const router = useRouter();

  useEffect(() => {
    // Get token from URL
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");

    if (code) {
      // Exchange code for access token
      fetch("http://localhost:8000/auth/callback")
        .then((res) => res.json())
        .then((data) => {
          if (data.access_token) {
            localStorage.setItem("auth_token", data.access_token);
            setUser(data.user);
          } else {
            router.push("/login");
          }
        })
        .catch(() => router.push("/login"));
    } else {
      // Try to get existing token
      const token = localStorage.getItem("auth_token");
      if (!token) {
        router.push("/login");
      } else {
        fetch("http://localhost:8000/auth/user", {
          headers: { Authorization: `Bearer ${token}` },
        })
          .then((res) => res.json())
          .then((data) => setUser(data.user))
          .catch(() => router.push("/login"));
      }
    }
  }, []);

  if (!user) return <p>Loading...</p>;

  return <h1>Welcome, {user.name}!</h1>;
}
