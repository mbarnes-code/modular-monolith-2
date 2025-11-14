module.exports = function(api) {
    api.cache.forever();

    const presets = [
        ["@babel/preset-env", {
            "modules": false,
            "useBuiltIns": "entry",
            "corejs": 3,
            "targets": {
                "node": "18", // For backend services
                "browsers": [
                    "> 1%",
                    "last 2 versions",
                    "not dead"
                ]
            }
        }],
        ["@babel/preset-typescript", {
            "allowDeclareFields": true,
            "allowNamespaces": true
        }],
        ["@babel/preset-react", {
            "runtime": "automatic"
        }]
    ];

    const plugins = [
        "@babel/plugin-syntax-import-assertions",
        "@babel/plugin-transform-runtime",
        "babel-plugin-dynamic-import-node"
    ];

    // Environment-specific configurations
    const envConfigs = {
        // Security domain - enhanced transformations
        security: {
            presets,
            plugins: [
                ...plugins,
                ["babel-plugin-transform-builtin-extend", {
                    "globals": ["Error"]
                }]
            ]
        },
        
        // Node.js services
        node: {
            presets: [
                ["@babel/preset-env", {
                    "targets": { "node": "18" },
                    "modules": "commonjs"
                }],
                "@babel/preset-typescript"
            ],
            plugins: ["@babel/plugin-transform-runtime"]
        },

        // Browser/React projects
        browser: {
            presets: [
                ["@babel/preset-env", {
                    "targets": "defaults",
                    "modules": false
                }],
                "@babel/preset-react",
                "@babel/preset-typescript"
            ],
            plugins
        }
    };

    // Apply environment-specific config based on project path or env variable
    const projectPath = process.cwd();
    const babelEnv = process.env.BABEL_ENV;
    
    // Environment override
    if (babelEnv && envConfigs[babelEnv]) {
        return envConfigs[babelEnv];
    }
    
    // Path-based detection
    if (projectPath.includes('/security/')) {
        return envConfigs.security;
    } else if (projectPath.includes('/jane-orchestrator') || projectPath.includes('/llm-server')) {
        return envConfigs.node;
    } else if (projectPath.includes('/jane-ui') || projectPath.includes('/frontend') || projectPath.includes('/site')) {
        return envConfigs.browser;
    }

    // Default configuration for libraries and mixed environments
    return { presets, plugins };
};