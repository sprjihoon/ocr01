import axios from "axios";
import { useAuth } from "../context/AuthContext";

const BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export const apiClient = () => {
  const { token } = useAuth();
  const client = axios.create({ baseURL: BASE_URL });
  client.interceptors.request.use((config) => {
    if (token) config.headers["Authorization"] = `Bearer ${token}`;
    return config;
  });
  return client;
}; 