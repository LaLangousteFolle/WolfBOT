"use client";
import { useEffect, useState } from "react";

export default function RolesConfig({ nbJoueurs }) {
  const [roles, setRoles] = useState([]);
  const [quantities, setQuantities] = useState({});

  useEffect(() => {
    fetch("http://localhost:8000/roles")
      .then((res) => res.json())
      .then((data) => {
        setRoles(data);
        const initialQuantities = {};
        data.forEach((role) => {
          initialQuantities[role.id] = 0;
        });
        setQuantities(initialQuantities);
      });
  }, []);

  const increment = (id) => {
    setQuantities((prev) => ({
      ...prev,
      [id]: prev[id] + 1,
    }));
  };

  const decrement = (id) => {
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
              <img
                src={role.image}
                alt={role.name}
                className="w-full h-full object-cover"
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
