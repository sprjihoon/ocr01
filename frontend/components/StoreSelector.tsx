import React, { useEffect } from "react";
import Select from "react-select";
import { useQuery } from "react-query";
import { apiClient } from "../utils/api";

interface Option {
  value: number;
  label: string;
}

interface Props {
  value: number | undefined;
  onChange: (storeId: number) => void;
}

export const StoreSelector: React.FC<Props> = ({ value, onChange }) => {
  const { data: stores } = useQuery<Option[]>("stores", async () => {
    const res = await apiClient().get<{ id: number; name: string }[]>("/stores");
    return res.data.map((s) => ({ value: s.id, label: s.name }));
  });

  useEffect(() => {
    if (!value && stores && stores.length > 0) {
      onChange(stores[0].value);
    }
  }, [stores]);

  return (
    <Select
      options={stores || []}
      value={stores?.find((o) => o.value === value)}
      onChange={(opt) => opt && onChange(opt.value)}
      placeholder="매장 선택..."
      classNamePrefix="react-select"
    />
  );
}; 