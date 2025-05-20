import { useQuery } from "@tanstack/react-query";
import { api } from "../api/api";
import bg from "../assets/bg2.png";
import logo from "../assets/logo.png";
import waterIcon from "../assets/watertemplogo.png";
import airIcon from "../assets/airtemplogo.png";
import { Link } from "react-router-dom";

export default function Dashboard() {
  const token =
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIn0.CsnstcipfQ_rNlGYCBOhPNthAgL_q5Q22eW6n96tBQ0";

  const { data, error, isLoading } = useQuery({
    queryKey: ["temps"],
    queryFn: async () => {
      const response = await api.get("/temperature/latest", {
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.data;
    },
    refetchInterval: 3000,
  });

  return (
    <div className="">
      <div
        className="rounded-xl shadow-lg p-20 w-full max-w-4xl bg-cover bg-center relative"
        style={{
          backgroundImage: `url(${bg})`,
        }}
      >
        {/* Home Button */}
        <Link
          to="/"
          className="absolute top-6 left-6 btn-primary flex items-center gap-2 rounded-full bg-green-800 px-4 py-2 text-white shadow hover:bg-green-900"
        >
          <span className="material-icons">home</span>
        </Link>

        {/* Logo + Title */}
        <div className="flex flex-col items-center gap-4 mb-8">
          <img src={logo} alt="Logo" className="w-20" />
          <h2 className="text-3xl font-bold text-green-900 tracking-wide">
            TEMPERATURE
          </h2>
        </div>

        {/* Loading/Error State */}
        {isLoading && <p className="text-white text-center">Loading...</p>}
        {error && (
          <p className="text-red-500 text-center">
            Error fetching data: {(error as any).message}
          </p>
        )}

        {/* Temperature Cards */}
        <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
          <TempCard
            icon={waterIcon}
            label="Water Temperature"
            value={data ? `${data.water_temperature.toFixed(1)}°C` : "—"}
          />
          <TempCard
            icon={airIcon}
            label="Air Humidity"
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
    <div className="flex flex-col items-center justify-center text-center gap-3 rounded-xl bg-green-600 p-3 shadow-md">
      <img src={icon} alt={label} className="w-50 h-16" />
      <p className="text-white text-sm font-medium">{label}</p>
      <p className="text-white text-2xl font-bold">{value}</p>
    </div>
  );
}

