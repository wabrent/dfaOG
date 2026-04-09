import { forwardRef, LabelHTMLAttributes } from "react";
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export interface LabelProps extends LabelHTMLAttributes<HTMLLabelElement> {}

const Label = forwardRef<HTMLLabelElement, LabelProps>(
  ({ className, ...props }, ref) => (
    <label
      ref={ref}
      className={twMerge(
        clsx(
          "text-sm font-medium leading-none text-gray-900",
          "peer-disabled:cursor-not-allowed peer-disabled:opacity-70",
          className
        )
      )}
      {...props}
    />
  )
);
Label.displayName = "Label";

export { Label };