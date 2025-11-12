/* eslint-disable */
export default {
  displayName: 'kasmvnc-service',
  preset: '../../jest.preset.js',
  testEnvironment: 'node',
  transform: {
    '^.+\\.[tj]s$': ['ts-jest', { tsconfig: '<rootDir>/tsconfig.spec.json' }],
  },
  moduleFileExtensions: ['ts', 'js', 'html'],
  coverageDirectory: '../../coverage/apps/kasmvnc-service',
  testMatch: [
    '<rootDir>/src/**/*.(test|spec).{js,ts}',
    '<rootDir>/tests/**/*.(test|spec).{js,ts}',
  ],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/main.ts',
    '!src/**/*.d.ts',
  ],
};