export function useSocketLogout(oldUserId: string): void {
  const { $socket } = useNuxtApp();

  if (!$socket.connected) {
    $socket.once("connect", () => {
      $socket.emit("leave", { userId: oldUserId });
    });
  } else {
    $socket.emit("leave", { userId: oldUserId });
  }
}