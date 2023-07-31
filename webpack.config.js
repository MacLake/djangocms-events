const path = require('path');

module.exports = {
    entry: {
        index: './assets/src/index.js',
        calendar:  './assets/src/calendar.js',
    },
    module: {
        rules: [
            {
                test: /\.css$/i,
                use: ["style-loader", "css-loader"],
            },
        ],
    },
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, './src/djangocms_events/static/djangocms_events/webpack'),
        clean: true,
    },
    mode: 'production',
};