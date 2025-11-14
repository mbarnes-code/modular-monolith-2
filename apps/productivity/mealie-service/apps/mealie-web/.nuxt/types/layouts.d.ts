import type { ComputedRef, MaybeRef } from 'vue'
export type LayoutKey = "admin" | "basic" | "blank" | "default" | "error"
declare module 'nuxt/app' {
  interface PageMeta {
    layout?: MaybeRef<LayoutKey | false> | ComputedRef<LayoutKey | false>
  }
}