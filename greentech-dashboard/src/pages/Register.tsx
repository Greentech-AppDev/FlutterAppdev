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
      alert("Registered successfully!");
      nav("/dashboard", { replace: true });
    } catch (e: any) {
      alert(e.response?.data?.detail ?? "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen">
      <img src={bg} className="absolute inset-0 -z-10 h-full w-full object-cover" />

      <div className="flex flex-col items-center gap-8 pt-6 pb-16">
        <button onClick={() => nav(-1)} className="self-start p-4 text-white">
          ←
        </button>

        <img src={logo} className="w-36" />
        <h2 className="text-3xl font-bold text-green-900">Register</h2>

        <input
          className="input"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />
        <input
          className="input"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
        />
        <input
          className="input"
          type="password"
          placeholder="Password"
          value={pwd}
          onChange={e => setPwd(e.target.value)}
        />

        {loading
          ? <div className="loader" />
          : <button className="btn-primary" onClick={submit}>REGISTER</button>}
      </div>
    </div>
  );
}
