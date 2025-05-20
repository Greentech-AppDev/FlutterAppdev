import { useQuery } from "@tanstack/react-query";
import { api, bearer } from "../api/api";
import bg from "../assets/bg2.png";
import logo from "../assets/logo.png";
import waterIcon from "../assets/watertemplogo.png";
import airIcon from "../assets/airtemplogo.png";
import { Link } from "react-router-dom";

export default function Dashboard() {
  const { data } = useQuery({
    queryKey: ["temps"],
    queryFn: async () =>
      (await api.get("/latest-temperature", {
        headers: { Authorization: `Bearer ${bearer}` },
      })).data,
    refetchInterval: 3000,
  });

  return (
    <div className="relative min-h-screen">
      <img src={bg} className="absolute inset-0 -z-10 h-full w-full object-cover" />

      <div className="p-4">
        <Link to="/" className="btn-primary flex w-fit items-center gap-2">
          <span className="material-icons">home</span> HOME
        </Link>
      </div>

      <div className="flex flex-col items-center gap-8 pt-4">
        <img src={logo} className="w-20" />
        <h2 className="text-xl font-bold text-green-900 tracking-wide">TEMPERATURE</h2>

        <TempCard
          icon={waterIcon}
          label="Water Temperature"
          value={data ? `${data.water_temperature.toFixed(1)}°C` : "—"}
        />
        <TempCard
          icon={airIcon}
          label="Air Temperature"
          value={data ? `${data.air_temperature.toFixed(1)}°C` : "—"}
        />
      </div>
    </div>
  );
}

function TempCard({ icon, label, value }: { icon: string; label: string; value: string }) {
  return (
    <div className="mx-6 flex w-full max-w-md items-center gap-5 rounded-2xl bg-green-600 p-5">
      <img src={icon} className="w-10" />
      <div>
        <p className="font-medium text-white">{label}</p>
        <p className="text-lg font-bold text-white">{value}</p>
      </div>
    </div>
  );
}
