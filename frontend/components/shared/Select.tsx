"use client";

import { forwardRef, useState, useRef, useEffect, Children, ReactElement } from "react";
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { ChevronDown } from "lucide-react";

interface SelectProps {
  value?: string;
  onValueChange?: (value: string) => void;
  children: React.ReactNode;
  defaultValue?: string;
}

export function Select({ value, onValueChange, children, defaultValue }: SelectProps) {
  const [internalValue, setInternalValue] = useState(value || defaultValue || "");
  const currentValue = value !== undefined ? value : internalValue;

  const handleChange = (newValue: string) => {
    if (value === undefined) {
      setInternalValue(newValue);
    }
    onValueChange?.(newValue);
  };

  // Find the selected child's label
  const selectedChild = Children.toArray(children).find(
    (child) => (child as ReactElement).props.value === currentValue
  );

  return (
    <div className="relative">
      {Children.map(children, (child) => {
        if (!child || typeof child !== "object") return child;
        const element = child as ReactElement;
        return element.type === SelectTrigger
          ? <SelectTrigger {...element.props} selectedLabel={(selectedChild as any)?.props?.children} />
          : element.type === SelectContent
          ? <SelectContent {...element.props} onSelect={handleChange} selectedValue={currentValue} />
          : child;
      })}
    </div>
  );
}

interface SelectTriggerProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  selectedLabel?: React.ReactNode;
}

const SelectTrigger = forwardRef<HTMLButtonElement, SelectTriggerProps>(
  ({ className, selectedLabel, children, ...props }, ref) => {
    const [open, setOpen] = useState(false);

    return (
      <>
        <button
          type="button"
          ref={ref}
          className={twMerge(
            clsx(
              "flex h-10 w-full items-center justify-between rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm",
              "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
              className
            )
          )}
          onClick={() => setOpen(!open)}
          {...props}
        >
          <span className="truncate">{selectedLabel || children}</span>
          <ChevronDown className="h-4 w-4 text-gray-500" />
        </button>
        {open && (
          <div className="absolute z-50 mt-1 w-full rounded-lg border border-gray-200 bg-white shadow-lg">
            {(props as any).children}
          </div>
        )}
      </>
    );
  }
);
SelectTrigger.displayName = "SelectTrigger";

interface SelectContentProps {
  children: React.ReactNode;
  onSelect?: (value: string) => void;
  selectedValue?: string;
}

function SelectContent({ children, onSelect, selectedValue }: SelectContentProps) {
  return (
    <div className="p-1">
      {Children.map(children, (child) => {
        if (!child || typeof child !== "object") return child;
        const element = child as ReactElement;
        if (element.type === SelectItem) {
          return (
            <SelectItem
              {...element.props}
              onSelect={onSelect}
              isSelected={element.props.value === selectedValue}
            />
          );
        }
        return child;
      })}
    </div>
  );
}

interface SelectItemProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  value: string;
  onSelect?: (value: string) => void;
  isSelected?: boolean;
}

const SelectItem = forwardRef<HTMLButtonElement, SelectItemProps>(
  ({ className, value, children, onSelect, isSelected, ...props }, ref) => {
    return (
      <button
        type="button"
        ref={ref}
        className={twMerge(
          clsx(
            "flex w-full items-center rounded-md px-3 py-2 text-sm",
            "hover:bg-gray-100",
            isSelected && "bg-blue-50 text-blue-700 hover:bg-blue-100",
            className
          )
        )}
        onClick={() => onSelect?.(value)}
        {...props}
      >
        {children}
      </button>
    );
  }
);
SelectItem.displayName = "SelectItem";

export { SelectTrigger, SelectContent, SelectItem };