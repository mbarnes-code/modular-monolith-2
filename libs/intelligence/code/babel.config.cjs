module.exports = {
    presets: [
        ["@babel/preset-env", {
            "targets": { "node": "18" },
            "modules": "commonjs"
        }],
        "@babel/preset-typescript"
    ],
    plugins: [
        "@babel/plugin-transform-runtime"
    ]
};