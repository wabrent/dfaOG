"use client";

import { forwardRef, InputHTMLAttributes } from "react";
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { Check } from "lucide-react";

export interface CheckboxProps extends InputHTMLAttributes<HTMLInputElement> {}

const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
  ({ className, checked, ...props }, ref) => {
    return (
      <div className="relative flex h-5 w-5 items-center">
        <input
          type="checkbox"
          className={twMerge(
            clsx(
              "peer h-5 w-5 cursor-pointer appearance-none rounded border border-gray-400",
              "checked:border-blue-600 checked:bg-blue-600",
              "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2",
              "disabled:cursor-not-allowed disabled:opacity-50",
              className
            )
          )}
          checked={checked}
          ref={ref}
          {...props}
        />
        {checked && (
          <Check className="pointer-events-none absolute left-1/2 top-1/2 h-3.5 w-3.5 -translate-x-1/2 -translate-y-1/2 text-white" />
        )}
      </div>
    );
  }
);
Checkbox.displayName = "Checkbox";

export { Checkbox };