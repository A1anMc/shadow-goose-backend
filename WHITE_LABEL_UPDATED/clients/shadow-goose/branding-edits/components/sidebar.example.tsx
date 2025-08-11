import Image from "next/image";

export function SidebarExample({ branding }: { branding: { logoLight: string; name: string } }) {
  return (
    <aside className="h-full w-64 bg-[var(--sg-primary)] text-[var(--sg-secondary)]">
      <div className="flex items-center gap-3 p-4">
        <Image src={branding.logoLight} alt={branding.name} width={28} height={28} />
        <span className="sg-heading text-lg font-semibold">{branding.name}</span>
      </div>
    </aside>
  );
}
