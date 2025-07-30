import React from "react";
import { useAuth } from "../../context/AuthContext";
import { apiClient } from "../../utils/api";
import useSWR from "swr";
import { useRouter } from "next/router";

const fetcher = (url: string) => apiClient().get(url).then((r) => r.data);

export default function AdminDashboard() {
  const { token } = useAuth();
  const router = useRouter();
  if (!token) {
    router.push("/login");
    return null;
  }

  const { data: logs } = useSWR("/logs", fetcher);
  const { data: users } = useSWR("/users", fetcher);
  const { data: stores } = useSWR("/stores", fetcher);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">관리자 대시보드</h1>
      <section className="mb-8">
        <h2 className="font-semibold mb-2">요약</h2>
        <ul className="list-disc ml-6">
          <li>사용자: {users?.length ?? "-"}</li>
          <li>매장: {stores?.length ?? "-"}</li>
          <li>로그 수: {logs?.length ?? "-"}</li>
        </ul>
      </section>
      <section className="mb-8">
        <h2 className="font-semibold mb-2">최근 로그</h2>
        <table className="w-full text-sm border">
          <thead>
            <tr className="bg-gray-100">
              <th className="border px-2 py-1">ID</th>
              <th className="border px-2 py-1">User</th>
              <th className="border px-2 py-1">Action</th>
              <th className="border px-2 py-1">Meta</th>
            </tr>
          </thead>
          <tbody>
            {logs?.slice(0, 20).map((l: any) => (
              <tr key={l.id}>
                <td className="border px-2 py-1">{l.id}</td>
                <td className="border px-2 py-1">{l.user_id}</td>
                <td className="border px-2 py-1">{l.action}</td>
                <td className="border px-2 py-1 text-xs whitespace-pre-wrap">{JSON.stringify(l.meta)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
} 