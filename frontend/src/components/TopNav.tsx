"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

type NavItem = {
  href: string;
  label: string;
  isActive: (pathname: string) => boolean;
};

const navItems: NavItem[] = [
  { href: "/", label: "Overview", isActive: (p) => p === "/" },
  { href: "/entities", label: "Entities", isActive: (p) => p === "/entities" || p.startsWith("/entities/") },
  { href: "/categories", label: "Categories", isActive: (p) => p === "/categories" || p.startsWith("/categories/") },
  { href: "/flows", label: "Flows", isActive: (p) => p === "/flows" || p.startsWith("/flows/") },
];

export default function TopNav() {
  const pathname = usePathname() ?? "/";

  return (
    <nav className="ml-auto flex items-center gap-1 overflow-x-auto">
      {navItems.map((item) => {
        const active = item.isActive(pathname);
        return (
          <Link
            key={item.href}
            href={item.href}
            className={[
              "px-3 py-2 rounded-lg text-sm font-medium transition-colors whitespace-nowrap",
              active ? "bg-zinc-800 text-white" : "text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900",
            ].join(" ")}
          >
            {item.label}
          </Link>
        );
      })}
    </nav>
  );
}

