import { useQuery } from "@tanstack/react-query";
import { api } from "../api/api";
import bg from "../assets/bg2.png";
import logo from "../assets/logo.png";
import waterIcon from "../assets/watertemplogo.png";
import airIcon from "../assets/airtemplogo.png";
import { Link } from "react-router-dom";

export default function Dashboard() {
  const token = localStorage.getItem("token");

  const { data } = useQuery({
    queryKey: ["temps"],
    queryFn: async () =>
      (await api.get("/latest-temperature", {
        headers: { Authorization: `Bearer ${token}` },
      })).data,
    refetchInterval: 3000,
  });

  return (
    <div className="relative min-h-screen bg-cover bg-center">
      <img
        src={bg}
        alt="Background"
        className="absolute inset-0 -z-10 h-full w-full object-cover"
      />

      <div className="mx-auto max-w-screen-md px-6 py-4">
        {/* Home Button */}
        <Link
          to="/"
          className="btn-primary flex w-fit items-center gap-2 rounded-full bg-green-800 px-4 py-2 text-white shadow hover:bg-green-900"
        >
          <span className="material-icons">HOME</span> 
        </Link>

        {/* Logo + Title */}
        <div className="mt-6 flex flex-col items-center gap-4">
          <img src={logo} alt="Logo" className="w-20" />
          <h2 className="text-2xl font-bold text-green-900 tracking-wider">
            TEMPERATURE
          </h2>
        </div>

        {/* Cards */}
        <div className="mt-8 flex flex-col items-center gap-6">
          <TempCard
            icon={waterIcon}
            label="Temperature"
            value={data ? `${data.water_temperature.toFixed(1)}°C` : "—"}
          />
          <TempCard
            icon={airIcon}
            label="Humidity"
            value={data ? `${data.air_temperature.toFixed(1)}°C` : "—"}
          />
        </div>
      </div>
    </div>
  );
}

function TempCard({
  icon,
  label,
  value,
}: {
  icon: string;
  label: string;
  value: string;
}) {
  return (
    <div className="flex w-full max-w-md items-center gap-5 rounded-2xl bg-green-600 p-5 shadow-md">
      <img src={icon} alt={label} className="w-10" />
      <div>
        <p className="font-medium text-white">{label}</p>
        <p className="text-lg font-bold text-white">{value}</p>
      </div>
    </div>
  );
}
