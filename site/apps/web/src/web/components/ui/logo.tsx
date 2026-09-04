import { cn } from "~/web/lib/cn";

// La marque : le logo (douze disques en spirale) et le nom. L'image PNG est
// l'original fourni ; réduite pour le web (512 px), elle sert partout.

export function Logo({ className, size = 28 }: { className?: string; size?: number }) {
  return (
    <img
      src="/logo-512.png"
      alt=""
      width={size}
      height={size}
      className={cn("inline-block select-none", className)}
    />
  );
}

export function Wordmark({ className }: { className?: string }) {
  return (
    <span className={cn("inline-flex items-center gap-2.5", className)}>
      <Logo size={30} />
      <span className="font-sans text-[1.05rem] font-semibold tracking-tight text-ink">
        Métabolisme
      </span>
    </span>
  );
}
