import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyD6AQun59-EJCgA7qzxMxBJj9BmKsWZrPw",
  authDomain: "royal-fitness-club-7adc1.firebaseapp.com",
  projectId: "royal-fitness-club-7adc1",
  storageBucket: "royal-fitness-club-7adc1.firebasestorage.app",
  messagingSenderId: "116269953135",
  appId: "1:116269953135:web:e9c815a1e62788fbd05d9a",
  measurementId: "G-T2XRQFKLRE"
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const db = getFirestore(app);

export default app;
