import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/api";
import bg from "../assets/bg2.png";
import logo from "../assets/logo.png";

export default function Login() {
  const nav = useNavigate();
  const [email, setEmail] = useState("");
  const [pwd, setPwd] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    setLoading(true);
    try {
      const r = await api.post("/token", new URLSearchParams({
        username: email.trim(),
        password: pwd.trim(),
        grant_type: "password",
      }));
      console.log("token:", r.data.access_token);
      nav("/dashboard", { replace: true });
    } catch (e: any) {
      alert(e.response?.data?.detail ?? "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="">
      <div
        className="rounded-xl shadow-lg p-10 w-full max-w-2xl text-center bg-cover bg-center"
        style={{
          backgroundImage: `url(${bg})`,
        }}
      >
        {/* Logo */}
        <img src={logo} className="w-36 mx-auto mb-4" />

        {/* Title */}
        <h2 className="text-3xl font-bold text-green-900 mb-8">Welcome Back</h2>

        {/* Email Input */}
        <input
          className="w-full max-w-sm mx-auto mb-4 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
        />

        {/* Password Input */}
        <input
          type="password"
          className="w-full max-w-sm mx-auto mb-6 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
          placeholder="Password"
          value={pwd}
          onChange={e => setPwd(e.target.value)}
        />

        {/* Button or Loader */}
        {loading ? (
          <div className="text-green-900 font-semibold">Loading...</div>
        ) : (
          <button
            className="px-6 py-2 rounded-md text-white font-semibold"
            style={{ backgroundColor: "#0F4913" }}
            onClick={submit}
          >
            LOGIN
          </button>
        )}
      </div>
    </div>
  );
}
