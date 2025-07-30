import React from "react";
import Link from "next/link";

interface Props {
  id: number;
  name: string;
  image_url?: string;
  recent_price?: number;
  badge7?: boolean;
  badge30?: boolean;
}

export const ProductCard: React.FC<Props> = ({ id, name, image_url, recent_price, badge7, badge30 }) => {
  return (
    <Link href={`/products/${id}`} className="block border rounded shadow-sm overflow-hidden hover:shadow-lg transition">
      {image_url ? <img src={image_url} alt={name} className="w-full h-40 object-cover" /> : <div className="w-full h-40 bg-gray-200" />}
      <div className="p-4">
        <h3 className="font-semibold mb-1 text-sm truncate">{name}</h3>
        {recent_price && <p className="text-gray-700 text-sm">{recent_price.toLocaleString()}원</p>}
        <div className="space-x-1 mt-1">
          {badge7 && <span className="bg-green-600 text-white text-xs px-1.5 rounded">7일 최저가</span>}
          {badge30 && <span className="bg-yellow-500 text-white text-xs px-1.5 rounded">30일 최저가</span>}
        </div>
      </div>
    </Link>
  );
}; 