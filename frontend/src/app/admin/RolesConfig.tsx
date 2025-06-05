"use client";
import Image from "next/image";
import { useEffect, useState } from "react";

type Role = {
  id: string;
  name: string;
  description?: string;
  type?: string;
  image?: string;
};

export default function RolesConfig({ nbJoueurs }: { nbJoueurs: number }) {
  const [roles, setRoles] = useState<Role[]>([]);
  const [quantities, setQuantities] = useState<Record<string, number>>({});

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/roles`)
      .then((res) => res.json())
      .then((data) => {
        console.log("data reçue:", data);
        const rolesData = data as Role[]; // cast explicite
        setRoles(rolesData);
        const initialQuantities: Record<string, number> = {};
        rolesData.forEach((role) => {
          initialQuantities[role.id] = 0;
        });
        setQuantities(initialQuantities);
      });
  }, []);

  const increment = (id: string) => {
    setQuantities((prev) => ({
      ...prev,
      [id]: prev[id] + 1,
    }));
  };

  const decrement = (id: string) => {
    setQuantities((prev) => ({
      ...prev,
      [id]: Math.max(0, prev[id] - 1),
    }));
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Rôles disponibles</h2>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
        {roles.map((role) => (
          <div
            key={role.id}
            className="flex flex-col items-center bg-gray-100 p-4 rounded-lg shadow-md"
          >
            <p className="font-semibold text-center mb-2">{role.name}</p>
            <div className="w-20 h-20 rounded-full overflow-hidden border-2 border-gray-300 mb-2">
              <Image
                src={role.image ?? "/placeholder.png"}
                alt={role.name}
                className="w-full h-full object-cover"
                width={80}
                height={80}
              />
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => decrement(role.id)}
                className="px-2 py-1 bg-red-500 text-white rounded"
              >
                -
              </button>
              <span className="text-lg font-medium">{quantities[role.id]}</span>
              <button
                onClick={() => increment(role.id)}
                className="px-2 py-1 bg-green-500 text-white rounded"
              >
                +
              </button>
            </div>
          </div>
        ))}
      </div>
      <p>{nbJoueurs}</p>
    </div>
  );
}
