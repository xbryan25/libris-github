import { io } from "socket.io-client";

const baseURL = import.meta.env.VITE_API_URL;

const socket = io(baseURL, {
  transports: ["websocket"], 
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 1000,
});

const paymentSuccess = ref<number | null>(null);
let isInitialized = false;

export function useSocket(userId: string) {
  if (!isInitialized) {
    socket.on("connect", () => {
      console.log("Socket connected:", socket.id);
      socket.emit("join", { user_id: userId });
    });

    socket.on("payment_success", (data) => {
      paymentSuccess.value = data.readits_amount;
    });

    socket.on("disconnect", () => {
      console.log("Socket disconnected, will try to reconnect");
    });

    socket.on("connect_error", () => {
      console.log("Connection error, trying to reconnect...");
    });

    isInitialized = true;
  } else {
    socket.emit("join", { user_id: userId });
  }

  return { socket, paymentSuccess };
}