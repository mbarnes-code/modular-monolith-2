/* eslint-disable */
export default {
  displayName: "inspector-service",
  preset: "../../jest.preset.js",
  testEnvironment: "node",
  transform: {
    "^.+\\.[tj]s$": ["ts-jest", { tsconfig: "<rootDir>/server/tsconfig.json" }],
  },
  moduleFileExtensions: ["ts", "js", "html"],
  coverageDirectory: "../../coverage/apps/inspector-service",
  testMatch: [
    "<rootDir>/server/src/**/*.{test,spec}.{js,ts}",
    "<rootDir>/cli/src/**/*.{test,spec}.{js,ts}",
  ],
  collectCoverageFrom: [
    "server/src/**/*.{ts,js}",
    "cli/src/**/*.{ts,js}",
    "!**/*.d.ts",
  ],
};
