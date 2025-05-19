import axios from "axios";

export const api = axios.create({
  baseURL: "https://backendappdev.onrender.com",
});

export const bearer =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
