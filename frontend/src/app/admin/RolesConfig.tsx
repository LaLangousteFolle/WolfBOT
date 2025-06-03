"use client";
import { useEffect, useState } from "react";

export default function RolesConfig() {
  const [roles, setRoles] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/roles")
      .then((res) => res.json())
      .then((data) => setRoles(data));
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-2">Rôles disponibles</h2>
      <ul className="space-y-2">
        {roles.map((role) => (
          <li key={role.id} className="p-2 border rounded bg-gray-100">
            <p className="font-semibold">{role.name}</p>
            <p className="text-sm text-gray-700">{role.description}</p>
            <p className="text-xs text-gray-500 italic">Type: {role.type}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
