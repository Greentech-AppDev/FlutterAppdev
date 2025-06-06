import { Link } from "react-router-dom";
import logo from "../assets/logo.png";
import bg from "../assets/bg.png"; // Make sure bg.png is in your /assets folder

export default function Welcome() {
  return (
    <div className="">
      <div
        className="rounded-xl shadow-lg p-20 max-w-md w-full text-center bg-cover bg-center"
        style={{
          backgroundImage: `url(${bg})`,
        }}
      >
        {/* Title */}
        <h1 className="text-4xl font-extrabold text-green-900 mb-4">WELCOME!</h1>

        {/* Logo */}
        <img src={logo} alt="GreenTech Logo" className="w-40 h-auto mx-auto mb-4" />

        {/* Subtitle */}
        <p className="text-lg text-green-800 font-semibold mb-6">GreenTech</p>

        {/* Buttons */}
        <div className="flex justify-center gap-6">
          <Link
            to="/login"
            className="px-6 py-2 rounded-md text-white font-semibold"
            style={{ backgroundColor: "#0F4913" }}
          >
            Login
          </Link>
          <Link
            to="/register"
            className="px-6 py-2 rounded-md text-white font-semibold"
            style={{ backgroundColor: "#275C29" }}
          >
            Register
          </Link>
        </div>
      </div>
    </div>
  );
}
