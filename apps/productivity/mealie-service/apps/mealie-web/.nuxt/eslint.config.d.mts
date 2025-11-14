import type { FlatConfigComposer } from "../../../../../../node_modules/.pnpm/eslint-flat-config-utils@2.1.4/node_modules/eslint-flat-config-utils/dist/index.mjs"
import { defineFlatConfigs } from "../../../../../../node_modules/.pnpm/@nuxt+eslint-config@1.10.0_@typescript-eslint+utils@8.46.4_eslint@9.38.0_jiti@2.6.1__ty_b014e05cee3e0a0dcf6fe930bc1fea56/node_modules/@nuxt/eslint-config/dist/flat.mjs"
import type { NuxtESLintConfigOptionsResolved } from "../../../../../../node_modules/.pnpm/@nuxt+eslint-config@1.10.0_@typescript-eslint+utils@8.46.4_eslint@9.38.0_jiti@2.6.1__ty_b014e05cee3e0a0dcf6fe930bc1fea56/node_modules/@nuxt/eslint-config/dist/flat.mjs"

declare const configs: FlatConfigComposer
declare const options: NuxtESLintConfigOptionsResolved
declare const withNuxt: typeof defineFlatConfigs
export default withNuxt
export { withNuxt, defineFlatConfigs, configs, options }