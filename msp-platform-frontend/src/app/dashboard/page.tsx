"use client";
import { useAuth0 } from "@auth0/auth0-react";
import { useEffect, useState } from "react";
import axios from "axios";

export default function Dashboard() {
  const { user, isAuthenticated, getAccessTokenSilently } = useAuth0();
  const [data, setData] = useState(null);

  useEffect(() => {
    if (isAuthenticated) {
      const fetchData = async () => {
        try {
          const token = await getAccessTokenSilently();
          const response = await axios.get("http://54.166.194.14:8000/client-data", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          setData(response.data);
        } catch (error) {
          console.error("Error fetching data", error);
        }
      };
      fetchData();
    }
  }, [isAuthenticated, getAccessTokenSilently]);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      {isAuthenticated ? (
        <div>
          <p>Welcome, {user?.name}!</p>
          <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
      ) : (
        <p>Please log in.</p>
      )}
    </div>
  );
}
