import React from "react";
import Select from "react-select";
import { useQuery } from "react-query";
import { apiClient } from "../utils/api";

interface Option {
  value: number;
  label: string;
}

interface Props {
  value: Option[];
  onChange: (opts: Option[]) => void;
  isMulti?: boolean;
}

export const CategorySelector: React.FC<Props> = ({ value, onChange, isMulti = true }) => {
  const { data: categories } = useQuery<Option[]>("categories", async () => {
    const res = await apiClient().get<{ id: number; name: string }[]>("/categories");
    return res.data.map((c) => ({ value: c.id, label: c.name }));
  });

  return (
    <Select
      isMulti={isMulti}
      options={categories || []}
      value={value}
      onChange={(opts) => onChange(opts as Option[])}
      placeholder="카테고리 선택..."
      classNamePrefix="react-select"
    />
  );
}; 