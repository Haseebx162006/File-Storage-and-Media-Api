import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { forwardRef } from "react";

function cn(...inputs) {
    return twMerge(clsx(inputs));
}

const Button = forwardRef(({ className, variant = "primary", size = "default", isLoading, children, ...props }, ref) => {
    const variants = {
        primary: "bg-black text-white hover:bg-zinc-800 shadow-sm border border-transparent focus-visible:ring-black",
        secondary: "bg-white text-black border border-zinc-200 hover:bg-zinc-100 shadow-sm",
        danger: "bg-red-600 text-white hover:bg-red-700 shadow-sm border border-transparent",
        ghost: "text-zinc-600 hover:bg-zinc-100 hover:text-black",
        link: "text-black hover:text-zinc-700 hover:underline underline-offset-4",
    };

    const sizes = {
        sm: "h-8 px-3 text-xs",
        default: "h-9 px-4 py-2",
        lg: "h-10 px-8",
        icon: "h-9 w-9 p-0 flex items-center justify-center",
    };

    return (
        <button
            className={cn(
                "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-slate-950 disabled:pointer-events-none disabled:opacity-50",
                variants[variant],
                sizes[size],
                className
            )}
            disabled={isLoading || props.disabled}
            ref={ref}
            {...props}
        >
            {isLoading && (
                <svg
                    className="mr-2 h-4 w-4 animate-spin"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                >
                    <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                    ></circle>
                    <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                </svg>
            )}
            {children}
        </button>
    );
});

Button.displayName = "Button";

export { Button };
