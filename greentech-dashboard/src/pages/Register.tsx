import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/api";
import bg from "../assets/bg2.png";
import logo from "../assets/logo.png";

export default function Register() {
  const nav = useNavigate();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [pwd, setPwd] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    setLoading(true);
    try {
      await api.post("/register", {
        username: username.trim(),
        email: email.trim(),
        password: pwd.trim(),
      });
      alert("Registered successfully!");
      nav("/dashboard", { replace: true });
    } catch (e: any) {
      alert(e.response?.data?.detail ?? "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="">
      <div
        className="rounded-xl shadow-lg p-5 w-full max-w-2xl text-center bg-cover bg-center relative"
        style={{
          backgroundImage: `url(${bg})`,
        }}
      >
        {/* Back Button */}
        <button
          onClick={() => nav(-1)}
          className="absolute top-6 left-6 text-white text-xl font-bold"
        >
          ←
        </button>

        {/* Logo */}
        <img src={logo} className="w-36 mx-auto mb-4" />

        {/* Title */}
        <h2 className="text-3xl font-bold text-green-900 mb-8">Register</h2>

        {/* Username */}
        <input
          className="w-full max-w-sm mx-auto mb-4 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        {/* Email */}
        <input
          className="w-full max-w-sm mx-auto mb-4 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        {/* Password */}
        <input
          type="password"
          className="w-full max-w-sm mx-auto mb-6 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
          placeholder="Password"
          value={pwd}
          onChange={(e) => setPwd(e.target.value)}
        />

        {/* Button or Loader */}
        {loading ? (
          <div className="text-green-900 font-semibold">Loading...</div>
        ) : (
          <button
            className="px-6 py-2 rounded-md text-white font-semibold"
            style={{ backgroundColor: "#275C29" }}
            onClick={submit}
          >
            REGISTER
          </button>
        )}
      </div>
    </div>
  );
}
