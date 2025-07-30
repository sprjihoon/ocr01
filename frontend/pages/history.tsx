import React, { useState } from "react";
import { useQuery } from "react-query";
import { apiClient } from "../utils/api";
import { PriceHistoryChart } from "../components/PriceHistoryChart";
import { OCRResultCard } from "../components/OCRResultCard";
import { useRouter } from "next/router";
import { useAuth } from "../context/AuthContext";

interface PH {
  id: number;
  product_name: string;
  price: number;
  date: string;
  event_info?: string;
  badge7?: boolean;
  badge30?: boolean;
}

export default function HistoryPage() {
  const { token } = useAuth();
  const router = useRouter();
  const [selectedProduct, setSelectedProduct] = useState<string | null>(null);

  const { data: histories } = useQuery<PH[]>("histories", async () => {
    const res = await apiClient().get<PH[]>("/price-history");
    return res.data;
  });

  if (!token) {
    router.push("/login");
    return null;
  }

  const products = Array.from(new Set(histories?.map((h) => h.product_name)));
  const filtered = selectedProduct
    ? histories?.filter((h) => h.product_name === selectedProduct) || []
    : [];

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">가격 이력</h1>
      <div className="mb-4">
        <label className="mr-2">상품:</label>
        <select value={selectedProduct || ""} onChange={(e) => setSelectedProduct(e.target.value)}>
          <option value="">선택</option>
          {products.map((p) => (
            <option key={p} value={p}>{p}</option>
          ))}
        </select>
      </div>
      {selectedProduct && (
        <>
          <PriceHistoryChart data={filtered.map((h) => ({ date: h.date, price: h.price }))} />
          <h2 className="text-xl font-semibold mt-6 mb-2">이력</h2>
          {filtered.map((h) => (
            <OCRResultCard
              key={h.id}
              product_name={h.product_name}
              price={h.price}
              event_info={h.event_info}
              badge7={h.badge7}
              badge30={h.badge30}
            />
          ))}
        </>
      )}
    </div>
  );
} 