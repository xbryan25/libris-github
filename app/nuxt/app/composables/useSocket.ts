
const paymentSuccess = ref<number | null>(null);
const updateUnreadNotificationsCount = ref<number | null>(null)

let isInitialized = false;
let currentUserId: string | null = null

export function useSocket(userId: string | null) {

  const { $socket } = useNuxtApp();

  currentUserId = userId;

  if (!isInitialized) {

    $socket.on("payment_success", (data) => {
      paymentSuccess.value = data.readitsAmount;
    });

    $socket.on("update_unread_notifications_count", (data) => {
      updateUnreadNotificationsCount.value = data.unreadNotificationsCount;
    });

    $socket.on("disconnect", () => {
      console.log("Socket disconnected, will try to reconnect");
    });

    $socket.on("connect_error", () => {
      console.log("Connection error, trying to reconnect...");
    });

    $socket.on("reconnect", () => {
      if (currentUserId) $socket.emit("join", { user_id: currentUserId });
    });

    if (userId) {
      if ($socket.connected) {
        $socket.emit("join", { userId });
      } else {
        $socket.once("connect", () => {
          $socket.emit("join", { userId });
        });
      }
    }

    isInitialized = true;
  } else {
    currentUserId = userId
  }

  return { paymentSuccess, updateUnreadNotificationsCount };
}