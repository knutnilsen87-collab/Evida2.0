declare module "next/dist/lib/metadata/types/metadata-interface.js" {
  export type ResolvingMetadata = unknown;
  export type ResolvingViewport = unknown;
}

declare module "next" {
  export type Metadata = Record<string, unknown>;
}

declare module "next/link" {
  import type { AnchorHTMLAttributes, ReactNode } from "react";

  export default function Link(
    props: AnchorHTMLAttributes<HTMLAnchorElement> & { href: string; children?: ReactNode }
  ): JSX.Element;
}
