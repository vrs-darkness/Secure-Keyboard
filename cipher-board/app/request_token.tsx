import { useEffect, useState } from "react";
import { Platform, Alert } from "react-native";
import * as Notifications from "expo-notifications";
import * as Device from "expo-device";


class DeviceInfo {
  deviceName!: string;
  token!: string;
};

async function registerForPushNotificationsAsync() {
  let token;

  // Check if the device supports push notifications
  if (!Device.isDevice) {
    Alert.alert("Must use a physical device for Push Notifications");
    return;
  }

  // Request user's permissions
  const { status: existingStatus } = await Notifications.getPermissionsAsync();
  let finalStatus = existingStatus;

  if (existingStatus !== "granted") {
    const { status } = await Notifications.requestPermissionsAsync();
    finalStatus = status;
  }

  if (finalStatus !== "granted") {
    Alert.alert("Permission not granted for push notifications!");
    return;
  }

  // Get the FCM token (only works if you added Firebase)
  token = (await Notifications.getExpoPushTokenAsync()).data;
  console.log("Device Token:", token); // 📌 This is your token

  return token;
}



async function sendTokenToServer(deviceInfo: DeviceInfo) {
  const response = await fetch(`${process.env.SERVER_URL}/register-device`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(deviceInfo),
  });

  if (!response.ok) {
    throw new Error("Failed to register device");
  }

  console.log("Device registered successfully");
}




export default function App() {
  const [deviceToken, setDeviceToken] = useState<string | null>(null);

  useEffect(() => {
    registerForPushNotificationsAsync().then((token) => {
      if (token) {
        setDeviceToken(token);
        sendTokenToServer({
          deviceName: Device.deviceName ?? 'Unknown Device',
          token: token,
        });
      }
    });
  }, []);

  return null;
}
