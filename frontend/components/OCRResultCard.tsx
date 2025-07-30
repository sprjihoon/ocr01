import React from "react";

interface Props {
  product_name: string;
  price: number;
  event_info?: string;
  badge7?: boolean;
  badge30?: boolean;
}

export const OCRResultCard: React.FC<Props> = ({ product_name, price, event_info, badge7, badge30 }) => {
  return (
    <div className="border p-4 rounded shadow-sm mb-2 flex justify-between items-center">
      <div>
        <h3 className="font-semibold">{product_name}</h3>
        <p className="text-gray-700">{price.toLocaleString()}원</p>
        {event_info && <p className="text-sm text-blue-600">{event_info}</p>}
      </div>
      <div className="space-x-2">
        {badge7 && <span className="bg-green-600 text-white text-xs px-2 py-1 rounded">7일 최저가</span>}
        {badge30 && <span className="bg-yellow-500 text-white text-xs px-2 py-1 rounded">30일 최저가</span>}
      </div>
    </div>
  );
}; 