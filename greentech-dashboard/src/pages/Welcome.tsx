import { Link } from "react-router-dom";
import bg   from "../assets/bg.png";     // make sure the images are in /src/assets
import logo from "../assets/logo.png";

export default function Welcome() {
  return (
    <div
      className="min-h-screen w-full flex items-center justify-center bg-cover bg-center"
      style={{ backgroundImage: `url(${bg})` }}
    >
      <div className="flex flex-col items-center gap-6 px-4">
        {/* headline */}
        <h1 className="text-6xl font-extrabold text-green-900 text-center drop-shadow-sm">
          WELCOME!
        </h1>

        {/* logo */}
        <img src={logo} alt="logo" className="w-64 max-w-full" />

        {/* buttons */}
        <div className="flex flex-col gap-4 w-full max-w-md px-8">
          <Link
            to="/login"
            className="rounded-xl py-4 text-white text-xl font-semibold text-center"
            style={{ backgroundColor: "#0F4913" }}   /* dark green */
          >
            Login
          </Link>

          <Link
            to="/register"
            className="rounded-xl py-4 text-white text-xl font-semibold text-center"
            style={{ backgroundColor: "#275C29" }}   /* slightly lighter green */
          >
            Register
          </Link>
        </div>
      </div>
    </div>
  );
}
