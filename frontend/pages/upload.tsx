import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { apiClient } from "../utils/api";
import axios from "axios";
import { useRouter } from "next/router";

interface Store {
  id: number;
  name: string;
}

export default function UploadPage() {
  const { token } = useAuth();
  const router = useRouter();
  const [stores, setStores] = useState<Store[]>([]);
  const [storeId, setStoreId] = useState<number | undefined>();
  const [zone, setZone] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      router.push("/login");
      return;
    }
    const fetchStores = async () => {
      try {
        const res = await apiClient().get<Store[]>("/stores");
        setStores(res.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchStores();
  }, [token]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !storeId || !zone) return;

    try {
      // Step1: get presigned
      const presRes = await apiClient().post("/images/presigned", {
        filename: file.name,
        content_type: file.type,
      });
      const { url, fields, key } = presRes.data;

      // Step2: upload to S3
      const formData = new FormData();
      Object.entries(fields).forEach(([k, v]) => formData.append(k, v as string));
      formData.append("file", file);
      await axios.post(url, formData, { headers: { "Content-Type": "multipart/form-data" } });

      // Step3: notify backend
      const notifyRes = await apiClient().post("/images/complete", {
        store_id: storeId,
        zone,
        key,
        image_url: `${url}/${key}`,
      });

      setMessage("업로드 완료 및 OCR 처리 중. 결과가 저장되었습니다.");
      console.log(notifyRes.data);
    } catch (err: any) {
      console.error(err);
      setMessage(err.response?.data?.detail || "업로드 실패");
    }
  };

  return (
    <div className="max-w-xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">가격표 업로드</h1>
      {message && <p className="mb-4 text-green-700">{message}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block mb-1">매장</label>
          <select
            className="border p-2 w-full"
            value={storeId}
            onChange={(e) => setStoreId(Number(e.target.value))}
          >
            <option value="">선택</option>
            {stores.map((s) => (
              <option key={s.id} value={s.id}>{s.name}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="block mb-1">Zone</label>
          <input className="border p-2 w-full" value={zone} onChange={(e) => setZone(e.target.value)} />
        </div>
        <div>
          <label className="block mb-1">이미지</label>
          <input type="file" accept="image/*" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        </div>
        <button className="bg-blue-600 text-white py-2 px-4 rounded">업로드</button>
      </form>
    </div>
  );
} 