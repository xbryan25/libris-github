import { io } from "socket.io-client";

export default defineNuxtPlugin(() => {
  const baseURL = import.meta.env.VITE_API_URL;
  
  const socket = io(baseURL, {
    transports: ["websocket"], 
    reconnection: true,
    reconnectionAttempts: Infinity,
    reconnectionDelay: 1000,
  });

  return {
    provide: {
      socket,
    },
  };
});