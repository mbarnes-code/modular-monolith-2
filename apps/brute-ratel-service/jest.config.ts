export default {
  displayName: 'brute-ratel-service',
  preset: '../../jest.preset.js',
  testEnvironment: 'node',
  testTimeout: 5000, // 5 seconds timeout for all tests
  maxWorkers: 1, // Reduce parallel execution to speed up
  verbose: false, // Reduce output for faster execution
  transform: {
    '^.+\\.[tj]s$': ['ts-jest', { tsconfig: '<rootDir>/tsconfig.spec.json' }],
  },
  moduleFileExtensions: ['ts', 'js', 'html'],
  coverageDirectory: '../../coverage/apps/brute-ratel-service',
};
