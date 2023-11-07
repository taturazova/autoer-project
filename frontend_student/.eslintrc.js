module.exports = {
    root: true,
    parserOptions: {
        ecmaVersion: 2020,
        sourceType: 'module',
        ecmaFeatures: {
            jsx: true
        }
    },
    settings: {
        react: {
            version: 'detect'
        }
    },
    env: {
        browser: true,
        amd: true,
        node: true
    },
    extends: [
        'eslint:recommended',
        'plugin:react/recommended',
        'plugin:jsx-a11y/recommended',
        'plugin:prettier/recommended',
        'plugin:jest/all'
    ],
    rules: {
        'prettier/prettier': ['error', {}, { usePrettierrc: true }],
        'react/display-name': 'off',
        'react/prop-types': 'off',
        'no-unused-vars': 'warn',
        'no-undef': 'off'
    },
    plugins: ['jest']
}
