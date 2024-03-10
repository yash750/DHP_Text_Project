import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyAs3mfIDyJYMkyqzUUJnijaAKhd6hbEZXo",
  authDomain: "alpha-262f3.firebaseapp.com",
  projectId: "alpha-262f3",
  storageBucket: "alpha-262f3.appspot.com",
  messagingSenderId: "625645982946",
  appId: "1:625645982946:web:0869be283cb5533f74fabb",
  measurementId: "G-NY11DZRYX6"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const googleSignInBtn = document.getElementById('google-sign-in-btn');

const provider = new GoogleAuthProvider();
console.log("I wasa executed! before auth")
googleSignInBtn.addEventListener('click', () => {
  console.log("I wasa executed! before auth")
  signInWithPopup(auth, provider)
    .then((result) => {
      const user = result.user;
      console.log("I wasa executed!")
      console.log(`Signed in as ${user.displayName}`);
      location.replace('/index')
});
});

// const googleSignInBtn = document.getElementById('google-sign-in-btn');
// const provider = new GoogleAuthProvider();

// googleSignInBtn.addEventListener('click', () => {
//   signInWithPopup(auth, provider)
//     .then((result) => {
//       const user = result.user;
//       console.log(`Signed in as ${user.displayName}`);
      
//       // Update the redirect URL to include '/index'
//       location.replace('https://dhp-text-project.onrender.com/index');
//     })
//     .catch((error) => {
//       console.error('Google sign-in error:', error.message);
//     });
// });
