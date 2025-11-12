export default {
  displayName: 'blackarch-service',
  preset: '../../jest.preset.js',
  testEnvironment: 'node',
  transform: {
    '^.+\\.[tj]s$': ['ts-jest', { tsconfig: '<rootDir>/tsconfig.spec.json' }],
  },
  moduleFileExtensions: ['ts', 'js', 'html'],
  coverageDirectory: '../../coverage/blackarch-service',
  moduleNameMapper: {
    '^blackarch$': '<rootDir>/../../libs/blackarch/src/index.ts',
  },
};
